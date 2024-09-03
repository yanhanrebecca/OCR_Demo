import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import feature
from matplotlib import font_manager
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path).convert('L')  # 转换为灰度图
        images.append(np.array(img))
    return images

def compute_mean_and_std(images):
    all_pixels = np.concatenate([img.flatten() for img in images])
    mean = np.mean(all_pixels)
    std = np.std(all_pixels)
    return mean, std

def compute_edge_density(image):
    edges = feature.canny(image)
    return np.sum(edges) / np.prod(image.shape)

def compute_image_statistics(images):
    means = []
    stds = []
    edge_densities = []

    for img in images:
        mean = np.mean(img)
        std = np.std(img)
        edge_density = compute_edge_density(img)

        means.append(mean)
        stds.append(std)
        edge_densities.append(edge_density)

    mean_all, std_all = compute_mean_and_std(images)
    std_edge_density_all = np.std(edge_densities)  # 计算边缘密度的标准差

    return means, stds, edge_densities, mean_all, std_all, std_edge_density_all

def plot_results(images, means, stds, edge_densities, mean_all, std_all, std_edge_density_all):
    # 配置中文字体
    font_path = r'D:\Download\SimHei.ttf'  # 确保字体路径正确
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
    plt.rcParams['axes.unicode_minus'] = False

    fig, axs = plt.subplots(2, 3, figsize=(18, 12))

    # 绘制灰度值直方图
    axs[0, 0].hist(np.concatenate([img.flatten() for img in images]), bins=20, alpha=0.5, color='green', edgecolor='black', linewidth=1.5)
    axs[0, 0].set_title('灰度值直方图', fontproperties=font_prop)

    # 绘制均值与平均值的差异
    axs[0, 1].bar(range(len(means)), [mean - mean_all for mean in means])
    axs[0, 1].set_title('灰度均值差异', fontproperties=font_prop)

    # 绘制标准差与平均标准差的差异
    axs[0, 2].bar(range(len(stds)), [std - std_all for std in stds])
    axs[0, 2].set_title('灰度标准差差异', fontproperties=font_prop)

    # 绘制边缘密度直方图
    axs[1, 0].hist(edge_densities, bins=20, alpha=0.5, color='green', edgecolor='black', linewidth=1.5)
    axs[1, 0].set_title('边缘密度直方图', fontproperties=font_prop)

    # 绘制边缘密度均值与平均均值的差异
    axs[1, 1].bar(range(len(edge_densities)), [density - np.mean(edge_densities) for density in edge_densities])
    axs[1, 1].set_title('边缘密度均值差异', fontproperties=font_prop)

    # 绘制边缘密度标准差差异
    axs[1, 2].bar(range(len(edge_densities)), [density - std_edge_density_all for density in edge_densities])
    axs[1, 2].set_title('边缘密度标准差差异', fontproperties=font_prop)

    # 添加标注
    axs[0, 0].text(0.5, -0.15, '图1: 灰度值变化', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[0, 0].transAxes)
    axs[0, 1].text(0.5, -0.15, '图2: 灰度均值差异', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[0, 1].transAxes)
    axs[0, 2].text(0.5, -0.15, '图3: 灰度标准差差异', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[0, 2].transAxes)
    axs[1, 0].text(0.5, -0.15, '图4: 边缘密度变化', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[1, 0].transAxes)
    axs[1, 1].text(0.5, -0.15, '图5: 边缘密度均值差异', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[1, 1].transAxes)
    axs[1, 2].text(0.5, -0.15, '图6: 边缘密度标准差差异', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=axs[1, 2].transAxes)

    plt.tight_layout()
    plt.show()

# 使用示例
folder = './result/Test/T'
images = load_images_from_folder(folder)
means, stds, edge_densities, mean_all, std_all, std_edge_density_all = compute_image_statistics(images)
plot_results(images, means, stds, edge_densities, mean_all, std_all, std_edge_density_all)

