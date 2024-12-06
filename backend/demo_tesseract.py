# coding:utf-8

import sys
import cv2                        # OpenCV: Computer vision and image manipulation package
import pytesseract                # python Tesseract: OCR in python
import matplotlib.pyplot as plt   # plotting
import numpy as np                # Numpy for arrays
from PIL import Image             # Pillow: helps us read remote images
import requests                   # Requests: to fetch remote URLs
from io import BytesIO            # Helps read remote images

def get_image(url):
    if url.startswith('http://'): # ÍøÂçÎÄ¼þ
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    else: # ±¾µØÎÄ¼þ
        img = Image.open(url)
        #img = cv2.imread(url)
    return img

file_name = "E:\ocr\data\联合国宣言\中英.jpg"
# file_name = "E:\ocr\data\联合国宣言\俄语.jpg"
file_name = "E:\ocr\data\联合国宣言\德语.jpg"
file_name = "E:\ocr\data\联合国宣言\日语.jpg"
file_name = "E:\ocr\data\联合国宣言\法语.jpg"
# file_name = "E:\ocr\data\hand\\2.jpg"
# file_name = "E:\ocr\data\hand\\4.png"
# file_name = "e:\ocr\data\OCR_e2e_img\general_ocr_001.png"
#img = get_image('https://github.com/jalammar/jalammar.github.io/raw/master/notebooks/cv/label.png')
#img = get_image('e:\\code_new\\ocr\\data\\a.png')
img = get_image(file_name)
print(f"文件名: {file_name=}")
# OCR 识别
# res = pytesseract.image_to_string(img) # 默认英语
if file_name.find('hand') != -1:
    print('手写体')
    res = pytesseract.image_to_string(img, lang='chi_sim') # 中文
else:
    # res = pytesseract.image_to_string(img, lang='chi_sim+eng') # 中英
    # res = pytesseract.image_to_string(img, lang='chi_sim+eng+deu+fra+rus+jpn')
    res = pytesseract.image_to_string(img, lang='fra')

print("识别结果: ", res)


# sys.exit(1)

print('='*30)

import numpy as np
import pytesseract
from pytesseract import Output
import cv2

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image
    
img = cv2.imread(file_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

width_list = []
for c in cnts:
    _, _, w, _ = cv2.boundingRect(c)
    width_list.append(w)
wm = np.median(width_list)

tess_text = pytesseract.image_to_data(img, output_type=Output.DICT, lang='chi_sim')
for i in range(len(tess_text['text'])):
    word_len = len(tess_text['text'][i])
    if word_len > 1:
        world_w = int(wm * word_len)
        (x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
        cv2.rectangle(img, (x, y), (x + world_w, y + h), (255, 0, 0), 1)
        im = Image.fromarray(img)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
        draw.text((x, y - 20), tess_text['text'][i], (0, 255, 0), font=font)
        img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

cv2.imshow("TextBoundingBoxes", img)
cv2.waitKey(0)
