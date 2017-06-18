import tensorflow as tf
import cv2
import os
import numpy as np
#from PIL import Image

#data_dir = '/Users/xd/Downloads/UCF101_subset'
label_dic = {'Basketball': 0, 'BasketballDunk': 1, 'Biking': 2, 'Diving': 3}

def spliter(data_dir, image_dir):
    for file in os.listdir(data_dir):
        file_dir = os.path.join(data_dir,file)
        if os.path.isdir(file_dir):
            for data in os.listdir(file_dir):
                vc = cv2.VideoCapture(os.path.join(file_dir,data))
                c = 1
                #fps = vc.get(cv2.cv.CV_CAP_PROP_FPS)
                if vc.isOpened():
                    rval, frame = vc.read()
                else:
                    rval = False

                timeF = 15

                while rval:
                    rval, frame = vc.read()
                    if(c%timeF == 0):
                        cv2.imwrite(image_dir + '/' + str(data[:-4]) + '_' + str(c /100) + '.jpg', frame)
                    #print('write done')
                    c = c + 1

                vc.release()

def label_generator(image_dir, label_txt, split_name):
    f = open(label_txt, 'w')
    k = []
    for file in os.listdir(image_dir):
        #print(file)
        if file != '.DS_Store':
            whole_path = image_dir + '/' + file
            #img = Image.open(whole_path)
            if os.path.getsize(whole_path):
                k.append(whole_path)
    if split_name == 'train':
        permutation = np.random.permutation(len(k))
        k = np.array(k)
        k = k[permutation]
        for file in k:
            label = file[len(image_dir)+3:-14]
            if label in label_dic.keys():
                f.write(file + ' ' + str(label_dic[label]))
                f.write('\n')
        print ('label generated')
        f.close()
    elif split_name == 'test':
        for file in k:
            label = file[len(image_dir)+3:-14]
            if label in label_dic.keys():
                f.write(file + ' ' + str(label_dic[label]))
                f.write('\n')
        print ('label generated')
        f.close()
