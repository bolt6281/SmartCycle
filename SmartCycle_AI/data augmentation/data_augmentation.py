from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot as plt
from cv2 import cv2
import os

loc = "...//augmented_data"
data_list = os.listdir(loc)

for each in data_list:

    inside = loc + "//" + each
    inside_list = os.listdir(inside)[:-1]

    # total 10000 images (10 times)

    if each[-1] == "1":
        brightness_lowest = 0.6
        to_be = 400
    else:
        brightness_lowest = 0.8
        to_be = 400
        
    # create image data augmentation generator
    datagen = ImageDataGenerator(horizontal_flip=True, rotation_range=35, brightness_range=[brightness_lowest,1.0])
    
    print("\nstart to augment", each + ". . .\n")
    cycle = 0
    while True:
        for inside_each in inside_list:
            
            # load the image
            img = load_img(inside + "//" + inside_each)

            # convert to numpy array
            data = img_to_array(img)

            # expand dimension to one sample
            samples = expand_dims(data, 0)

            # prepare iterator
            it = datagen.flow(samples, batch_size=1)

            # generate samples
            batch = it.next()[0].astype('uint8')
            batch = cv2.cvtColor(batch, cv2.COLOR_RGB2BGR)
            cv2.imwrite(inside + "//" + inside_each[:-4] + "_argumented_" + str(cycle) + ".jpg", batch)
            
            current_amount = len(os.listdir(inside)[:-1])
        
        if (to_be - current_amount) < 50 : # Done
            break
        cycle+=1
    
    print("\n" + each + " is successfully augmented!\n")

print("Done!")