from flask import Flask, jsonify, render_template, redirect, session
import datetime
import os
import socket


# Create an instance of flask
app = Flask(__name__)

# Define the routes that are used
@app.route('/')
def home():
    print("Responding to the home route:", datetime.datetime.now())
    return render_template("index.html")

@app.route('/mask-info')
def maskinfo():
    print("Responding to the mask info route:", datetime.datetime.now())
    return render_template("mask_info.html")

@app.route('/mask-detector')
def detector():
    print("Responding to the mask info route:", datetime.datetime.now())
    return render_template("mask_detector.html")

@app.route('/about')
def about():
    print("Responding to the about us page:", datetime.datetime.now())
    return render_template("about_us.html")

@app.route('/webcamcapture')
def home():
    print("Responding to the webcam capture route", datetime.datetime.now())
    return redirect('/mask-info')

if __name__ == "__main__":
    app.run(debug=True)