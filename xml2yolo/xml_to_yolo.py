# -*- coding: utf-8 -*-
# @Time    : 2021/6/10
# @Author  : chenyuming
# @Software: PyCharm
# @Brief   : 将xml格式的标注转换为yolo格式

import os
from PIL import Image, ImageDraw
from xml.dom.minidom import parse
import numpy as np


def cord_converter(size, box):
    """ 将标注的 xml 文件标注转换为 darknet 形的坐标
    :param size: 图片的尺寸： [w,h]
    :param box: anchor box 的坐标 [左上角x,左上角y,右下角x,右下角y,]
    :return: 转换后的 [x,y,w,h]
    """
    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    dw = np.float32(1. / int(size[0]))
    dh = np.float32(1. / int(size[1]))
    w = x2 - x1
    h = y2 - y1
    x = x1 + (w / 2)
    y = y1 + (h / 2)

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return [x, y, w, h]


def save_file(img_jpg_file_name, size, img_box):
    save_file_name = os.path.join(save_label_root, img_jpg_file_name + '.txt')
    print('save_file_name= ', save_file_name, 'size=', size)
    if int(size[0]) == 0 or int(size[1]) == 0:
        print('ERROR: [{}] is broken! '.format(save_file_name))
        return -1
    
    file_path = open(save_file_name, "a+")
    for box in img_box:

        # if box[0] == cls_names[0]: # person
        #     cls_num = 0
        # elif box[0] == cls_names[1]: # hat
        #     cls_num = 1
        # elif box[0] == cls_names[2]: # excavator
        #     cls_num = 2
        # elif box[0] ==cls_names[3]: # crane
        #     cls_num = 3
        # else:
        #     continue

        cls_num = cls_names.index(box[0])
        new_box = cord_converter(size, box[1:])

        file_path.write(f"{cls_num} {new_box[0]} {new_box[1]} {new_box[2]} {new_box[3]}\n")

    file_path.flush()
    file_path.close()
    return 0


def test_dataset_box_feature(file_name, point_array):
    """
    使用样本数据测试数据集的建议框
    :param image_name: 图片文件名
    :param point_array: 全部的点 [建议框sx1,sy1,sx2,sy2]
    :return: None
    """
    im = Image.open(f"{IMAGE_PATH}\{file_name}")
    imDraw = ImageDraw.Draw(im)
    for box in point_array:
        x1 = box[1]
        y1 = box[2]
        x2 = box[3]
        y2 = box[4]
        imDraw.rectangle((x1, y1, x2, y2), outline='red')

    im.show()


def get_xml_data(file_path, img_xml_file):
    img_path = file_path + '/' + img_xml_file + '.xml'
    print(img_path)

    dom = parse(img_path)
    root = dom.documentElement
    img_name = root.getElementsByTagName("filename")[0].childNodes[0].data
    img_size = root.getElementsByTagName("size")[0]
    objects = root.getElementsByTagName("object")
    img_w = img_size.getElementsByTagName("width")[0].childNodes[0].data
    img_h = img_size.getElementsByTagName("height")[0].childNodes[0].data
    img_c = img_size.getElementsByTagName("depth")[0].childNodes[0].data
    # print("img_name:", img_name)
    # print("image_info:(w,h,c)", img_w, img_h, img_c)
    img_box = []
    for box in objects:
        cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
        x1 = int(float(box.getElementsByTagName("xmin")[0].childNodes[0].data))
        y1 = int(float(box.getElementsByTagName("ymin")[0].childNodes[0].data))
        x2 = int(float(box.getElementsByTagName("xmax")[0].childNodes[0].data))
        y2 = int(float(box.getElementsByTagName("ymax")[0].childNodes[0].data))
        if cls_name not in cls_names:
            cls_names.append(cls_name)
            num_box_cls.append(1)
        else:
            num_box_cls[cls_names.index(cls_name)] += 1
        img_jpg_file_name = img_xml_file + '.jpg'
        img_box.append([cls_name, x1, y1, x2, y2])
    # print(img_box)
    # test_dataset_box_feature(img_jpg_file_name, img_box)
    save_file(img_xml_file, [img_w, img_h], img_box)


if __name__ == '__main__':
    IMAGE_PATH = '/home/cym/CYM/dataset/diaoche/diaoche/JPEGImages/'  # the diretary of images.
    annotations_path = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/Annotations/'  # the diretary of annotation files.
    save_label_root = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/Labels/'  # the diretary of saving the annotation files with yolo format. eg. xxx.txt

    # cls_names = ['person', 'hat', 'excavator', 'crane', 'forklift', 'elevator', 'smoke']
    cls_names = [ 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
         'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor' ]
    num_box_cls = [0] * len(cls_names)

    # step 1: xml转yolo格式的txt，并保存到Labels文件夹下。
    if os.path.exists(save_label_root) is False:
        os.mkdir(save_label_root)
    files = sorted(os.listdir(annotations_path))
    print('len(files)= ', len(files))
    for file in files:
        print("file name: ", file)
        file_xml = file.split(".")
        get_xml_data(annotations_path, file_xml[0])
        # break

    print(cls_names)
    print(num_box_cls)


