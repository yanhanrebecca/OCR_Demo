import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 全局变量
dragging = False
ix, iy = -1, -1
tx, ty = 0, 0

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
        else:
            print(f"Warning: Cannot read image {img_path}")
    return images

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    return binary

def resize_image(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

def manual_align(base_image, image_to_align):
    global dragging, ix, iy, tx, ty
    tx, ty = 0, 0  # 重置平移量
    scale_x, scale_y = 1.0, 1.0  # 初始化水平和垂直缩放比例
    angle = 0  # 初始化旋转角度

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

    # 创建并调整窗口大小
    cv2.namedWindow('Align', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Align', 800, 800)  # 设置窗口尺寸为 800x800
    cv2.setMouseCallback('Align', on_mouse)

    while True:
        combined_image = base_image.copy()
        rows, cols = image_to_align.shape

        # 创建旋转矩阵
        center = (cols // 2, rows // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)  # 旋转角度 angle

        # 应用旋转变换到图像
        rotated_image = cv2.warpAffine(image_to_align, rotation_matrix, (cols, rows))

        # 应用平移和缩放
        M = np.float32([[scale_x, 0, tx], [0, scale_y, ty]])
        moved_image = cv2.warpAffine(rotated_image, M, (cols, rows))

        # 显示组合后的图像
        combined_image = cv2.addWeighted(combined_image, 0.5, moved_image, 0.5, 0)
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
        elif key == ord('e'):  # 按 'e' 键顺时针旋转
            angle += 1
        elif key == ord('r'):  # 按 'r' 键逆时针旋转
            angle -= 1

    cv2.destroyAllWindows()
    return moved_image

def generate_heatmap(image_list, mode='original'):
    base_image = preprocess_image(resize_image(image_list[0], (500, 500)))
    heatmap = np.zeros_like(base_image, dtype=np.float32)

    # 设置初始对齐基准为处理后的第一张图片
    current_base_image = base_image

    for img in image_list:
        preprocessed_img = preprocess_image(resize_image(img, (500, 500)))
        if mode == 'manual':
            # 将当前图片与已经对齐好的基准图片对齐
            aligned_image = manual_align(current_base_image, preprocessed_img)
            current_base_image = aligned_image  # 将对齐后的图片作为下一张图片的基准
        else:
            aligned_image = preprocessed_img
        heatmap += aligned_image.astype(np.float32)

    heatmap /= len(image_list)
    heatmap = (heatmap / heatmap.max() * 255).astype(np.uint8)
    return heatmap

def save_heatmap(heatmap, folder_name):
    # 创建保存路径
    save_folder = os.path.join('./result/ChongDie', folder_name)
    os.makedirs(save_folder, exist_ok=True)

    # 保存为文件
    heatmap_path = os.path.join(save_folder, 'heatmap.png')
    cv2.imwrite(heatmap_path, heatmap)
    print(f"Heatmap saved at: {heatmap_path}")

def display_heatmap(heatmap):
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()

# 示例使用
folder_path = './result/Test/V'
output_folder_name = 'V_processed'

images = load_images_from_folder(folder_path)
if images:
    heatmap = generate_heatmap(images, mode='manual')  # 可以选择 'original' 或 'manual'
    save_heatmap(heatmap, output_folder_name)  # 保存结果
    display_heatmap(heatmap)  # 显示热图
else:
    print("No images found in the specified folder.")
