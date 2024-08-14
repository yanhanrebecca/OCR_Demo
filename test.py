from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # use_angle_cls=True for angle classification

# 识别图片1中的签名
result1 = ocr.ocr('8.jpg', cls=True)
signature_texts = [line[1][0] for line in result1[0]]  # 提取图片1中的签名文本

# 识别图片2中的文本
result2 = ocr.ocr('7.jpg', cls=True)

# 遍历图片2中的识别结果
for line in result2[0]:
    text = line[1][0]
    if any(signature_text in text for signature_text in signature_texts):
        # 找到匹配的文本区域，裁剪签名区域
        box = np.array(line[0], dtype=np.int32)  # 提取文本框坐标
        image2 = Image.open('7.jpg')
        cropped_image = image2.crop((box[0][0], box[0][1], box[2][0], box[2][1]))
        cropped_image.save('cropped_signature.jpg')
        break
