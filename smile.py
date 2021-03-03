import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from tensorflow.keras.models import load_model

import cv2
import sys
import logging as log
import datetime as dt
from time import sleep


model = load_model("face.h5")

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0
while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    key = cv2.waitKey(1)
    if key == ord('s'): 
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            video_capture.release()

            # img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            # img_new = cv2.imshow("Captured Image", img_new)
            
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            
            images = 'saved_img.jpg'
            test = tf.keras.preprocessing.image.load_img(images, target_size = (220,220))
            input_arr = keras.preprocessing.image.img_to_array(test)
            input_arr = np.array([input_arr])
            predictions = model.predict(input_arr)

            # print("Processing image...")
            # img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            # print("Converting RGB image to grayscale...")
            # gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            # print("Converted RGB image to grayscale...")
            # print("Resizing image to 28x28 scale...")
            # img_ = cv2.resize(gray,(224,224))
            # print("Resized...")
            # img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            # print("Image saved!")

            mask_dict = {0:'Masked', 1:'No Mask'}
            print(mask_dict[predictions.argmax()])
        
            break
    elif key == ord('q'):
            print("Turning off camera.")
            video_caputure.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    # Display the resulting frames
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()