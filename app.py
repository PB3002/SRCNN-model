from flask import *
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import keras.backend as K
import numpy as np
import cv2

app = Flask(__name__)

#Allow item extension
duoi_file = set(['png','jpg','jpeg','gif'])

@app.route('/',methods=['GET'])
def helloworld():
    return render_template("home.html")

@app.route('/result',methods=['GET'])
def result_page():
    input_img_filename = request.files['lowres_upload'].filename
    or_img_filename = request.files['ori_upload'].filename
    predicted_img_filename = input_img_filename.split(".")[0] + "_predicted.jpg"
    
    input_img_url = url_for('static', filename='pics/'+input_img_filename)
    predicted_img_url = url_for('static', filename='predicted pics/'+predicted_img_filename)
    or_img_url = url_for('static', filename='original pics/'+input_img_filename)
    
    return render_template("result.html", input_img_url=input_img_url, predicted_img_url=predicted_img_url,or_img_url=or_img_url)

@app.route('/',methods=['POST'])
def upload_page():
    if request.method == 'POST':
        #Original img
        originalfile = request.files['ori_upload']
        img_path = "./static/original pics/"+originalfile.filename
        originalfile.save(img_path)

        #Lowres img
        lowresfile = request.files['lowres_upload']
        img_path = "./static/pics/"+lowresfile.filename
        lowresfile.save(img_path)
        scale_factor = 2

        image = cv2.imread(img_path)
        w,h,c = image.shape
        image_bicubic = cv2.resize(image, (w*scale_factor, h*scale_factor), interpolation = cv2.INTER_CUBIC)
        image_bicubic_arr = img_to_array(image_bicubic)
        image_bicubic_arr = cv2.cvtColor(image_bicubic_arr, cv2.COLOR_BGR2RGB)

        def psnr(y_true,y_pred):
            return -10*K.log(K.mean(K.flatten((y_true-y_pred))**2))/np.log(10)
        srcnn_model = load_model('./srcnn_update.h5',custom_objects={'psnr': psnr})

        image_pred = srcnn_model.predict(image_bicubic_arr.reshape(1, w*scale_factor, h*scale_factor, 3) / 255.) * 255.
        predicted_image = image_pred[0].astype(np.uint8)
        predicted_image = cv2.cvtColor(predicted_image,cv2.COLOR_RGB2BGR)

        predicted_image_path = './static/predicted pics/' + lowresfile.filename.split(".")[0] + "_predicted.jpg"
        cv2.imwrite(predicted_image_path, predicted_image)

        return result_page()

if __name__=="__main__":
    app.run(debug=True)