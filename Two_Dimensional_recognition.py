import os
import glob
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 提取图像中的轮廓
def extract_contours(image):
    # 将图像转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用二值化处理
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # 查找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# 获取轮廓的边界框
def get_bounding_box(contours):
    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    return x, y, w, h

# 获取笔画的方向
def get_stroke_directions(contours):
    directions = []
    for contour in contours:
        if len(contour) > 1:
            # 拟合轮廓点的直线
            [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
            angle = np.arctan2(vy, vx) * 180 / np.pi
            directions.append(angle)
    return directions

# 绘制轮廓并显示
def plot_contours(image, contours, title):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    for contour in contours:
        contour = contour.reshape(-1, 2)  # 重新调整形状为 (N, 2)
        plt.plot(contour[:, 0], contour[:, 1], marker='o')
    plt.show()

# 读取指定文件夹中的图像文件
def read(base_folder):
    image_files = []
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)

        if os.path.isdir(folder_path):
            print(f"处理文件夹: {folder_name}")
            image_files.extend(glob.glob(os.path.join(folder_path, '*.jpg')))
    return image_files

# 处理图像并标注信息
def process_image(image_file, font_path):
    image = Image.open(image_file)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    np_image = np.array(image)
    gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建带有透明度的叠加图像
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype(font_path, size=20)
    except IOError:
        print("字体文件未找到或无法打开。")
        font = ImageFont.load_default()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # 在叠加图像上用指定颜色和透明度绘制轮廓
        overlay_draw.rectangle([x, y, x + w, y + h], outline='green', width=2)

        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            overlay_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill='rgba(255,0,0,128)')  # 红色带透明度
            overlay_draw.text((cx + 10, cy), '重心', font=font, fill='rgba(255,0,0,128)')

        # 标注轮廓的大小信息
        size_text = f'宽: {w} 高: {h}'
        overlay_draw.text((x, y - 20), size_text, font=font, fill='rgba(0,255,0,128)')  # 绿色带透明度

        # 计算轮廓的角度
        sz = len(cnt)
        data_pts = np.empty((sz, 2), dtype=np.float64)
        for i in range(sz):
            data_pts[i] = [cnt[i, 0, 0], cnt[i, 0, 1]]

        mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean=np.empty((0)))
        angle = np.arctan2(eigenvectors[0, 1], eigenvectors[0, 0])
        angle_degrees = np.degrees(angle)

        overlay_draw.text((x, y - 40), f'角度: {angle_degrees:.2f} 度', font=font, fill='rgba(0,0,255,128)')  # 蓝色带透明度

    # 将原始图像转换为RGBA以允许透明度
    image = image.convert('RGBA')

    # 将原始图像与叠加图像合成
    combined = Image.alpha_composite(image, overlay)

    # 保存输出图像
    output_path = os.path.splitext(image_file)[0] + '_annotated.png'  # 保存为PNG以保留透明度
    combined.save(output_path)
    print(f"已保存标注图像: {output_path}")

# 主函数
def main():
    base_folder = r'./result\Test'
    font_path = r'D:\Download\SimHei.ttf'  # 替换为你的字体文件路径
    image_files = read(base_folder)
    for image_file in image_files:
        process_image(image_file, font_path)
        # 使用 Pillow 读取图像
        image_pil = Image.open(image_file)

        # 将 Pillow 图像转换为 NumPy 数组
        image_np = np.array(image_pil)

        # 如果需要将图像从 RGB 转换为 BGR（OpenCV 使用的颜色空间）
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # 现在你可以继续使用 OpenCV 进行处理
        contours1 = extract_contours(image_bgr)
        x1, y1, w1, h1 = get_bounding_box(contours1)
        directions1 = get_stroke_directions(contours1)
        print(f"字符 1 的边界框: x={x1}, y={y1}, 宽={w1}, 高={h1}")
        print(f"字符 1 的笔画方向: {directions1}")
        plot_contours(image_bgr, contours1, "contours1")


if __name__ == "__main__":
    main()
