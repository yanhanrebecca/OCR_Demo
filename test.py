import os


def test_directory_and_file_operations(base_dir):
    picture_dir = os.path.join(base_dir, 'picture')
    unrecognized_dir = os.path.join(base_dir, 'unrecognized')

    # 创建目录
    if not os.path.exists(picture_dir):
        os.makedirs(picture_dir)
        print(f"创建目录: {picture_dir}")

    if not os.path.exists(unrecognized_dir):
        os.makedirs(unrecognized_dir)
        print(f"创建目录: {unrecognized_dir}")

    # 创建测试文件
    test_file_path = os.path.join(base_dir, 'test.jpg')
    with open(test_file_path, 'w') as f:
        f.write('This is a test file.')

    # 移动测试文件
    new_file_path = os.path.join(picture_dir, 'test.jpg')
    if not os.path.exists(new_file_path):
        os.rename(test_file_path, new_file_path)
        print(f"移动文件: {test_file_path} -> {new_file_path}")
    else:
        print(f"文件 {new_file_path} 已经存在，跳过。")


if __name__ == '__main__':
    base_directory = './result'
    test_directory_and_file_operations(base_directory)
