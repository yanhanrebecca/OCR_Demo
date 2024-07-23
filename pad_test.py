import os
import cv2
import numpy as np
import subprocess
import os

HIOG = 50
VIOG = 3
Position = []

'''水平投影'''


def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 获取图像大小
    (h, w) = image.shape
    # 统计像素个数
    h_ = [0] * h
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8)
    (h, w) = image.shape
    w_ = [0] * w
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1
    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255
    return w_


def scan(vProjection, iog, pos=0):
    start = 0
    V_start = []
    V_end = []

    for i in range(len(vProjection)):
        if vProjection[i] > iog and start == 0:
            V_start.append(i)
            start = 1
        if vProjection[i] <= iog and start == 1:
            if i - V_start[-1] < pos:
                continue
            V_end.append(i)
            start = 0
    return V_start, V_end


def checkSingle(image):
    h = getHProjection(image)
    start = 0
    end = 0

    for i in range(h):
        pass


# 分割
def CropImage(image, dest, boxMin, boxMax):
    a = boxMin[1]
    b = boxMax[1]
    c = boxMin[0]
    d = boxMax[0]
    cropImg = image[a:b, c:d]
    cv2.imwrite(dest, cropImg)


# 开始识别
def DOIT(rawPic, save_directory):
    # 读入原始图像
    origineImage = cv2.imread(rawPic)
    # 图像灰度化
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)

    # 将图片二值化
    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    (h, w) = img.shape
    # 垂直投影
    V = getVProjection(img)

    start = 0
    V_start = []
    V_end = []

    # 对垂直投影水平分割
    V_start, V_end = scan(V, HIOG)
    if len(V_start) > len(V_end):
        V_end.append(w - 5)

    # 分割行，分割之后再进行列分割并保存分割位置
    for i in range(len(V_end)):
        # 获取行图像
        if V_end[i] - V_start[i] < 30:
            continue

        cropImg = img[0:h, V_start[i]:V_end[i]]
        H = getHProjection(cropImg)
        H_start, H_end = scan(H, VIOG, 40)

        if len(H_start) > len(H_end):
            H_end.append(h - 5)

        for pos in range(len(H_start)):
            # 再进行一次列扫描
            DcropImg = cropImg[H_start[pos]:H_end[pos], 0:w]
            d_h, d_w = DcropImg.shape
            sec_V = getVProjection(DcropImg)
            c1, c2 = scan(sec_V, 0)
            if len(c1) > len(c2):
                c2.append(d_w)

            x = 1
            while x < len(c1):
                if c1[x] - c2[x - 1] < 12:
                    c2.pop(x - 1)
                    c1.pop(x)
                    x -= 1
                x += 1

            if len(c1) == 1:
                Position.append([V_start[i], H_start[pos], V_end[i], H_end[pos]])
            else:
                for x in range(len(c1)):
                    Position.append([V_start[i] + c1[x], H_start[pos], V_start[i] + c2[x], H_end[pos]])

    # 根据确定的位置分割字符
    number = 0
    for m in range(len(Position)):
        rectMin = (Position[m][0] - 5, Position[m][1] - 5)
        rectMax = (Position[m][2] + 5, Position[m][3] + 5)
        cv2.rectangle(origineImage, rectMin, rectMax, (0, 0, 255), 2)
        number += 1
        # 保存裁剪后的图像到指定目录
        crop_path = os.path.join(save_directory, f'{number}.jpg')
        CropImage(origineImage, crop_path, rectMin, rectMax)


    result_image_path = os.path.join(save_directory, 'ResultImage.jpg')
    cv2.imwrite(result_image_path, origineImage)
    cv2.waitKey(1)


# 执行命令，但不会捕获输出
# exit_status = os.system('paddleocr --image_dir ./2.jpg --use_angle_cls true --use_gpu false | tee out.txt')

# 注意：这里无法直接获取命令的输出

# # 打开out.txt文件以读取内容
# with open('out.txt', 'r', encoding='utf-8') as file:
#     # 逐行读取文件
#     for line in file:
#         # 去除每行末尾的换行符（如果有的话）
#         line = line.rstrip('\n')
#         # 处理每一行（这里只是打印出来）
#         print(line)
#         # 或者你可以在这里添加其他处理逻辑
#         # 例如，分析文本、存储到数据库等

def ocr(image_dir):
    # 使用PaddleOCR进行图片中文本的识别


    # 获取指定目录下所有文件名
    files = os.listdir(image_dir)

    # 遍历每个文件
    for file in files:
        # 拼接文件的完整路径
        file_path = os.path.join(image_dir, file)
        print("-----------------------------------------------------------")
        print("正在识别：{}".format(file))
        # 检查文件是否是jpg格式
        if file.lower().endswith('.jpg'):
            pad_ocr(file_path)

def pad_ocr(file_path):
    command = ['paddleocr', '--image_dir', file_path, '--use_angle_cls', 'true', '--use_gpu', 'false']

    # 执行命令并捕获输出
    result = subprocess.run(command, capture_output=True, text=True)

    # 检查命令是否成功执行
    if result.returncode == 0:
        print("识别成功。")
        output_lines = result.stdout.splitlines()

        # 打印或处理命令的标准输出的最后一行
        if output_lines:
            last_line = output_lines[-1]
            # print("命令输出的最后一行:")
            # print(last_line)
            word = process_log(last_line)
            print("{}图片是识别出的文字是{}".format(file_path, word))

            # 将最后一行输出到文件中
            with open('out.txt', 'w') as f:
                f.write(word)
        else:
            print("命令没有输出任何内容。")
    else:
        print("命令执行失败。")
        # 打印或处理命令的错误输出
        print("错误输出:")
        print(result.stderr)

def process_log(log_string):
    start_index = log_string.find('(')
    if start_index != -1:
        # 截取左括号后面的内容
        content_after_bracket = log_string[start_index + 1:]
        # 找到逗号的位置，即找到左括号后面的内容的结束位置
        end_index = content_after_bracket.find(',')
        if end_index != -1:
            # 提取找到的字符
            found_character = content_after_bracket[:end_index].strip()

            # 输出结果
    #         print("找到的字符:", found_character)
    #     else:
    #         print("未找到逗号，无法提取右边的字符。")
    # else:
    #     print("未找到左括号，无法提取右边的字符。")
    return found_character

if __name__ == '__main__':
    # 设置保存目录为D盘某个路径
    save_directory = r'./result'
    # 确保保存目录存在
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # 示例
    rawPicPath = r"./2.jpg"
    print("开始图片处理")
    DOIT(rawPicPath, save_directory)
    print("图片处理完毕")
    image_dir = './result'
    ocr(image_dir)
