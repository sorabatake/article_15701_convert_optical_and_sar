import os, requests, subprocess
import math
import numpy as np
import cv2
import random

# read dataset
file_path = "./ROIs1970_fall/"
cmd = "find " + file_path + "s1* | grep png"
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
file_name_list = process.rsplit()
data_x = []
data_y = []
for _file_name in file_name_list:
  data_x.append(_file_name)
  data_y.append(_file_name.replace('s1_','s2_'))
data_x = np.asarray(data_x)
data_y = np.asarray(data_y)

# extract data
part_data_ratio = 0.1 # extract data depending on the ratio from all data
test_data_ratio = 0.1
all_data_size = len(data_x)
idxs = range(all_data_size) # all data
part_idxs = random.sample(idxs, int(all_data_size * part_data_ratio)) # part data
part_data_size = len(part_idxs)
test_data_idxs = random.sample(part_idxs, int(part_data_size * test_data_ratio)) # test data from part data
train_data_idxs = list(set(part_idxs) - set(test_data_idxs)) # train data = all data - test data
test_x = data_x[test_data_idxs]
test_y = data_y[test_data_idxs]
train_x = data_x[train_data_idxs]
train_y = data_y[train_data_idxs]

# data copy
os.makedirs('datasets/sar/trainA', exist_ok=True)
os.makedirs('datasets/sar/trainB', exist_ok=True)
os.makedirs('datasets/sar/testA', exist_ok=True)
os.makedirs('datasets/sar/testB', exist_ok=True)
cmd = 'find ./datasets/sar/* -type l -exec unlink {} \;'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
print("[Start] extract test dataset")
for i in range(len(test_x)):
  cmd = "ln -s " + test_x[i] + " datasets/sar/testA/"
  process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
  cmd = "ln -s " + test_y[i] + " datasets/sar/testB/"
  process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
  if i % 500 == 0:
    print("[Done] ", i, "/", len(test_x))
print("Finished")

print("[Start] extract train dataset")
for i in range(len(train_x)):
  cmd = "ln -s " + train_x[i] + " datasets/sar/trainA/"
  process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
  cmd = "ln -s " + train_y[i] + " datasets/sar/trainB/"
  process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
  if i % 500 == 0:
    print("[Done] ", i, "/", len(train_x))
print("Finished")

