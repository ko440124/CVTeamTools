import numpy as np
import os
import random
import glob
import argparse
from shutil import copyfile
from pathlib import Path


def split_train_test(train_radio=0.9):
    '''
    split the dataset to trainset and testset according to the train_radio.
    And saving train.txt and test.txt into root+'Main'.
    '''
    img_list = np.array(sorted(glob.glob(root+'Labels/**.txt')))
    total_num = len(img_list)
    for i in range(total_num):
        line = img_list[i]
        line = line.split('/')[-1]
        line = line.split('.')[0]
        img_list[i] = line+'\n'

    np.random.seed(1024)
    select_index = np.random.permutation(total_num)

    train_num = int(train_radio*len(select_index))
    test_num = len(select_index) - train_num
    train_idx = select_index[:train_num]
    test_idx = select_index[train_num:]

    train_img_list = img_list[train_idx]
    test_img_list = img_list[test_idx]

    with open(root+'yolo/Main/train.txt', 'w') as f:
        f.writelines((train_img_list))
    with open(root+'yolo/Main/test.txt', 'w') as f:
        f.writelines(test_img_list)
    print('train:[{}] test:[{}]'.format(train_num, test_num))
    print(len(train_idx), len(test_idx))


def copy_data(img_set_source, img_labels_root, imgs_source, type):
    file_name = img_set_source + '/' + type + ".txt"
    print('file_name: ', file_name)
    file = open(file_name)

    # 判断文件夹是否存在，不存在则创建
    root_file = Path(DEST_IMAGES_PATH + '/' + type)
    if not root_file.exists():
        print(f"Path {root_file} is not exit")
        os.makedirs(root_file)

    root_file = Path(DEST_LABELS_PATH + '/' + type)
    if not root_file.exists():
        print(f"Path {root_file} is not exit")
        os.makedirs(root_file)

    # 遍历文件夹
    for line in file.readlines():
        # print(line)
        img_name = line.strip('\n')
        img_sor_file = imgs_source + '/' + img_name + '.jpg'
        label_sor_file = img_labels_root + '/' + img_name + '.txt'

        # 复制图片
        DICT_DIR = DEST_IMAGES_PATH + '/' + type
        img_dict_file = DICT_DIR + '/' + img_name + '.jpg'
        try:
            copyfile(img_sor_file, img_dict_file)
        except:
            img_sor_file = imgs_source + '/' + img_name + '.JPG'
            copyfile(img_sor_file, img_dict_file)
        # 复制 label
        DICT_DIR = DEST_LABELS_PATH + '/' + type
        img_dict_file = DICT_DIR + '/' + img_name + '.txt'
        copyfile(label_sor_file, img_dict_file)

        # print('label_dict_file: ', img_dict_file)

    print('###############[{}]: The end of copying##############'.format(type))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--root', type==str, default='', help='the root path of dataset')
    # args = parser.parse_args()
    root = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/'
    split_train_test(train_radio=0.9)

    print('\n############################################\n')
    # step 2：根据txt文件，划分train和val，并生成train.txt和test.txt
    # 代码见：split_train_test.py
    # step 3：根据 train.txt和 test.txt，将图像和txt复制到对应的文件夹
    DEST_IMAGES_PATH = "/home/cym/CYM/dataset/VOCdevkit/VOC2007/yolo/images"  # 区分训练集、测试集、验证集的图片目标路径
    DEST_LABELS_PATH = "/home/cym/CYM/dataset/VOCdevkit/VOC2007/yolo/labels"  # 区分训练集、测试集、验证集的标签文件目标路径
    img_labels_root = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/Labels/'
    img_set_root = os.path.join(root, 'yolo/Main/')
    imgs_root = os.path.join(root, 'JPEGImages/')

    copy_data(img_set_root, img_labels_root, imgs_root, "train")
    copy_data(img_set_root, img_labels_root, imgs_root, "val")
    copy_data(img_set_root, img_labels_root, imgs_root, "test")