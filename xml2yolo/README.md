#### xml2yolo
##### 将voc格式数据，转为yolo格式。
step 1. 修改相应的文件路径以及类别
```python
cls_names = [...]
IMAGE_PATH = '/home/cym/CYM/dataset/diaoche/diaoche/JPEGImages/'  # the diretary of images.
annotations_path = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/Annotations/'  # the diretary of annotation files.
save_label_root = '/home/cym/CYM/dataset/VOCdevkit/VOC2007/Labels/'  # the diretary of saving the annotation files with yolo format. eg. xxx.txt
```
step 2. 执行命令
```python
python xml_to_yolo.py
```

