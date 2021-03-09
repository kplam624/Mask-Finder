# Importing main dependencies. for flask
from flask import Flask, jsonify, render_template, redirect, session, request
import os
import datetime
import socket
import sys

# Below is if the javascript code works
# from urllib import request as rq
import tensorflow as tf
import numpy as np
import PIL
from tensorflow import keras
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

# The script that holds the opencv function.
# import smile

# loading in the pretrained model
model = load_model("face.h5")

# Setting variables for uploads
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Create an instance of flask
app = Flask(__name__)

# Config the upload stream
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the routes that are used

# Home route
@app.route('/')
def home():
    print("Responding to the home route:", datetime.datetime.now())
    return render_template("index.html")

# Coronavirus route to show some visualizations
@app.route('/mask-info')
def maskinfo():
    print("Responding to the mask info route:", datetime.datetime.now())
    return render_template("corona_info.html")

# Brings the person to the page
@app.route('/mask-detector')
def detector():
    print("Responding to the mask detector route:", datetime.datetime.now())
    return render_template("mask_detector.html")

# The about us section of the page
@app.route('/about')
def about():
    print("Responding to the about us page:", datetime.datetime.now())
    return render_template("about.html")

# Route that pulls the data and uses it to create a prediction. Using JS to for post request.
@app.route('/webcamcapture', methods = ["GET","POST"])
def capture():
    if request.method == 'POST':
        print("Revving up those frying", datetime.datetime.now())
        
        # Reading the form as an image with file storage.
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        img = request.files["image"]

        # Attempting to read the form as a data_uri
        # img = request.form.get["image"]

        # with rq.urlopen(img) as response:
        #     data = response.read()

        # with open("static/img/saved_image.jpg", "wb") as j:
        #     j.write(data)

        # image = "static/img/myimage.jpg"

        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            print("Saving the file.")
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Identifying the filename.
        # print("The file name is: ", img.filename)

        return 'All Good'


    else:

        print("Responding to the webcam capture route", datetime.datetime.now())    
        
        # Pulls the file out.
        image = "static/img/saved_image.jpg"
        test = tf.keras.preprocessing.image.load_img(image, target_size = (220,220))
        input_arr = keras.preprocessing.image.img_to_array(test)
        input_arr = np.array([input_arr])
        predictions = model.predict(input_arr)
        
        # This file creates a dictionary to define the outcome. 
        mask_dict = {0:'Masked', 1:'No Mask'}
        result = mask_dict[predictions.argmax()]
        print(result)

        # Results in a json format to be used.
        result = [{'message': result}]

        # Want to focus on the 'POST' request, using dummy message 
        # result = [{'message': 'Masked'}]
    
    return jsonify(result)

# # Demo day incase the QOL does not work by then.
# @app.route('/webcamcapture', methods = ["GET","POST"])
# def capture():
#     result = ""
#     message = smile.mask()
#     result = [{'message': message}]
    
#     return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)