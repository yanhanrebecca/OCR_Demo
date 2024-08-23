from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob

def read(base_folder):
    image_files = []
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)

        if os.path.isdir(folder_path):
            print(f"处理文件夹: {folder_name}")
            image_files.extend(glob.glob(os.path.join(folder_path, '*.jpg')))
    return image_files

base_folder = r'D:\Work\ExtractionProJ\OCR_Demo\result\Test'
# 读取图片并转换为灰度图

color_thickness = (0, 255, 0)  # 绿色表示笔画粗细
color_depth = (255, 0, 0)      # 红色表示笔画深浅
color_std_dev = (0, 0, 255)    # 蓝色表示灰度变化
contour_color = (255, 255, 0)  # 黄色用于画轮廓



image_files = read(base_folder)
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
        img_draw.text((center_x, center_y - 30), f'Thickness: {thickness}', fill=color_thickness, font=font)

        # 标注笔画深浅（灰度）
        img_draw.text((center_x, center_y), f'Depth: {depth:.2f}', fill=128, font=font)

        # 标注灰度变化（灰度）
        img_draw.text((center_x, center_y + 30), f'Std Dev: {std_dev:.2f}', fill=128, font=font)

        # 画轮廓（灰度）
        contour_points = [(pt[0][0], pt[0][1]) for pt in contour]
        img_draw.line(contour_points, fill=255, width=2)

    # 显示标注后的图片
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()
