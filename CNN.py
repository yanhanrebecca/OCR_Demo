import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from PIL import Image
from scipy.spatial.distance import cosine

# 加载预训练的 ResNet18 模型
model = resnet18(pretrained=True)
model.eval()  # 设置为评估模式

# 定义图像预处理步骤
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_and_preprocess_image(img_path):
    """加载并预处理图像"""
    img = Image.open(img_path).convert('RGB')
    img_tensor = preprocess(img).unsqueeze(0)  # 增加批次维度
    return img_tensor

def extract_features(img_path):
    """提取图像特征"""
    img_tensor = load_and_preprocess_image(img_path)
    with torch.no_grad():
        features = model(img_tensor)
    return features.squeeze().numpy()  # 去掉批次维度

def calculate_similarity(features1, features2):
    """计算两个特征向量之间的相似度"""
    return 1 - cosine(features1, features2)

# 输入两个图像的路径
img_path1 = '10.jpg'
img_path2 = '9.jpg'

# 提取特征
features1 = extract_features(img_path1)
features2 = extract_features(img_path2)

# 计算相似度
similarity = calculate_similarity(features1, features2)

print(f'The similarity between the two images is: {similarity:.4f}')
