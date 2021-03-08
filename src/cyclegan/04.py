import cv2
import os
import random
import copy as cp
generation_size = 256
generation_num = 1000
img_a = cv2.imread("SAR.png")
img_b = cv2.imread("OPTICAL.png")
limit_y = img_a.shape[0] - generation_size
output_dir = "./datasets/customsar/"
os.makedirs( output_dir + 'trainA', exist_ok=True)
os.makedirs( output_dir + 'trainB', exist_ok=True)
os.makedirs( output_dir + 'testA', exist_ok=True)
os.makedirs( output_dir + 'testB', exist_ok=True)

for i in range(generation_num):
  offset_y = random.randint(generation_size, img_a.shape[0]) - generation_size
  offset_x = random.randint(generation_size, img_a.shape[1]) - generation_size
  new_a = cp.deepcopy(img_a[offset_y:offset_y+generation_size, offset_x:offset_x+generation_size, :])
  new_b = cp.deepcopy(img_b[offset_y:offset_y+generation_size, offset_x:offset_x+generation_size, :])
  cv2.imwrite(output_dir + "trainA/" + str(i) + ".png", new_a)
  cv2.imwrite(output_dir + "trainB/" + str(i) + ".png", new_b)

split_num = int(img_a.shape[1] / generation_size)
for i in range(split_num):
  offset_y = img_a.shape[0] - generation_size
  offset_x = i * generation_size
  new_a = cp.deepcopy(img_a[offset_y:offset_y+generation_size, offset_x:offset_x+generation_size, :])
  new_b = cp.deepcopy(img_b[offset_y:offset_y+generation_size, offset_x:offset_x+generation_size, :])
  cv2.imwrite(output_dir + "testA/" + str(i) + ".png", new_a)
  cv2.imwrite(output_dir + "testB/" + str(i) + ".png", new_b)
