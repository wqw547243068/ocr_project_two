# coding:utf-8
# pip install easyocr

import time
import easyocr
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import matplotlib.pyplot as plt

demo_dir = "E:\ocr\data"
test_file = f"{demo_dir}\a.png" # 中文
#test_file = 'e:\\code_new\\ocr\\data\\b.jpg' # 英文
test_file = f"{demo_dir}\OCR_e2e_img\general_ocr_001.png"

# 语种模型加载，只下载、加载一次，到内存里
# reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
reader = easyocr.Reader(['en', 'de', 'fr', 'ja', 'ru'])
# reader = easyocr.Reader(['ch_sim','en'], gpu=False)

start_time = time.time()
results = reader.readtext(test_file) # list 结构，包含解析内容及对应的box区域、置信度
# ([[86, 80], [134, 80], [134, 128], [86, 128]], '西', 0.40452659130096436)
# result = reader.readtext(test_file, detail=0) # list 结构, 只显示解析出的文本内容
results1 = reader.readtext(test_file, paragraph=False)
end_time = time.time()

cost_time = end_time - start_time
print(f"运行时间: {cost_time:.2f} s")
print(f'OCR结果:  {results=}')
print(f'OCR结果: 段落模式, {results1=}')

# 结果融合
font = cv2.FONT_HERSHEY_SIMPLEX
# font = ImageFont.truetype("simsun.ttf", 40, encoding="utf-8")

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("STSONG.TTF", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

img = cv2.imread(test_file)
# 单行
# img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
# img = cv2.putText(img,text,bottom_right, font, 0.5,(0,255,0),2,cv2.LINE_AA)
# 多行
spacer = 100
for detection in results: 
    top_left = tuple(detection[0][0])
    bottom_right = tuple(detection[0][2])
    text = detection[1]
    img = cv2.rectangle(img,top_left, bottom_right,(0,255,0),3)
    # cv2 直接显示中文会乱码
    #img = cv2.putText(img,text,(20,spacer), font, 0.5,(0,255,0),2,cv2.LINE_AA)
    img = cv2ImgAddText(img, text, bottom_right[0], bottom_right[0], (0, 255, 0), 30)
    spacer+=15

plt.figure(figsize=(10,10))
plt.imshow(img)
plt.show()


# 文本段落自适应聚合
boxes, texts, scores = [],[],[]
text_str_list = [] # 文本聚合
for res in results:
    if len(res) < 3:
        logging.error(f"识别结果格式有误 {res}")
        continue
    print(res)
    cur_box, cur_text, cur_score = res
    boxes.append(cur_box)
    texts.append(cur_text)
    scores.append(cur_score)
    if len(boxes) > 1:
        # print(f"{cur_box[0][1]} - {boxes[-2][0][1]}")
        pass
    if text_str_list and len(boxes) > 1 and cur_box[0][1] - boxes[-2][0][1] < 5:
        text_str_list[-1] += f',{cur_text}'
    else:
        text_str_list.append(cur_text)
merge_text = '\n'.join(text_str_list)
print(f'聚合结果:  \n{merge_text}')

