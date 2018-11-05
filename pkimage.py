import cv2
from IPython.display import clear_output
import numpy as np
import pandas as pd
import os
import dlib
import bul
import pickle
import time

class Detect:
    def __init__(self):
        self.face_detec=dlib.get_frontal_face_detector()

    def detec(self,image,biggest_only=True):
        faces_coord=self.face_detec(image,1)
        return faces_coord                          


def draw_rectangle(image,coords):
    img=dlib.image_window()
    img.set_image(image)
    for i,mtr in enumerate(coords):
        img.add_overlay(mtr)
    return img

def image(image):
    det=Detect()
    known_folder='peoples/'
    frame=cv2.imread(image,1)
    known_names=[]
    encodings=[]
    people=[]
    if not os.path.exists('known_names.pickle'):
        print('train....')
        wrt1=open('known_names.pickle','wb')
        wrt2=open('encodings.pickle','wb')
        known_names,encodings=bul.scan_known_people(known_folder)
        pickle.dump(known_names,wrt1)
        pickle.dump(encodings,wrt2)
        wrt1.close()
        wrt2.close()
    else:
        print('fetch....')
        wrt1=open('known_names.pickle','rb')
        wrt2=open('encodings.pickle','rb')
        known_names=pickle.load(wrt1)
        encodings=pickle.load(wrt2)
        wrt1.close()
        wrt2.close()
    names=bul.test_image(image,known_names,encodings,0.45,False)
    
    faces_coord=det.detec(frame,True)
    if len(faces_coord):
                
        for i,mat in enumerate(faces_coord):
            clear_output(wait=True)
            if names[i] != "unknown":
                if names[i] not in people:
                    people.append(names[i])
            cv2.putText(frame,names[i].capitalize(),(mat.left(),mat.top()-10),cv2.FONT_HERSHEY_PLAIN,1,(66,53,243),2,cv2.LINE_AA)
        
    img=draw_rectangle(frame,faces_coord)
    print(people)
    time.sleep(8)
    print('exit...')