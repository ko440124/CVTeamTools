# -*- coding: utf-8 -*-
# @Time    : 2020/7/31 21:10
# @Author  : PeterH
# @Email   : peterhuang0323@outlook.com
# @File    : merge_data.py
# @Software: PyCharm
# @Brief   : 将自己的数据集使用 yolov5 检测出人体，合入自己数据集生成的安全帽标签
# 使用命令 python detect.py --save-txt --source 图片路径， 可以在 output 中看到每个图片的 txt 标签文件

import os
import numpy as np
import shutil
# train
# YOLOV5_LABEL_ROOT = "/home/cym/CYM/dataset/Safety_Helmet_Train_dataset_person/score/labels/trainval/"  # yolov5 导出的推理图片的 txt
# YOLOV5_IMAGE_ROOT = "/home/cym/CYM/dataset/Safety_Helmet_Train_dataset_person/score/images/trainval/"  # yolov5 导出的推理图片的 txt
# DATASET_LABEL_ROOT = "/home/cym/CYM/dataset/Safety_Tools_Train_dataset/score/labels/helmet/"  # 数据集的路径
# DATASET_IMAGE_ROOT = "/home/cym/CYM/dataset/Safety_Tools_Train_dataset/score/images/helmet/"  # 数据集的路径
# test
YOLOV5_LABEL_ROOT = "/home/cym/CYM/dataset/Safety_Helmet_Train_dataset_person/score/labels/test/"  # yolov5 导出的推理图片的 txt
YOLOV5_IMAGE_ROOT = "/home/cym/CYM/dataset/Safety_Helmet_Train_dataset_person/score/images/test/"  # yolov5 导出的推理图片的 txt
DATASET_LABEL_ROOT = "/home/cym/CYM/dataset/Safety_Tools_Train_dataset/score/labels/test_helmet/"  # 数据集的路径
DATASET_IMAGE_ROOT = "/home/cym/CYM/dataset/Safety_Tools_Train_dataset/score/images/test_helmet/"  # 数据集的路径


if __name__ == '__main__':
    print('finishing for copy helmet files......')
    yolo_file = np.array(sorted(os.listdir(YOLOV5_LABEL_ROOT)))

    # target_num = 1000
    target_num = 200
    total_num = len(yolo_file)
    print(total_num)
    total_index = np.random.permutation(total_num)
    target_idx = total_index[:target_num]
    
    yolo_file = yolo_file[target_idx]
    print(len(yolo_file))
    # 遍历文件里面有 .txt 结尾的
    for file_name in yolo_file:
        # 判断 txt 文件才进行读取
        if not file_name.endswith(".txt"):
            continue

        img_name = file_name.split('.')[0]+'.jpg'
        origin_img_path = YOLOV5_IMAGE_ROOT + img_name
        dest_img_path = DATASET_IMAGE_ROOT + img_name
        # print(origin_img_path)
        # print(dest_img_path)
        shutil.copyfile(origin_img_path, dest_img_path)

        file_path = YOLOV5_LABEL_ROOT + file_name
        with open(file_path, "r") as f:
            for line in f.readlines():

                # 只需要提取 0 -> person 的数据
                # if line.split()[0] != '0':
                #     continue

                data_path = DATASET_LABEL_ROOT + file_name
                # 汇总到数据集的标注文件
                with open(data_path, "a") as fd:
                    fd.write(line)
        # print(data_path)
    print('finished for copy helmet files!!!')
