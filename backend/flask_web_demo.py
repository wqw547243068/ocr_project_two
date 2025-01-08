# !/usr/bin/env python
# -*- coding:utf8 -*- 

# **************************************************************************
# * Copyright (c) 2024. All Rights Reserved
# **************************************************************************
# * @function OCR Demo, tesseract+Vite UI 实现, windows 环境
# * @author wqw547243068@163.com
# * @date 2024/12/05 17:00
# **************************************************************************


import os
import json
import logging
import threading
from queue import Queue
import socket
import time
import random
from flask import Flask, request, send_file
from conf import response_info, font_path

app = Flask(__name__)

# 日志系统配置
handler = logging.FileHandler('app.log', encoding='UTF-8') # 日志输出到终端
# handler = logging.StreamHandler() # 日志输出到控制台
#设置日志文件，和字符编码
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
#设置日志存储格式，也可自定义日志格式满足不同的业务需求
logger = logging.getLogger(__name__)

cur_dir = os.path.dirname(__file__)
cache_dir = os.path.join(cur_dir, os.pardir, 'cache_file')
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = cache_dir
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 设置最大文件上传大小为 100MB

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

# 服务器 ip地址: 跨机器访问时图片无法显示，ip地址从localhost改127.0.0.1或0.0.0.0都不管用，最后用实际ip地址
# http://0.0.0.0:5000/download?fileId=123.tar
local_host_ip = extract_ip()
local_file_url = f'http://{local_host_ip}:5000/download?fileId='

def log(msg):
    """
        多进程日志输出
    """
    pid = os.getpid()
    tid = threading.current_thread().ident
    logging.info(f"进程[{pid}]-线程[{tid}]: {msg}")


@app.route('/')
def home():
    app.logger.info('主页请求')
    # app.logger.info('message info is %s', message, exc_info=1)。
    #app.logger.exception('%s', e) # 异常信息
    return 'OCR接口主页!'
    # return render_template('index.html') 


@app.route("/download")
def download_file():
    """
    下载 src_file 目录下的文件
    eg: 下载当前目录下123.tar 文件 http://0.0.0.0:5000/download?fileId=123.tar
    """
    file_name = request.args.get('fileId')
    file_path = os.path.join(cache_dir, file_name)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"

@app.route('/api_ocr', methods = ["GET", "POST"])
def post_data():
    # 获取客户端的文件信息
    remote_file = '-'
    # ======= 统一 ======
    if request.method == 'POST':
        # data = request.json
        # data = request.form.to_dict()
        # data = request.values
        data = request.files
        file = data['uploadFile'] # 请求方设置的文件名字段
        # 文件写入磁盘
        cur_file = os.path.join(cache_dir, file.filename)
        file.save(cur_file)
        remote_file = local_file_url + file.filename
    elif request.method == 'GET':
        data = request.args
        cur_file = data['uploadFile']
        remote_file = cur_file
    
    logger.info(f"请求参数: {data=}, {cur_file=}")
    res = {"status":0, 
            "msg":'-', 
            "data":{
                "content":[], # 识别内容
                "merge_image": remote_file, # 融合图
                "scores":[], # 分值
            }, 
            'req':{'file_name': cur_file} # 请求信息
    }
    
    if not os.path.exists(cur_file):
        res['status'] = -1
        res['msg'] = f"文件{cur_file}不存在"
        logger.error(res['msg'])
        return json.dumps(res, ensure_ascii=False)

    res['req']['file_name'] = os.path.basename(cur_file)
    if cur_file.find('.') != -1:
        cur_ext = cur_file.split('.')[-1]
    else:
        cur_ext = '-'
    cur_ext = cur_ext.lower()
    res['data']['file_type'] = cur_ext
    
    # 预设字典
    file_ext = res['req']['file_name']
    if file_ext in response_info:
        res['data']['content'] = response_info[file_ext]['content'].split('\n')
        res['data']['num'] = len(res['data']['content'])
        res['status'] = 1
        res['msg'] = '字典映射'
        res['data']['merge_image'] = local_file_url + response_info[file_ext]['merge_image']
        sleeptime = random.uniform(1, 2)
        time.sleep(sleeptime)
        return res
    else:
        logging.error('非测试文件, 跳出。。。')
        res['status'] = 0
        res['msg'] = '非测试文件'
        return res


if __name__ == '__main__':
    #app.run() # 本地访问：只能从自己的计算机上访问
    app.run(host='0.0.0.0', debug=True) # 外网可访问

