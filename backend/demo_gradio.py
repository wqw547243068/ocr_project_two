# !/usr/bin/env python
# -*- coding:utf8 -*- 

# **************************************************************************
# * Copyright (c) 2024 ke.com, Inc. All Rights Reserved
# **************************************************************************
# * @function OCR Demo, easyOCR+Gradio实现, windows 环境
# * @author wqw547243068@163.com
# * @date 2024/12/05 17:00
# **************************************************************************


import os
import gradio as gr  # gradio==4.20.0

os.environ['FLAGS_allocator_strategy'] = 'auto_growth'
import random
import math
import cv2
import logging
import numpy as np
import json
import time
import PIL
from PIL import Image, ImageDraw, ImageFont
# from tools.infer_e2e import OpenOCR, check_and_download_font, draw_ocr_box_txt
# from OpenOCR.tools.infer.utility import get_rotate_crop_image, get_minarea_rect_crop, draw_ocr_box_txt

drop_score = 0.01
# text_sys = OpenOCR(drop_score=drop_score)
# # warm up 5 times
# if True:
#     img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
#     for i in range(5):
#         res = text_sys(img_numpy=img)
# font_path = './simfang.ttf'
font_path = "C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc"
# check_and_download_font(font_path)

def list_image_paths(directory):
    """
        遍历目录下所有图片文件路径
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    image_paths = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                relative_path = os.path.relpath(os.path.join(root, file),
                                                directory)
                full_path = os.path.join(directory, relative_path)
                image_paths.append(full_path)

    return image_paths

# 演示文件目录
demo_dir = "E:\ocr\data\OCR_e2e_img"
e2e_img_example = list_image_paths(demo_dir)


def create_font(txt, sz, font_path=font_path):
    font_size = int(sz[1] * 0.99)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    if int(PIL.__version__.split(".")[0]) < 10:
        length = font.getsize(txt)[0]
    else:
        length = font.getlength(txt)

    if length > sz[0]:
        font_size = int(font_size * sz[0] / length)
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    return font

def draw_box_txt_fine(img_size, box, txt, font_path=font_path):
    box_height = int(
        math.sqrt((box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    )
    box_width = int(
        math.sqrt((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2)
    )

    if box_height > 2 * box_width and box_height > 30:
        img_text = Image.new("RGB", (box_height, box_width), (255, 255, 255))
        draw_text = ImageDraw.Draw(img_text)
        if txt:
            font = create_font(txt, (box_height, box_width), font_path)
            draw_text.text([0, 0], txt, fill=(0, 0, 0), font=font)
        img_text = img_text.transpose(Image.ROTATE_270)
    else:
        img_text = Image.new("RGB", (box_width, box_height), (255, 255, 255))
        draw_text = ImageDraw.Draw(img_text)
        if txt:
            font = create_font(txt, (box_width, box_height), font_path)
            draw_text.text([0, 0], txt, fill=(0, 0, 0), font=font)

    pts1 = np.float32(
        [[0, 0], [box_width, 0], [box_width, box_height], [0, box_height]]
    )
    pts2 = np.array(box, dtype=np.float32)
    M = cv2.getPerspectiveTransform(pts1, pts2)

    img_text = np.array(img_text, dtype=np.uint8)
    img_right_text = cv2.warpPerspective(
        img_text,
        M,
        img_size,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )
    return img_right_text

def draw_ocr_box_txt(
    image,
    boxes,
    txts=None,
    scores=None,
    drop_score=0.5,
    font_path=font_path,
):
    h, w = image.height, image.width
    img_left = image.copy()
    img_right = np.ones((h, w, 3), dtype=np.uint8) * 255
    random.seed(0)

    draw_left = ImageDraw.Draw(img_left)
    if txts is None or len(txts) != len(boxes):
        txts = [None] * len(boxes)
    for idx, (box, txt) in enumerate(zip(boxes, txts)):
        if scores is not None and scores[idx] < drop_score:
            continue
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if isinstance(box[0], list):
            box = list(map(tuple, box))
        draw_left.polygon(box, fill=color)
        img_right_text = draw_box_txt_fine((w, h), box, txt, font_path)
        pts = np.array(box, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img_right_text, [pts], True, color, 1)
        img_right = cv2.bitwise_and(img_right, img_right_text)
    img_left = Image.blend(image, img_left, 0.5)
    img_show = Image.new("RGB", (w * 2, h), (255, 255, 255))
    img_show.paste(img_left, (0, 0, w, h))
    img_show.paste(Image.fromarray(img_right), (w, 0, w * 2, h))
    return np.array(img_show)

# pip install easyocr

import easyocr

# test_file = 'e:\\code_new\\ocr\\data\\a.png' # 中文
#test_file = 'e:\\code_new\\ocr\\data\\b.jpg' # 英文
test_file = f"{demo_dir}\general_ocr_001.png"

logging.info('OCR Tool 初始化 ...')
# 语种模型加载，只下载、加载一次，到内存里
reader = easyocr.Reader(['ch_sim','en']) 
# reader = easyocr.Reader(['ch_sim','en', 'de', 'fr', 'ja']) # this needs to run only once to load the model into memory
# result = reader.readtext(test_file) # list 结构，包含解析内容及对应的box区域、置信度
# ([[86, 80], [134, 80], [134, 128], [86, 128]], '西', 0.40452659130096436)
# result = reader.readtext(test_file, detail=0) # list 结构, 只显示解析出的文本内容
# print(f'临时测试 {result=}')


def main(input_image):
    """
        主函数
    """
    logging.info('文件格式检测 ...')
    if len(input_image) == 0:
        logging.error(f'待检测文件为空 {input_image=} ...')
        return '输入文件为空', 0, None
    img = input_image[:, :, ::-1]
    # starttime = time.time()
    # # results, time_dict, mask = text_sys(img_numpy=img, return_mask=True)
    # results, time_dict, mask = None, None, None, 
    # elapse = time.time() - starttime
    # save_pred = json.dumps(results[0], ensure_ascii=False)
    # image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # boxes = [res['points'] for res in results[0]]
    # txts = [res['transcription'] for res in results[0]]
    # scores = [res['score'] for res in results[0]]
    
    # img = Image.open(input_image)
    start_time = time.time()
    results = reader.readtext(input_image, detail=0)
    results = reader.readtext(input_image, paragraph="False")

    end_time = time.time()
    elapse = end_time - start_time
    logging.info(f'检测耗时: {elapse=} = {start_time=} -> {end_time=}')
    # ([[86, 80], [134, 80], [134, 128], [86, 128]], '西', 0.40452659130096436)
    # 输出结果后处理
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 文本段落自适应聚合
    boxes, texts, scores = [],[],[]
    text_str_list = [] # 文本聚合
    # 文本段落自适应聚合
    for res in results:
        if len(res) < 3:
            logging.error(f"识别结果格式有误 {res}")
            continue
        cur_box, cur_text, cur_score = res
        boxes.append(cur_box)
        texts.append(cur_text)
        scores.append(cur_score)
        # 差5个像素以内的文本，合并成一行 
        if text_str_list and len(boxes) > 1 and cur_box[0][1] - boxes[-2][0][1] < 5:
            text_str_list[-1] += f',{cur_text}'
        else:
            text_str_list.append(cur_text)
    save_pred = '\n'.join(text_str_list)
    # print(f'聚合结果:  \n{save_pred}')
    # 绘制效果图
    draw_img = draw_ocr_box_txt(
        image,
        boxes,
        texts,
        scores,
        drop_score=drop_score,
        font_path=font_path,
    )
    # mask = mask[0, 0, :, :] > 0.3
    # return save_pred, elapse, draw_img, mask.astype('uint8') * 255
    return save_pred, elapse, draw_img

def find_file_in_current_dir_and_subdirs(file_name):
    for root, dirs, files in os.walk('.'):
        if file_name in files:
            relative_path = os.path.join(root, file_name)
            return relative_path


if __name__ == '__main__':
    logging.info("Web DEMO 启动 ")
    css = '.image-container img { width: 100%; max-height: 320px;}'

    # file_upload = gr.File(label="上传文件", file_types=['application/pdf', 'text/plain', 'application/msword'])

    with gr.Blocks(css=css) as demo:
        gr.HTML("""
                <h1 style='text-align: center;'>OCR 离线识别 Demo</h1>""")
        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(label='输入图片',
                                       elem_classes=['image-container'])

                examples = gr.Examples(examples=e2e_img_example,
                                       inputs=input_image,
                                       label='示例')
                downstream = gr.Button('开始识别')

            with gr.Column(scale=1):
                # img_mask = gr.Image(label='mask',
                #                     interactive=False,
                #                     elem_classes=['image-container'])
                img_output = gr.Image(label='输出效果',
                                      interactive=False,
                                      elem_classes=['image-container'])

                confidence = gr.Textbox(label='置信度')
                output = gr.Textbox(label='识别结果')
                

            downstream.click(fn=main,
                             inputs=[input_image,],
                             outputs=[output,confidence,img_output,
                                 # img_mask,
                             ])

    # demo.launch(share=True)
    demo.launch(debug=True, share=True, server_name="0.0.0.0", server_port=9000)