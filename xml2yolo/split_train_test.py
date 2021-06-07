import numpy as np
import random
import glob
import argparse
def split_train_test(train_radio=0.9):
    '''
    split the dataset to trainset and testset according to the train_radio.
    And saving train.txt and test.txt into root+'Main'.
    '''
    root = '/home/cym/CYM/dataset/diaoche/diaoche/'
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

    with open(root+'Main/train.txt', 'w') as f:
        f.writelines((train_img_list))
    with open(root+'Main/test.txt', 'w') as f:
        f.writelines(test_img_list)
    print('train:[{}] test:[{}]'.format(train_num, test_num))
    print(len(train_idx), len(test_idx))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--root', type==str, default='', help='the root path of dataset')
    # args = parser.parse_args()
    split_train_test(train_radio=0.9)