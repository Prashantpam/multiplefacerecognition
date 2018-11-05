import cv2
from IPython.display import clear_output
import os
import dlib
import bul
import pickle



def draw_rectangle(image,coords):
    for i,mtr in enumerate(coords):
        cv2.rectangle(image,(mtr.left(),mtr.right()),(mtr.top(),mtr.bottom()),(150,150,0),8)


def scanner():
    webcam=cv2.VideoCapture(0)
    cv2.namedWindow("Pam Developers",cv2.WINDOW_NORMAL)
    data,frame=webcam.read()
    known_folder='peoples/'
    known_names=[]
    encodings=[]
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
        
    det=dlib.get_frontal_face_detector()
    previous=[]
    people=[]
    while True:
        da,frame=webcam.read()
        faces_coord=det(frame)
        if len(faces_coord):
            cv2.imwrite('try.jpg',frame)
            if not len(faces_coord)==len(previous):
                names=bul.test_image('try.jpg',known_names,encodings,0.45,False)
                    
            for i,mtr in enumerate(faces_coord):
                clear_output(wait=True)
                if names[i]!="unknown":
                    if names[i] not in people:
                        people.append(names[i]);
                cv2.putText(frame,names[i].capitalize(),(mtr.left(),mtr.top()-10),cv2.FONT_HERSHEY_PLAIN,2,(66,53,243),2,cv2.LINE_AA)

        previous=faces_coord
            
        cv2.imshow("Pam Developers",frame)
        if cv2.waitKey(40)&0xFF==27:
            break
    os.remove('try.jpg')
    print(people)
    webcam.release()
    cv2.destroyAllWindows()
    
