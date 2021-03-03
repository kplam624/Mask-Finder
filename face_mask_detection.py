#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import os
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import random
import pickle
from PIL import Image
from numpy import asarray


# In[2]:


# find and read image
images_dir = cv2.imread("/Users/atemkuh/Documents/GitHub/Mask-Finder/data/with_mask/0.jpg")


# In[3]:


#view image and convert into RGB using cv2
plt.imshow(cv2.cvtColor(images_dir, cv2.COLOR_BGR2RGB))


# In[4]:


#images_dir.shape


# In[5]:


#loop through dataset
Images_directory = "/Users/atemkuh/Documents/GitHub/Mask-Finder/data"
Classes = ["with_mask","without_mask"]
for category in Classes:
    path = os.path.join(Images_directory, category)
    for img in os.listdir(path):
        images_dir = cv2.imread(os.path.join(path,img))
        
        plt.imshow(cv2.cvtColor(images_dir, cv2.COLOR_BGR2RGB))
        plt.show()
        # stop processing after first image
        break
    break
    


# In[ ]:





# In[4]:


#resize images using imageNet 
img_size = 224
new_img_array=cv2.resize(images_dir,(img_size,img_size))
plt.imshow(cv2.cvtColor(images_dir, cv2.COLOR_BGR2RGB))
plt.show()


# In[7]:


# convert images to arrays 
training_data = []

def create_training_data():
    for category in Classes:
        path = os.path.join(Images_directory,category)
        class_num = Classes.index(category)
        
        print("category")
        for img in os.listdir(path):
            try:
               # print(img, ", ", path)
                images_dir    = cv2.imread(os.path.join(path,img))
                
                new_img_array = cv2.resize(images_dir,(img_size,img_size))
                
                training_data.append([new_img_array, class_num])
              #  print(len(training_data))
                
            except Exception as e:
                print(e)
                
                
    


# In[8]:


create_training_data()


# In[9]:


print(len(training_data))


# In[10]:


random.shuffle(training_data)


# In[11]:


X =[]
y=[]

for features,label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1,img_size,img_size,3)


# In[12]:


X.shape


# In[13]:


Y=np.array(y)


# In[14]:


#pickle x
pickle_out = open("X.pickle","wb")
pickle.dump(X,pickle_out)
pickle_out.close()
#pickle y
pickle_out = open("y.pickle","wb")
pickle.dump(y,pickle_out)
pickle_out.close()


# In[15]:


pickle_in = open("X.pickle","rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle","rb")
y = pickle.load(pickle_in)


# In[16]:


#create and train deep learning model
#pre trained model
model = tf.keras.applications.MobileNet()
model.summary() #Total params: 4,253,864


# In[17]:


# use existing solution by implementing transfer learning "tuning", "weights"
base_input = model.layers[0].input
base_output = model.layers[-4].output
Flatten_layer =  layers.Flatten()(base_output)
#classifier  can either be 0 or 1
final_output = layers.Dense(1)(Flatten_layer)
final_output = layers.Activation('sigmoid')(final_output)
#new model

new_model=keras.Model(inputs = base_input, outputs = final_output)
new_model.summary()## display the sum of the new model #Total params: 3,229,889


# In[18]:


#setup up configuration os classes('with_mask','without_mask')

#compile new model
new_model.compile(loss="binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])


# In[19]:


new_model.fit (X,Y, epochs = 1, validation_split = 0.1)


# In[9]:


#save model
new_model.save('new_model.h5')


# In[7]:


#import trained model using tf.keras.models.load_model
new_model = tf.keras.models.load_model('new_model.h5')


# In[8]:


#predictions with mask
frame = cv2.imread('demo_mask.jpg')


# In[72]:


plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


# In[73]:


final_img =cv2.resize(frame,(224,224))
final_img =np.expand_dims(final_img, axis=0)
final_img = final_img/255.0


# In[74]:


Predictions = new_model.predict(final_img)
Predictions


# In[75]:


frame=cv2.imread('demo_without_mask.jpg')


# In[76]:


plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


# In[77]:


#get haarcascades feature detector with prestore faces and features
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
#convert image from BGR to gray
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray.shape


# In[84]:


# to detect faces

faces = faceCascade.detectMultiScale(gray,1.1,4) # detects face and gives the four corners of the face

for x,y,w,h in faces:
    
    roi_gray = gray[y:y + h, x:x + w]
    
    roi_color = frame[y:y + h, x:x + w]
    
    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2) # DRAWS A RECTANGLE ON THE FACE
    
    facess = faceCascade.detectMultiScale(roi_gray)
    
    if len(facess)==0:
        
        print("No Face Detected")
    else:
        for (ex, ey, ew, eh) in facess:
            
            face_roi = roi_color[ey: ey + eh, ex: ex + ew] # CROPS FACE


