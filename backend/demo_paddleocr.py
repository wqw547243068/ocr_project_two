# !/usr/bin/env python
# -*- coding:gbk -*- 

# **************************************************************************
# * Copyright (c) 2024. All Rights Reserved
# **************************************************************************
# * @function OCR Demo, PaddleOCR 实现, windows 环境
# * @author wqw547243068@163.com
# * @date 2024/12/07 17:00
# **************************************************************************

import sys
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order


# file_name = "E:\ocr\data\联合国宣言\中英.jpg"
# file_name = "E:\ocr\data\联合国宣言\德语.jpg"
# file_name = "E:\ocr\data\联合国宣言\日语.jpg"
# file_name = "E:\ocr\data\联合国宣言\法语.jpg"
# file_name = r"E:\ocr\data\hand\1.jpg"
file_name = r"E:\ocr\data\hand\3.jpg"
# file_name = r"E:\ocr\data\OCR_e2e_img\general_ocr_001.png"

# # 语言检测 以下代码未调试通过
# # pip install paddleclas
# import paddleclas
# lang_model = paddleclas.PaddleClas(model_name="language_classification")
# result = lang_model.predict(input_data=file_name)
# result = list(result)
# lang_type = result[0][0]['label_names'][0]
# print('语言类型为：',lang_type)


# 初始化, 首次执行会自动下载模型文件
# 语种选择: ['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari']
# ocr = PaddleOCR(use_angle_cls=True) # 默认ch 中文+英文
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
# ocr = PaddleOCR(use_angle_cls=True, lang='japan') # 不支持一次指定多种语言
# ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False, det=True, rec=True, cls=True)
# 指定手写体
# handwriting_ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det_model_dir='handwriting_det', rec_model_dir='handwriting_rec')

# 开始识别，传入参数 file_name 可以是文件名+numpy, 如 Image.open(img_path)
result = ocr.ocr(file_name, cls=True) # 方向分类器
# result = ocr.ocr(file_name, det=False) # 每个item只有文本内容和置信度
# result = ocr.ocr(file_name, cls=True, det=False) # 不需要文本框，每个item只有文本内容和置信度
# result = ocr.ocr(file_name, cls=True, rec=False) # 不需要文本内容，每个item只有文本框
# result = ocr.ocr(file_name, cls=True, rec=False, det=False) #  仅执行方向分类器, 返回分类结果+置信度


print(f'{result=}')
# 格式: [文本框, [文字, 置信度]]
# [[[24.0, 36.0], [304.0, 34.0], [304.0, 72.0], [24.0, 74.0]], ['纯臻营养护发素', 0.964739]]
# [[[24.0, 80.0], [172.0, 80.0], [172.0, 104.0], [24.0, 104.0]], ['产品信息/参数', 0.98069626]]
# [[[24.0, 109.0], [333.0, 109.0], [333.0, 136.0], [24.0, 136.0]], ['（45元/每公斤，100公斤起订）', 0.9676722]]


for idx in range(len(result)):
    res = result[idx]
    if not res:
        continue
    for line in res:
        print(line)

if not result and not result[0]:
    print(f'结果为空: {result}')
    sys.exit(1)

# draw result
from PIL import Image

result = result[0]
image = Image.open(file_name).convert('RGB')
boxes, txts, scores = [], [], []
for line in result:
    if not line:
        continue
    boxes.append(line[0])
    txts.append(line[1][0])
    scores.append(line[1][1])

im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
im_show.show('result.jpg')
