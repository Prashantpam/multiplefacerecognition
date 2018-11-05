from __future__ import print_function
import os
import re
import api as face_recognition
import PIL.Image
import numpy as np
from collections import Counter
from collections import defaultdict

def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []
    
    for f in os.listdir(known_people_folder):
        for file in image_files_in_folder(known_people_folder+f):
            
            basename = os.path.splitext(os.path.basename(file))[0]
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)
            
            if len(encodings) > 1:
                print("WARNING: More than one face found in {}. Only considering the first face.".format(file))
            
            if len(encodings) == 0:
                print("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_names.append(f)
                known_face_encodings.append(encodings[0])
            
    return known_names, known_face_encodings


def print_result(filename, name, distance, show_distance=False):
    return name

def test_image(image_to_check,known_names,known_face_encodings,tolerance=0.6,show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)
    
    if max(unknown_image.shape) > 1600:
        
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)
    
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    faces=[]
    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)
        res=[]
        if True in result:
            [res.append(print_result(image_to_check, name, distance, show_distance)) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else:
            res.append(print_result(image_to_check, "unknown", None, show_distance))
        mat=defaultdict(int)
        mat=Counter(res)
        res=max(mat.items(),key=lambda x:x[1])
        faces.append(res[0])
            
    if not unknown_encodings:

        print_result(image_to_check, "no_persons_found", None, show_distance)
    return faces
    


def image_files_in_folder(folder):
    mtp=[folder+"/"+f for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]
    return mtp