# In[85]:


plt.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))# DETECT FACE AND PLACE A RECTANGLE ON THE FACE


# In[82]:


# crop face
plt.imshow(cv2.cvtColor(face_roi,cv2.COLOR_BGR2RGB))# crop our region of interest (ROI)


# In[60]:


final_img =cv2.resize(face_roi,(224,224))
final_img =np.expand_dims(final_img, axis=0)
final_img = final_img/255.0
Predictions = new_model.predict(final_img)
Predictions


# In[ ]:


path = "haarcascade_frontalface_default.xml"
font_scale=1.5
font = cv2.FONT_HERSHEY_PLAIN

rectangle_bgr = (255,255,255)
img = np.zeros((500,500))
text="some. text in a box!"#text in a box
#width and height
(text_width, text_height) = cv2.getTextSize(text,font,fontScale=font_scale, thickness=1)[0]
#set text position

text_offset_x = 10
text_offset_y = img.shape[0]-25

#box coords

box_coords =((text_offset_x, text_offset_y),(text_offset_x + text_width + 2,text_offset_y - text_height - 2))
cv2.rectangle (img,box_coords[0], box_coords[1],rectangle_bgr, cv2.FILLED)
cv2.putText(img,text,(text_offset_x, text_offset_y), font, fontScale=font_scale, color = (0,0,0), thickness = 1)
#setup video capture

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    cap = cv2.VideoCapture(0)#number of camera 0 for one camera present
if not cap.isOpened():
    raise IOError("Please check webcam")

while True:
    
    ret,frame = cap.read()
    
    faceCascade =cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.1,4)
    
    for x,y,w,h in faces:
        
        roi_gray=gray[y:y+h, x:x+w] 
        
        roi_color = frame[y:y+h, x:x+w]
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)
        
        facess = faceCascade.detectMultiScale(roi_gray)
        
        if len(facess)==0:
            print ("No face detected")
        else:
            # crop our region of interest (ROI)
            
            for (ex,ey,ew,eh) in facess:
                
                face_roi = roi_color[ey: ey+eh, ex:ex + ew]
                
                
                
                
    final_image = cv2.resize(face_roi,(224,224))
    
    final_image= np.expand_dims(final_image,axis =0)
    
    final_image=final_image/255.0
    
    font=cv2.FONT_HERSHEY_SIMPLEX
    
    Predictions = new_model.predict(final_image)
    
    font_scale=1.5
    
    font=cv2.FONT_HERSHEY_PLAIN
    
    if (Predictions>0):
        
        status = "NO Mask"
        x1,y1,w1,h1 = 0,0,175,75
        
        cv2.rectangle(frame, (x1,x1),(x1+w1, y1+h1), (0,0,0), -1)
        
        cv2.putText (frame,status, (x1+int (w1/10), y1+int (h1/2)), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255),2)
        
        cv2.putText(frame,status,(100,150), font,3, (0,0,255),2,cv2.LINE_4)
        
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255))
        
        
    else:
        status = "Thank You"
        
        x1,y1,w1,h1 = 0,0,175,75
        
        cv2.rectangle(frame, (x1,x1),(x1+w1,y1+h1), (0,0,0), -1)
        
        cv2.putText (frame,status, (x1+int(w1/10),y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,255,0),2)
        
        cv2.putText(frame,status,(100,150),font,3,(0,255,0),2,cv2.LINE_4)
        
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0))
        
        cv2.imshow('Mask Finder', frame)
        if cv2.waitKey(2)& 0xFF ==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
        
            
    #     


# In[ ]:




