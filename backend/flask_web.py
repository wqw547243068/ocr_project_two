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
from flask import Flask, request, jsonify, render_template, send_file

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

from PIL import Image
from docx import Document
import pdfplumber
import pytesseract
from paddleocr import PaddleOCR, draw_ocr
import langid

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

cur_dir = os.path.dirname(__file__)
cache_dir = os.path.join(cur_dir, os.pardir, 'cache_file')
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = cache_dir
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 设置最大文件上传大小为 100MB



if not os.path.exists(cache_dir):
    os.mkdirs(cache_dir)

def parseDoc(file_name):
    """
        word 文档解析
    """
    content_info = {"num": 0, "content":[], "status":0, 'msg':'-'}
    # 读取文档
    try:
        doc = Document(file_name)
        print(f"文件{file_name}解析成功")
        content_info['num'] = len(doc.paragraphs)
        for paragraph in doc.paragraphs:
            content_info['content'].append(paragraph.text)
        content_info['status'] = 1
        content_info['msg'] = 'word解析完毕'
    except Exception as err:
        # logging.error(f"word文档解析失败 {file_name} ...")
        content_info['status'] = -2
        content_info['msg'] = err
    return content_info

def parsePDF(file_name):
    """
        pdf 文档解析
    """
    content_info = {"num": 0, "content":[], "status":0, "msg":'-'}
    # 读取文档
    try:
        pdf =  pdfplumber.open(file_name)
        content_info['num'] = len(pdf.pages)
        # for page in pdf.pages:
        #     content_info['content'].append(page.extract_text())
        for i, page in enumerate(pdf.pages):
            content_info['content'].extend([f'==[第{i}页]==', page.extract_text()])
        content_info['status'] = 1
        content_info['msg'] = 'pdf解析完毕'
    except Exception as err:
        # logging.error(f"pdf文档解析失败 {file_name} ...")
        content_info['status'] = -1
        content_info['msg'] = err
    return content_info


def parseOCR(file_name, hand=False):
    """
        图片OCR: tesseract 
        特点: 支持多语种, 但手写体、场景图片文字识别效果一般
    """
    content_info = {"num": 0, "content":[], "status":0, "msg":'-', 'merge_image':'-'}
    # 读取文档
    try:
        if hand:
            out = pytesseract.image_to_string(file_name, lang='chi_sim', config="--psm 4") # 中文手写体识别
        else:
            out = pytesseract.image_to_string(file_name, lang='chi_sim+eng+deu+fra+rus+jpn')
        # 数据示例： g 611 283 631 297 0
        out = out.split('\n') if out else []
        # out = [ i.replace(' ','') for i in out.split('\n')]
        content_info['num'] = len(out)
        content_info['content'] = out
        content_info['status'] = 1
        content_info['msg'] = '图片OCR解析完毕'
    except Exception as err:
        # logging.error(f"pdf文档解析失败 {file_name} ...")
        content_info['status'] = -1
        content_info['msg'] = err
    return content_info


