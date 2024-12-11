
import os
from paddleocr import PaddleOCR, draw_ocr

# 设置识别语言为中文，可以根据需要调整
ocr = PaddleOCR(use_gpu=False, lang='ch')

# 指定PDF文件所在的文件夹路径
pdf_folder = 'pdfs'
# 遍历文件夹中的所有PDF文件
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        # 读取PDF文件内容
        with open(os.path.join(pdf_folder, filename), 'rb') as f:
            pdf_content = f.read()
        # 进行文字识别
        result = ocr.ocr(pdf_content, use_gpu=False)
        # 在终端中输出识别结果
        for line in result:
            line_text = ' '.join([word_info[-1] for word_info in line])
            print(line_text)
        # 可选：将识别结果保存到文件中，方便后续处理和分析
        # with open(os.path.join(pdf_folder, 'output', filename + '.txt'), 'w', encoding='utf-8') as f:
        #     f.write(''.join([line_text for line in result]))