#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:33:20 2021

@author: malav
"""

import numpy as np
from PIL import Image
from pathlib import Path
import time
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras import applications


##time function
def timer(func):
    def wrapper(*args,**kwargs):
        before = time.time()
        a = func(*args,**kwargs)
        print('function time : ',time.time() - before, "seconds" )
        return a
    return wrapper

###batch_create
def batch_create(l, n):
    batch_create_list=[]
    for i in range(0, len(l), n):
        batch_create_list.append(l[i:i+n])
    print("batches created : {}".format(len(batch_create_list)))
    return batch_create_list


class FeatureExtractor(object):

    def __init__(self,name):
        if name == 'ResNet50':
            self.model= applications.resnet50.ResNet50(weights='imagenet', include_top=False, pooling='avg')
        elif name == 'Xception':
            self.model= applications.xception.Xception(weights='imagenet', include_top=False, pooling='avg')
        elif name == 'VGG16':
            self.model= applications.vgg16.VGG16(weights='imagenet', include_top=False, pooling='avg')
        elif name == 'VGG19':
            self.model= applications.vgg19.VGG19(weights='imagenet', include_top=False, pooling='avg')
        elif name == 'InceptionV3':
            self.model= applications.inception_v3.InceptionV3(weights='imagenet', include_top=False, pooling='avg')
        elif name == 'MobileNet':
            self.model= applications.mobilenet.MobileNet(weights='imagenet', include_top=False, pooling='avg')
        else:
            raise ValueError('Unrecognised model: "{}"'.format(name))
        
    def batch_open(self,img_paths):
        batchImages =[]
        for i in range(len(img_paths)):
            img = cv2.imread(img_paths[i])
            img1 = Image.fromarray(img)
            img = img1.resize((224, 224))  # VGG takes 224x224 img as an input
            img = img.convert('RGB')  
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
            x = preprocess_input(x)  # Subtracting avg values for each pixel
            batchImages.append(x)
        return batchImages


    def folder_to_extract(self,folder_path):
        features = []
        features_name = []
        for img_path in sorted(Path(folder_path).rglob("b*")):
            f1  = self.extract(img=Image.open(img_path))
            features.append(f1)
            features_name.append(img_path.stem)
        return features,features_name

    def batch_save(self,features,features_name,write_to):
        for i in range(len(features)):
            #x = path_loc+features_name[i]
            y = features[i]
            x_path = write_to+'/'+str(features_name[i])+'_emb.npy'
            with open(x_path,'wb') as f:
                #print(x_path)
                np.save(f,y)
        #return True
        
    @timer
    def batch_extract(self,batch_file,batches_names,batch_size,write_to=None):
        #list_2 = []     ####create empty list
        print("starting loop - 1")
        print(len(batch_file))
        for i in range(len(batch_file)):
            #a1 = self.batch_url_extract(batch_file[i])   ###location
            f1  = self.batch_open(batch_file[i])   ##opening the first batch
            batchImagesStack = np.vstack(f1)   ##stacking the images
            if i==0:
                print("prediction of first batch")
            feature = (self.model).predict(batchImagesStack,batch_size=batch_size)  #### extracting the feature
            final_batch= feature / np.linalg.norm(feature)  ##normalization
            final_batch = final_batch.reshape((len(final_batch),2048))  ##reshaping according to the batch size
            if i==0:
                print("saving the first batch")
            fea_names = batches_names[i]
            self.batch_save(final_batch,fea_names,write_to)
            if i%5==0:
                print("Number of batches done : {}".format(i))
        #return list_2
        

        

  
