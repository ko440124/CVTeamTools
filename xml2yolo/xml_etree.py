import xml.etree.ElementTree as et
import xml.etree as etree
import cv2
import glob
def get_xml_annotation(xml_path, img_path):  
    img_name = img_path.split('/')[-1]
    new_tree_root = et.Element('annotation')
    
    xml_tree = et.ElementTree()
    xml_tree.parse(xml_path)
    root= xml_tree.getroot()
    
    filename = xml_tree.find('filename')
#     filename.text = img_name 
    new_tree_root.append(filename)
    
    if img_path.split('/')[-1].split('.')[0] != xml_path.split('/')[-1].split('.')[0] or img_path.split('/')[-1] != filename.text:
        print(img_path)
        print(xml_path)
        print(filename.text)
#         return 
    
    source = et.SubElement(root, 'source')
    database = et.SubElement(source, 'database')
    database.text = 'PASCAL: safety tools of substation'
    new_tree_root.append(source)
    
    img = cv2.imread(img_path)
    shape = img.shape # (height, width, channel)
#     print(shape)
    size = et.SubElement(root, 'size')
    width = et.SubElement(size, 'width')
    width.text = str(shape[1])
    height = et.SubElement(size, 'height')
    height.text = str(shape[0])
    depth = et.SubElement(size, 'depth')
    depth.text = str(shape[2])
    new_tree_root.append(size)
    
    
    objects = xml_tree.findall('object')
    num_obj = len(objects)
#     print('num_obj=', num_obj)
    for i in range(num_obj):
        obj = objects[i]
        label = obj.find('label')
        cls_name = label.text
        obj.remove(label)
        name = et.SubElement(obj, 'name')
        name.text = cls_name
        pose = et.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        difficult = et.SubElement(obj, 'difficult')
        difficult.text = str(0)
        truncated = et.SubElement(obj, 'truncated')
        truncated.text = str(0)
        new_tree_root.append(obj)
    t = et.ElementTree(new_tree_root)
    
    save_path = '/home/cym/桌面/图像标注/原图/ESR-F/Annotaions_from_iden/'+img_name.split('.')[0]+'.xml'
    t.write(save_path, xml_declaration=False, encoding='utf-8')

if __name__ == "__main__":
    xml_dir = '/home/cym/CYM/dataset/变电站安监/第一批交付成果/图像标注/标注/ESR-F-XML（验电操作-负样本）\
    /identification cards（标识牌）/'
    img_dir = '/home/cym/桌面/图像标注/原图/ESR-F/ESR-F/'

    xml_paths = sorted(glob.glob(xml_dir+'**.xml'))
    img_paths = sorted(glob.glob(img_dir+'**.jpg'))
    print(len(xml_paths))
    print(len(img_paths))
    for i in range(len(xml_paths)):
        xml_path = xml_paths[i]
        img_path = img_paths[i]
        get_xml_annotation(xml_path, img_path)