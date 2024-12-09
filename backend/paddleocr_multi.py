# -*- coding: utf-8 -*-

import logging
from queue import Queue
import os
import sys
import threading
import json
from paddleocr import PaddleOCR

# file_name = "E:\ocr\data\联合国宣言\中英.jpg"
# file_name = "E:\ocr\data\联合国宣言\德语.jpg"
# file_name = "E:\ocr\data\联合国宣言\日语.jpg"
# file_name = "E:\ocr\data\联合国宣言\法语.jpg"
file_name = r"E:\ocr\data\hand\1.jpg"
# file_name = r"E:\ocr\data\hand\3.jpg"
# file_name = r"E:\ocr\data\OCR_e2e_img\general_ocr_001.png"
# file_name = r"E:\ocr\data\多国语言-1205\日文\1.jpeg"

languages = ['ch', 'en', 'japan', 'fr', 'de']  # 需要支持的语言列表

# 模型初始化
api_info = {}
for lang in languages:
    api_info[lang] = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)


def log(msg):
    pid = os.getpid()
    tid = threading.current_thread().ident
    logging.info(f"进程[{pid}]-线程[{tid}]: {msg}")

# 多种返回结果: 空、一个识别结果、多个识别结果
# [null]
#  [[
#     [[[1931.0, 1453.0], [1990.0, 1453.0], [1990.0, 1487.0], [1931.0, 1487.0]], ["191t", 0.7493318915367126]]
#  ]]
# [[
#     [[[297.0, 157.0], [1755.0, 124.0], [1760.0, 337.0], [301.0, 370.0]], ["很多人不需要再见!", 0.9498765468597412]], 
#     [[[351.0, 493.0], [1773.0, 468.0], [1776.0, 657.0], [354.0, 683.0]], ["因为只是路过而已.", 0.8729634881019592]], 
#     [[[334.0, 833.0], [1755.0, 842.0], [1753.0, 1049.0], [333.0, 1039.0]], ["遗忘就是我给你", 0.9973150491714478]], 
#     [[[404.0, 1153.0], [1457.0, 1182.0], [1450.0, 1434.0], [397.0, 1404.0]], ["最好的纪念。", 0.951411783695221]], 
#     [[[1935.0, 1460.0], [1988.0, 1460.0], [1988.0, 1485.0], [1935.0, 1485.0]], ["19楼", 0.9435752034187317]]
# ]]

def getResult(lock, lang, q):
    """
        单次 OCR 请求
    """
    log('开始请求OCR服务')
    # 开始请求OCR服务
    result = api_info[lang].ocr(file_name)
    lock.acquire()
    score_avg = 0
    if not result[0]:
        pass
    else:
        # 计算平均得分
        score_list = [i[1][1] for i in result[0]]
        score_avg = sum(score_list)/len(score_list)
        print(f'[Note] {lang=}: \t{score_avg}\t{json.dumps([i[1][0] for i in result[0]], ensure_ascii=False)}')
    lock.release()
    q.put([lang, score_avg, result[0]])
    log('请求完毕')


if __name__ == '__main__':

    thread_lock = threading.Lock()
    
    job_list = []
    q = Queue() # 存储结果

    for lang in languages:
        job = threading.Thread(target=getResult, args=(thread_lock, lang, q), name=f'job_{lang}')
        job.start()
        job_list.append(job)
    
    # 阻塞在主进程前面
    for thread in job_list:
        thread.join()
    
    results = []
    for _ in languages:
        # [lang, score_avg, result[0]]
        results.append(q.get())

    # # 根据置信度选择最佳结果
    best_result = max(results, key=lambda x: x[1])
    print(f"最佳语言: {best_result[0]}, 得分: {best_result[1]}, 结果: {best_result[2]}")

    text = '\n'.join([i[1][0] for i in best_result[2]])
    print('Result: ', json.dumps(text, ensure_ascii=False))

sys.exit(1)

# 顺序依次请求

result_info = {}
max_lang = ['-', 0]
stop = False
MIN_VAL = 0.85

for lang in languages:
    ocr = PaddleOCR(use_angle_cls=True, lang=lang)
    result = ocr.ocr(file_name)
    if not result[0]:
        result_info[lang] = result
        continue
    # 计算平均得分
    score_list = [i[1][1] for i in result[0]]
    score_avg = sum(score_list)/len(score_list)
    print(f'[Note] {lang=}: \t{score_avg}\t{json.dumps([i[1][0] for i in result[0]], ensure_ascii=False)}')
    if score_avg > max_lang[1]:
        max_lang = [lang, score_avg]
    result_info[lang] = result[0]
    if score_avg > MIN_VAL:
        # 置信度较高, 终止检测
        stop = True
        print(f'[Note] 置信度较高 {score_avg:.2f}>{MIN_VAL}, 提前终止 ... 已检测语种: {result_info.keys()}')
        break

print(f'语种: {max_lang[0]}, 得分: {max_lang[1]}, 结果: {result_info[lang]}')

