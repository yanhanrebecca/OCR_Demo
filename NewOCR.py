import os
from paddleocr import PaddleOCR
from PIL import Image
import cv2
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch') # 可根据需求选择语言

# 要处理的图像路径
image_path = 'result/68.jpg'

# 读取图像
image = Image.open(image_path)

# 进行OCR识别
result = ocr.ocr(image_path, cls=True)

# 创建保存剪裁后图像的目录
cropped_image_dir = 'result'
os.makedirs(cropped_image_dir, exist_ok=True)

for idx, line in enumerate(result):
    for box in line:
        # 获取文字区域的边界框和识别出的文字
        text = box[1][0]
        box_coords = box[0]

        # 根据边界框计算最小外接矩形
        points = np.array(box_coords, dtype=np.int32)
        rect = cv2.boundingRect(points)
        x_min, y_min, w, h = rect
        x_max = x_min + w
        y_max = y_min + h

        # 剪裁图像
        cropped_image = image.crop((x_min, y_min, x_max, y_max))

        # 使用文字和索引作为文件名
        cropped_image_path = os.path.join(cropped_image_dir, f'{text}_{idx}.png')
        cropped_image.save(cropped_image_path)

print('图像剪裁和命名完成')