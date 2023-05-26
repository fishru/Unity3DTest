from pandas import *
import os
import pickle
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm

class_list = ['Swiping Left', 'Swiping Right', 
              'Pushing Two Fingers Away', 
              'Pulling Hand In', 'Swiping Up']
SET = ['Test','Train', 'Validation']
DATA_DIR = './data'

# for setname in SET:
#     #SET_DIR = DATA_DIR+'/'+setname
#     filename = './labels/'+setname+'.csv'
#     data = read_csv(filename,delimiter=";",header=None)
#     for index, row in data.iterrows():
#         if row[1] in class_list:
#             src_dir = DATA_DIR+'/'+str(row[0])
#             dst_dir = './data_selection/'+setname+'/'+str(row[0])
#             shutil.copytree(src_dir, dst_dir)
#             print(dst_dir)

class_dict = {
    "Swiping Left":"left",
    "Swiping Right":"right",
    "Pushing Two Fingers Away":"forward",
    "Pulling Hand In":"backward",
    "Swiping Up":"jump"
}

# class_dict.keys()

for setname in SET:
    cc = 0
    #SET_DIR = DATA_DIR+'/'+setname
    filename = './labels/'+setname+'.csv'
    data = read_csv(filename,delimiter=";",header=None)
    for index, row in data.iterrows():
        if row[1] in class_dict.keys():            
            # src_dir = './data_selection/'+setname+'/'+str(row[0])
            dst_dir = './data_selection/'+setname+'/'+class_dict[row[1]]+'/'+str(row[0])
            #shutil.move(src_dir, dst_dir)
            count = 0
            for root_dir, cur_dir, files in os.walk(dst_dir):
                count += len(files)
                if count != 37:
                    print(dst_dir)
                    shutil.rmtree(dst_dir)
                    cc += 1
                    #print(count)
    print(cc)