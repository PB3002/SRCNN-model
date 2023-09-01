from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import keras.backend as K
import numpy as np
import cv2

img_height,img_width = 256,256
scale_factor = 2

img_path = "./static/pics/butterfly.png"


image = cv2.imread(img_path)
w,h,c = image.shape
image_bicubic = cv2.resize(image, (w*scale_factor, h*scale_factor), interpolation = cv2.INTER_CUBIC)
image_bicubic_arr = img_to_array(image_bicubic)
image_bicubic_arr = cv2.cvtColor(image_bicubic_arr, cv2.COLOR_BGR2RGB)

def psnr(y_true,y_pred):
    return -10*K.log(K.mean(K.flatten((y_true-y_pred))**2))/np.log(10)
srcnn_model = load_model('./srcnn_update.h5',custom_objects={'psnr': psnr})

image_pred = srcnn_model.predict(image_bicubic_arr.reshape(1, w*scale_factor, h*scale_factor, 3) / 255.) * 255.

predicted_image_path = "./static/predicted pics/butterfly_predicted.jpg"
predicted_image = cv2.cvtColor(image_pred[0].astype(np.uint8), cv2.COLOR_RGB2BGR)
cv2.imwrite(predicted_image_path, predicted_image)