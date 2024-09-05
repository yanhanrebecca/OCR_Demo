from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
from PIL import Image
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# 初始化 OCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 进行 OCR 识别
image_path = '5.jpg'
result = ocr.ocr(image_path, cls=True)

# 提取识别出的文本
extracted_text = ''
for line in result:
    for word_info in line:
        extracted_text += word_info[1][0]

print("识别出的文本:", extracted_text)

# 可视化识别结果
image = Image.open(image_path).convert('RGB')
boxes = [elements[0] for elements in result[0]]
txts = [elements[1][0] for elements in result[0]]
scores = [elements[1][1] for elements in result[0]]

# 显示结果
im_show = draw_ocr(image, boxes, txts, scores)
plt.imshow(im_show)
plt.show()

# 假设有一个笔顺字典
stroke_order_dict = {
    '你': '笔顺信息',
    '好': '笔顺信息',
    # 添加更多字符和笔顺信息
}

# 获取每个字符的笔顺
def get_stroke_order(text, stroke_order_dict):
    stroke_orders = {}
    for char in text:
        if char in stroke_order_dict:
            stroke_orders[char] = stroke_order_dict[char]
        else:
            stroke_orders[char] = '未知笔顺'
    return stroke_orders

# 示例使用
stroke_orders = get_stroke_order(extracted_text, stroke_order_dict)
for char, order in stroke_orders.items():
    print(f"字符: {char}, 笔顺: {order}")