def parseOCRNew(file_name):
    """
        图片OCR: PaddleOCR,
        特点: 识别效果更好，但不支持多语种自动检测
    """
    content_info = {"num": 0, "content":[], "status":0, "msg":'-', "merge_image":'-'}
    # 读取文档
    try:
        out = ocr.ocr(file_name, cls=True) # 方向分类器
        # result = ocr.ocr(file_name, det=False) # 每个item只有文本内容和置信度
        # result = ocr.ocr(file_name, cls=True, det=False) # 不需要文本框，每个item只有文本内容和置信度
        # result = ocr.ocr(file_name, cls=True, rec=False) # 不需要文本内容，每个item只有文本框
        # result = ocr.ocr(file_name, cls=True, rec=False, det=False) #  仅执行方向分类器, 返回分类结果+置信度
        # 数据格式样例, [边框点坐标, [识别文本, 置信度]]
        # [[[442.0, 173.0], [1169.0, 173.0], [1169.0, 225.0], [442.0, 225.0]], ['ACKNOWLEDGEMENTS', 0.99283075]]

        # 结果可视化展示
        result = out[0]
        image = Image.open(file_name).convert('RGB')
        boxes, txts, scores = [], [], []
        for line in result:
            if not line:
                continue
            boxes.append(line[0])
            txts.append(line[1][0])
            scores.append(line[1][1])

        im_show = draw_ocr(image, boxes, txts, scores, font_path='/fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        new_file = os.path.basename(file_name).replace('.', '_merge.')
        remote_file = f'http://localhost:5000/download?fileId={new_file}'
        im_show.save(os.path.join(os.path.dirname(file_name), new_file))
        # im_show.show('result.jpg')

        # out = out.split('\n') if out else []
        # out = [ i.replace(' ','') for i in out.split('\n')]
        content_info['num'] = len(out)
        content_info['content'] = [i[1][0] for i in result]
        content_info['status'] = 1
        content_info['msg'] = '图片OCR二次解析完毕'
        content_info['merge_image'] = remote_file
    except Exception as err:
        # logging.error(f"pdf文档解析失败 {file_name} ...")
        content_info['status'] = -1
        content_info['msg'] = err
    return content_info




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
    eg: 下载当前目录下123.tar 文件 http://localhost:5000/download?fileId=123.tar
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
        remote_file = f'http://localhost:5000/download?fileId={file.filename}'
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
            'req':{} # 请求信息
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
    # 格式检测
    if cur_ext in ('doc', 'docx'): # word 文档, 直接解析
        res['data']['content'] = ['word 文档内容']
        res['msg'] = 'word文件'
        out = parseDoc(cur_file)
        res['status'] = out['status']
        res['data']['merge_image'] = f'http://localhost:5000/download?fileId=word.jpg'
        if out['msg'] != '-':
            res['msg'] = out['msg']
        if out['status'] > 0:
            res['data']['content'] = out['content']
        else:
            logger.error(f"word文档解析失败 {cur_file=} -> {out=} ...")
    elif cur_ext in ('pdf'): # pdf 文档
        res['data']['content'] = ['pdf 文档内容']
        res['msg'] = 'pdf文件'
        out = parsePDF(cur_file)
        res['status'] = out['status']
        res['data']['merge_image'] = f'http://localhost:5000/download?fileId=pdf.jpg'
        if out['msg'] != '-':
            res['msg'] = out['msg']
        if out['status'] > 0:
            res['data']['content'] = out['content']
        else:
            logger.error(f"pdf文档解析失败 {cur_file=} -> {out=}...")
    elif cur_ext in ('jpg', 'png', 'jpeg', 'tiff', 'bmp', 'gif'):
        # 调用ocr工具
        # res = some_function(cur_file)
        res['data']['content'] = ['ocr 文档内容']
        res['msg'] = '图片文件'
        out = parseOCR(cur_file)
        # 判断识别出来的文本质量, 语种检测非中文时, 重新生成
        detect_res = False # 判断是否中文
        if out['num'] > 0:
            tmp = langid.classify(','.join(out['content']))
            if tmp[0] == 'zh':
                detect_res = True
        if out['num'] == 0 or not detect_res:
            # print(f'二次检测, {out}')
            logger.warning('启动二次检测, 疑似手写体')
            # 启动中文手写体识别
            # out = parseOCR(cur_file, hand=True)
            out = parseOCRNew(cur_file)
        res['status'] = out['status']
        if out['msg'] != '-':
            res['msg'] = out['msg']
        if out['status'] > 0:
            res['data']['content'] = out['content'] if out['num'] > 0 else '[未识别到内容]'
            # 生成合成图
            if out['merge_image'] != '-':
                res['data']['merge_image'] = out['merge_image']
        else:
            res['data']['content'] = f'图片解析失败 {cur_file=} -> {out=}...'
            logger.error(f"图片解析失败 {cur_file=} -> {out=}...")
    else:
        res['data']['content'] = ['非预期格式']
        res['msg'] = '其它文件'
    print(f"请求参数: {data=}, {out=}, {res=}")
    # return res
    # return jsonify(res)
    return json.dumps(res, ensure_ascii=False)
    # return ';'.join(res['data']['content'])


if __name__ == '__main__':
    #app.run() # 本地访问：只能从自己的计算机上访问
    app.run(host='0.0.0.0', debug=True) # 外网可访问

