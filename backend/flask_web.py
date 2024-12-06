import os
import json
import logging
from flask import Flask, request, jsonify, render_template

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

from docx import Document
import pdfplumber
import pytesseract


cache_dir = 'tmp'
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)

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
        for page in pdf.pages:
            content_info['content'].append(page.extract_text())
        content_info['status'] = 1
        content_info['msg'] = 'pdf解析完毕'
    except Exception as err:
        # logging.error(f"pdf文档解析失败 {file_name} ...")
        content_info['status'] = -1
        content_info['msg'] = err
    return content_info


def parseOCR(file_name):
    """
        图片OCR: tesseract
    """
    content_info = {"num": 0, "content":[], "status":0, "msg":'-'}
    # 读取文档
    try:
        out = pytesseract.image_to_string(file_name, lang='chi_sim+eng+deu+fra+rus+jpn')
        out = out.split('\n')
        content_info['num'] = len(out)
        content_info['content'] = out
        content_info['status'] = 1
        content_info['msg'] = '图片OCR解析完毕'
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

@app.route('/api_ocr', methods = ["GET", "POST"])
def post_data():
    # 获取客户端的文件信息
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
    elif request.method == 'GET':
        data = request.args
        cur_file = data['uploadFile']
    
    logger.info(f"请求参数: {data=}, {cur_file=}")
    res = {"status":0, 
            "msg":'-', 
            "data":{
                "content":[], # 识别内容
                "merge_image":"-", # 融合图
                "scores":[], # 分值
            }, 
            'req':{} # 请求信息
    }
    
    if not os.path.exists(cur_file):
        res['status'] = -1
        res['msg'] = f"文件{cur_file}不存在"
        logger.error(res['msg'])
        return json.dumps(res, ensure_ascii=False)

    res['req']['file_name'] = cur_file
    if cur_file.find('.') != -1:
        cur_ext = cur_file.split('.')[-1]
    else:
        cur_ext = '-'
    cur_ext = cur_ext.lower()
    res['data']['file_type'] = cur_ext
    print(f"请求参数: {data=}, {cur_file=}, {cur_ext=}")
    # 格式检测
    if cur_ext in ('doc', 'docx'): # word 文档, 直接解析
        res['data']['content'] = ['word 文档内容']
        res['msg'] = 'word文件'
        out = parseDoc(cur_file)
        res['status'] = out['status']
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
        res['status'] = out['status']
        if out['msg'] != '-':
            res['msg'] = out['msg']
        if out['status'] > 0:
            res['data']['content'] = out['content']
            # 生成合成图
            res['data']['merge_image'] = '-'
            pass
        else:
            logger.error(f"图片解析失败 {cur_file=} -> {out=}...")
    else:
        res['data']['content'] = ['非预期格式']
        res['msg'] = '其它文件'
    print(f"[debug] {res}")
    # return res
    # return jsonify(res)
    return json.dumps(res, ensure_ascii=False)
    # return ';'.join(res['data']['content'])


if __name__ == '__main__':
    #app.run() # 本地访问：只能从自己的计算机上访问
    app.run(host='0.0.0.0', debug=True) # 外网可访问

