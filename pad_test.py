import os
import cv2
import numpy as np
import subprocess

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
HIOG = 50
VIOG = 3
Position = []

'''水平投影'''


def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    (h, w) = image.shape
    h_ = [0] * h
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
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


def CropImage(image, dest, boxMin, boxMax):
    a = boxMin[1]
    b = boxMax[1]
    c = boxMin[0]
    d = boxMax[0]
    cropImg = image[a:b, c:d]
    cv2.imwrite(dest, cropImg)


def DOIT(rawPic, save_directory):
    origineImage = cv2.imread(rawPic)
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)

    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    (h, w) = img.shape
    V = getVProjection(img)

    V_start, V_end = scan(V, HIOG)
    if len(V_start) > len(V_end):
        V_end.append(w - 5)

    for i in range(len(V_end)):
        if V_end[i] - V_start[i] < 30:
            continue

        cropImg = img[0:h, V_start[i]:V_end[i]]
        H = getHProjection(cropImg)
        H_start, H_end = scan(H, VIOG, 40)

        if len(H_start) > len(H_end):
            H_end.append(h - 5)

        for pos in range(len(H_start)):
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

    number = 0
    for m in range(len(Position)):
        rectMin = (Position[m][0] - 5, Position[m][1] - 5)
        rectMax = (Position[m][2] + 5, Position[m][3] + 5)
        cv2.rectangle(origineImage, rectMin, rectMax, (0, 0, 255), 2)
        number += 1
        crop_path = os.path.join(save_directory, f'{number}.jpg')
        CropImage(origineImage, crop_path, rectMin, rectMax)

    result_image_path = os.path.join(save_directory, 'ResultImage.jpg')
    cv2.imwrite(result_image_path, origineImage)
    cv2.waitKey(1)


def ocr(image_dir):
    picture_dir = os.path.join(image_dir, 'picture')
    unrecognized_dir = os.path.join(image_dir, 'unrecognized')
    if not os.path.exists(picture_dir):
        os.makedirs(picture_dir)
    if not os.path.exists(unrecognized_dir):
        os.makedirs(unrecognized_dir)

    files = os.listdir(image_dir)

    for file in files:
        file_path = os.path.join(image_dir, file)
        if file.lower().endswith('.jpg'):
            print("-----------------------------------------------------------")
            print("正在识别：{}".format(file))
            pad_ocr(file_path, picture_dir, unrecognized_dir)


def pad_ocr(file_path, picture_dir, unrecognized_dir):
    command = ['paddleocr', '--image_dir', file_path, '--use_angle_cls', 'true', '--use_gpu', 'false']

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("识别成功。")
        output = result.stdout
        if output is not None:
            output_lines = output.splitlines()
            if output_lines:
                last_line = output_lines[-1]
                word = process_log(last_line)
                word = word.replace("'", "")  # 去掉单引号
                print("{}图片是识别出的文字是{}".format(file_path, word))

                if word:
                    word_folder = os.path.join(picture_dir, word)
                    if not os.path.exists(word_folder):
                        os.makedirs(word_folder)

                    # 将识别出的字保存到对应的文件夹中
                    txt_path = os.path.join(word_folder, f'{word}.txt')
                    with open(txt_path, 'w') as f:
                        f.write(word)

                    # 移动原始图片到对应的文件夹中
                    move_file(file_path, word_folder)
                else:
                    move_file(file_path, unrecognized_dir)
            else:
                print("命令没有输出任何内容。")
                move_file(file_path, unrecognized_dir)
        else:
            print("标准输出是 None。")
            move_file(file_path, unrecognized_dir)
    else:
        print("命令执行失败。")
        print("错误输出:")
        print(result.stderr)
        move_file(file_path, unrecognized_dir)


def move_file(file_path, target_dir, word=None):
    # 如果目标文件已存在，重命名源文件以避免冲突
    if word:
        target_dir = os.path.join(target_dir, word)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
    base_name = os.path.basename(file_path)
    target_path = os.path.join(target_dir, base_name)
    if os.path.exists(target_path):
        # 文件已存在，添加一个后缀以避免冲突
        name, ext = os.path.splitext(base_name)
        counter = 1
        while os.path.exists(target_path):
            new_name = f"{name}_{counter}{ext}"
            target_path = os.path.join(target_dir, new_name)
            counter += 1
    os.rename(file_path, target_path)


def process_log(log_string):
    start_index = log_string.find('(')
    if start_index != -1:
        content_after_bracket = log_string[start_index + 1:]
        end_index = content_after_bracket.find(',')
        if end_index != -1:
            found_character = content_after_bracket[:end_index].strip()
            return found_character
    return ""


if __name__ == '__main__':
    save_directory = r'./result'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    rawPicPath = 'D:/Work/ExtractionProJ/OCR_Demo/2.jpg'
    print("开始图片处理")
    DOIT(rawPicPath, save_directory)
    print("图片处理完毕")
    image_dir = './result'
    ocr(image_dir)
