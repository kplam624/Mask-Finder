from urllib import request
from flask import Flask, jsonify, render_template, redirect, session
import datetime
import socket
import smile
import sys
import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from tensorflow.keras.models import load_model

model = load_model("face.h5")

# Create an instance of flask
app = Flask(__name__)

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

# Route that pulls the data and uses it to create a prediction.
@app.route('/webcamcapture', methods = ["GET","POST"])
def capture():
    if request.method == 'POST':
        img = request.form["image"]
        print("Recieving", datetime.datetime.now())

    else:
        print("Responding to the webcam capture route", datetime.datetime.now())
        
        # Pulls the file to the image.
        img = request.args.get("image")

        result = ""
        # message = smile.mask()

        with request.urlopen(data_uri) as response:
            data = response.read()

        with open("static/img/saved_image.jpg", "wb") as j:
            j.write(data)
            
        images = 'static/img/saved_img.jpg'
        test = tf.keras.preprocessing.image.load_img(images, target_size = (220,220))
        input_arr = keras.preprocessing.image.img_to_array(test)
        input_arr = np.array([input_arr])
        predictions = model.predict(input_arr)
        
        # This file creates a dictionary to define the outcome. 
        mask_dict = {0:'Masked', 1:'No Mask'}
        result = mask_dict[predictions.argmax()]
        print(result)
    
        result = [{'message': message}]
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)