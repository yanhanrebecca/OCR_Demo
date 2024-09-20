from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob

# 函数读取指定文件夹中的图片
def read(folder):
    # 只读取当前文件夹下的所有jpg图片
    image_files = glob.glob(os.path.join(folder, '*.jpg'))
    return image_files

# 指定文件夹路径
base_folder = r'./result/Test/T'
output_folder = r'./result/threeDimension'  # 输出文件夹

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 颜色定义
color_thickness = (0, 255, 0)  # 绿色表示笔画粗细
color_depth = (255, 0, 0)      # 红色表示笔画深浅
color_std_dev = (0, 0, 255)    # 蓝色表示灰度变化
contour_color = (255, 255, 0)  # 黄色用于画轮廓

# 读取图片列表
image_files = read(base_folder)

# 创建处理结果存放的文件夹（与输入文件夹同名）
output_subfolder = os.path.join(output_folder, os.path.basename(base_folder))
if not os.path.exists(output_subfolder):
    os.makedirs(output_subfolder)

for image_file in image_files:
    img = Image.open(image_file).convert('RGB')
    gray = img.convert('L')  # 转换为灰度图

    # 将灰度图转换为numpy数组
    gray_np = np.array(gray)

    # 二值化
    _, binary = cv2.threshold(gray_np, 150, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 将PIL图像转换为可编辑的绘图对象
    img_draw = ImageDraw.Draw(img)

    # 加载字体（确保字体路径正确）
    font = ImageFont.truetype("D:\Download\SimHei.ttf", 20)

    # 遍历所有轮廓并计算笔画粗细、深浅和灰度变化
    for contour in contours:
        # 计算最小外接矩形
        x, y, w, h = cv2.boundingRect(contour)

        # 粗细估计为外接矩形的最小边长
        thickness = min(w, h)

        # 计算轮廓区域的平均灰度值和标准差
        mask = np.zeros(gray_np.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=-1)
        mean_intensity = cv2.mean(gray_np, mask=mask)[0]
        std_dev = np.std(gray_np[mask == 255])

        # 将平均灰度值转换为深浅值（较低的灰度值表示较深的笔画）
        depth = 255 - mean_intensity

        # 在笔画中心位置标注粗细值、深浅值和灰度变化
        center_x, center_y = x + w // 2, y + h // 2

        # 标注笔画粗细（绿色）
        img_draw.text((center_x, center_y - 30), f'粗细: {thickness}', fill=color_thickness, font=font)

        # 标注笔画深浅（红色）
        img_draw.text((center_x, center_y), f'深度: {depth:.2f}', fill=color_depth, font=font)

        # 标注灰度变化（蓝色）
        img_draw.text((center_x, center_y + 30), f'灰度变化: {std_dev:.2f}', fill=color_std_dev, font=font)

        # 画轮廓（黄色）
        cv2.drawContours(gray_np, [contour], -1, contour_color, 2)

    # 获取图片文件名
    file_name = os.path.basename(image_file)

    # 保存处理后的图片到统一的输出子文件夹中
    output_path = os.path.join(output_subfolder, file_name)
    img.save(output_path)

    # 显示标注后的图片
    plt.imshow(img)
    plt.axis('off')
    plt.show()
