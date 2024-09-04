import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def mark_strokes(image_path):
    # 读取图像
    abs_image_path = os.path.abspath(image_path)
    with open(abs_image_path, 'rb') as f:
        image_array = np.asarray(bytearray(f.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        print(f"无法加载图像: {image_path}")
        return  # 如果图像读取失败，直接返回

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    lines = cv2.HoughLinesP(edges_dilated, 1, np.pi / 180, threshold=60, minLineLength=5, maxLineGap=5)
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if abs(angle) < 30:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            elif abs(angle) > 80:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            elif 30 <= angle <= 80:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            elif -80 <= angle <= -30:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 255), 3)

    result_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    plt.imshow(result_image_rgb)
    plt.axis('off')
    plt.show()


def read(base_folder):
    image_files = []
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            print(f"处理文件夹: {folder_name}")
            image_files.extend(glob.glob(os.path.join(folder_path, '*.jpg')))
    return image_files


base_folder = r'./result/Test'
image_files = read(base_folder)
for image_file in image_files:
    if not os.path.isfile(image_file):
        print(f"文件不存在: {image_file}")
    else:
        mark_strokes(image_file)