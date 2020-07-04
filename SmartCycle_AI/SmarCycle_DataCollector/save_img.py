import cv2
import numpy as np
import time

#save image
def save_image_640(image, index, location, show_shape = True):
    
    cv2.imwrite(location+"/image"+str(index)+'.jpg', image)
    if show_shape == True :
        print(str(index)+"th image("+str(image.shape)+") has been saved!\n")
    index+=1
    return index