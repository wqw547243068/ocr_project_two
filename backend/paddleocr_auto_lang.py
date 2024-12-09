
import langid

sen = [
    '纪念, fdsfd nfdsfd ',
    'fdsfd 纪念, nfdsfd ',
    '最好的纪念, fdsfd nfdsfd ',
    'К 534 при ',
    'TK BAA BAD! 292.4 РРР?. BX LRA} mW. ',
    'BOARDING PASS 航班 FLIGHT 日期 DATE 舱位 CLASS  序号 SERIAL NO.  座位号 “SEAT МО. MU 2379 03DEC    м    035      <目的地 T0   始发地 FROM [3       =         +'
]
for s in sen:
    tmp = langid.classify(s)
    print(s[:5], tmp)


# 语言检测 以下代码未调试通过
# pip install paddleclas
import paddleclas

# file_name = "E:\ocr\data\联合国宣言\中英.jpg"
# file_name = "E:\ocr\data\联合国宣言\德语.jpg"
# file_name = "E:\ocr\data\联合国宣言\日语.jpg"
# file_name = "E:\ocr\data\联合国宣言\法语.jpg"
# file_name = r"E:\ocr\data\hand\1.jpg"
file_name = r"E:\ocr\data\hand\3.jpg"
# file_name = r"E:\ocr\data\OCR_e2e_img\general_ocr_001.png"

lang_model = paddleclas.PaddleClas(model_name="language_classification")
result = lang_model.predict(input_data=file_name)
result = list(result)
lang_type = result[0][0]['label_names'][0]
print('语言类型为：',lang_type)

# RuntimeError: (NotFound) Cannot open file C:\Users\wqw/.paddleclas/inference_model\PULC\language_classification, please confirm whether the file is normal.
#   [Hint: Expected static_cast<bool>(fin.is_open()) == true, but received static_cast<bool>(fin.is_open()):0 != true:1.] (at ..\paddle\fluid\inference\api\analysis_predictor.cc:2577)