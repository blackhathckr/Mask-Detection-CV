import cv2
import numpy as np
import requests
import requests
import joblib as jb
from keras.models import load_model
model=jb.load("model.h5")

labels_dict={0:'without mask',1:'mask'}
color_dict={0:(0,0,255),1:(0,255,0)}

url="http://IP_over_LAN/shot.jpg"

size = 4
webcam = cv2.VideoCapture(0) #Use camera 0

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    (rval, im) = webcam.read()
    #frame=requests.get(url)
    #frame=np.array(bytearray(frame.content),dtype=np.uint8)
    #frame=cv2.imdecode(frame,1)
    im=cv2.flip(im,1,1) # Flip to act as a mirror

    # Resize the image to speed up detection
    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))

    # Detect MultiScale / faces 
    faces = classifier.detectMultiScale(mini)

    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
        #Save just the rectangle faces in SubRecFaces
        face_img = im[y:y+h, x:x+w]
        resized=cv2.resize(face_img,(150,150))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        #print(result)
        
        label=np.argmax(result,axis=1)[0]
      
        cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(im, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
    # Show the Image
    cv2.imshow('Real Time Face Mask Detection',im)
    key = cv2.waitKey(10)
    # if Esc key is pressed then break out of the loop 
    if key == 27: #The Esc key
        break

webcam.release()

# Close all the windows
cv2.destroyAllWindows()