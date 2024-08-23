import os
import shutil
from collections import defaultdict


def extract_chinese_characters(s):
    """提取字符串中所有汉字字符"""
    return ''.join([c for c in s if '\u4e00' <= c <= '\u9fff'])


def has_common_chars(chars1, chars2):
    """检查两个字符串是否有共同的汉字字符"""
    set1 = set(chars1)
    set2 = set(chars2)
    return not set1.isdisjoint(set2)


def find_folders_with_common_chars(src_dir):
    """找出文件夹名称中有共同汉字字符的文件夹"""
    folder_names = os.listdir(src_dir)
    print(f"Found folders: {folder_names}")  # 调试信息

    folder_paths = [os.path.join(src_dir, name) for name in folder_names if os.path.isdir(os.path.join(src_dir, name))]
    print(f"Folder paths: {folder_paths}")  # 调试信息

    folder_chars = {}
    for folder_path in folder_paths:
        folder_name = os.path.basename(folder_path)
        chars = extract_chinese_characters(folder_name)
        print(f"Folder: {folder_name}, Extracted chars: {chars}")  # 调试信息
        folder_chars[folder_path] = chars

    common_char_folders = []
    checked_folders = set()

    for folder_path1, chars1 in folder_chars.items():
        if folder_path1 in checked_folders:
            continue

        for folder_path2, chars2 in folder_chars.items():
            if folder_path1 != folder_path2 and folder_path2 not in checked_folders:
                if has_common_chars(chars1, chars2):
                    common_char_folders.append((folder_path1, folder_path2))
                    checked_folders.add(folder_path1)
                    checked_folders.add(folder_path2)

    if not common_char_folders:
        print("No folders with common characters found.")

    return common_char_folders


def copy_images_from_folders(folder_pairs, dest_dir):
    """从具有共同字符的文件夹中复制图片到目标文件夹"""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if not folder_pairs:
        print("No source directories provided for copying images.")
        return

    for folder1, folder2 in folder_pairs:
        combined_folder_name = f"{os.path.basename(folder1)}_{os.path.basename(folder2)}"
        new_folder_path = os.path.join(dest_dir, combined_folder_name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        print(f"Processing folder pair: '{folder1}' and '{folder2}'")

        for folder in [folder1, folder2]:
            if not os.path.exists(folder):
                print(f"Source directory '{folder}' does not exist.")
                continue

            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    shutil.copy(file_path, new_folder_path)
                    print(f"Copied {file_name} from '{folder}' to '{new_folder_path}'.")
        print(f"Finished copying images from '{folder1}' and '{folder2}'.")


if __name__ == "__main__":
    # 当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 图片文件夹路径
    picture_dir = r'.\result\picture'

    # 匹配文件夹路径
    match_dir = os.path.join(current_dir, 'result', 'match')

    # 查找具有共同汉字字符的文件夹
    folder_pairs_with_common_chars = find_folders_with_common_chars(picture_dir)

    # 复制图片文件到匹配文件夹
    copy_images_from_folders(folder_pairs_with_common_chars, match_dir)

    print("Finished processing images.")
