import cv2
import numpy as np
import matplotlib.pyplot as plt

def mark_horizontal_vertical_lines_advanced(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 形态学操作增强线条
    kernel = np.ones((5, 5), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # 霍夫变换检测线条
    lines = cv2.HoughLinesP(edges_dilated, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    # 创建一个空白图像用于绘制线条
    line_image = np.zeros_like(image)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # 判断横向和纵向
            if abs(x2 - x1) > abs(y2 - y1):
                # 横向线条
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 红色
            else:
                # 纵向线条
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # 蓝色

    # 将线条叠加到原始图像上
    result_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)

    # 转换颜色通道以适应 matplotlib
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

    # 使用 matplotlib 显示图像
    plt.imshow(result_image_rgb)
    plt.axis('off')  # 关闭坐标轴
    plt.show()

# 使用示例
mark_horizontal_vertical_lines_advanced('6.jpg')
