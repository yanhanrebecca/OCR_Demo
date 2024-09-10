import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 全局变量
dragging = False
ix, iy = -1, -1
tx, ty = 0, 0


# 从路径加载图片
def load_images_from_paths(path1, path2):
    images = []
    for file_path in [path1, path2]:
        img = cv2.imread(file_path)
        if img is not None:
            images.append(img)
        else:
            print(f"Warning: Cannot read image {file_path}")
    return images


# 预处理图像
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    return binary


# 改变图像大小
def resize_image(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


# 手动对齐函数
def manual_align(base_image, image_to_align):
    global dragging, ix, iy, tx, ty
    tx, ty = 0, 0  # 重置平移量
    scale_x, scale_y = 1.0, 1.0  # 初始化水平和垂直缩放比例

    def on_mouse(event, x, y, flags, param):
        global dragging, ix, iy, tx, ty
        if event == cv2.EVENT_LBUTTONDOWN:
            dragging = True
            ix, iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if dragging:
                tx += x - ix
                ty += y - iy
                ix, iy = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            dragging = False

    cv2.namedWindow('Align', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Align', 800, 800)
    cv2.setMouseCallback('Align', on_mouse)

    while True:
        combined_image = base_image.copy()
        rows, cols = image_to_align.shape
        # 调整大小和平移
        M = np.float32([[scale_x, 0, tx], [0, scale_y, ty]])
        moved_image = cv2.warpAffine(image_to_align, M, (cols, rows))

        # 增加对比度，让字体更清晰
        alpha = 0.7  # 基础图像的权重
        beta = 0.3  # 移动图像的权重
        gamma = 0  # 亮度偏移量
        combined_image = cv2.addWeighted(combined_image, alpha, moved_image, beta, gamma)

        # 更改字体颜色为白色并使用黑色背景
        cv2.putText(combined_image, 'Aligning...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)

        cv2.imshow('Align', combined_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 按 'q' 键退出
            break
        elif key == ord('w'):  # 按 'w' 键增加垂直缩放比例
            scale_y += 0.01
        elif key == ord('s'):  # 按 's' 键减少垂直缩放比例
            scale_y = max(0.01, scale_y - 0.01)
        elif key == ord('a'):  # 按 'a' 键减少水平方向的缩放比例
            scale_x = max(0.01, scale_x - 0.01)
        elif key == ord('d'):  # 按 'd' 键增加水平方向的缩放比例
            scale_x += 0.01

    cv2.destroyAllWindows()
    return moved_image


# 生成热图
def generate_heatmap(image_list, mode='original'):
    base_image = preprocess_image(resize_image(image_list[0], (500, 500)))
    heatmap = np.zeros_like(base_image, dtype=np.float32)

    for img in image_list:
        preprocessed_img = preprocess_image(resize_image(img, (500, 500)))
        if mode == 'manual':
            aligned_image = manual_align(base_image, preprocessed_img)
        else:
            aligned_image = preprocessed_img
        heatmap += aligned_image.astype(np.float32)

    heatmap /= len(image_list)
    heatmap = (heatmap / heatmap.max() * 255).astype(np.uint8)
    return heatmap


# 显示热图
def display_heatmap(heatmap):
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()

# 示例使用
# 手动输入图片路径
image_path1 = '7.jpg'
image_path2 = '10.jpg'

images = load_images_from_paths(image_path1, image_path2)
if len(images) == 2:
    heatmap = generate_heatmap(images, mode='manual')  # 使用前两张图片，可以选择 'original' 或 'manual'
    display_heatmap(heatmap)
else:
    print("Please ensure both image paths are correct.")