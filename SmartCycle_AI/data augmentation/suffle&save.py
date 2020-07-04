import os
from cv2 import cv2
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import random
import numpy as np

loc = "...//augmented_data"
data_list = os.listdir(loc)

destination = "...//SmartCycle_AI//SmartCycle_Trainer//tensorflow1//models//research//object_detection//images"
i = 0

# 전체 개수 확인
for each in data_list:

    inside = loc + "//" + each
    i += len(os.listdir(inside)[:-1])

index_list = np.arange(i-1)
random.shuffle(index_list)
IndexOfIndex = -1


for each in data_list:

    inside = loc + "//" + each
    inside_list = os.listdir(inside)[:-1]
    os.mkdir(destination + "//" + each)
    
    for inside_each in inside_list:
            
        # load the image
        img = img_to_array( load_img(inside + "//" + inside_each) )

        # save as different name
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        IndexOfIndex+=1
        cv2.imwrite(destination + "//" + each + "//image-" + str( index_list[IndexOfIndex] ) + ".jpg", img)
        if index_list[IndexOfIndex] == index_list[-1]:
            break

print("Done!")