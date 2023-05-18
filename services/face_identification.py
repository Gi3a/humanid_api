import ast

import numpy as np
import face_recognition
import urllib.request as ur

from models import Face


# Base64 Image to Face_Encodings
def get_encodings_from_image(face_data: Face):

    decoded = ur.urlopen(face_data.face_image)

    unknown_image = face_recognition.load_image_file(decoded)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    return unknown_encoding


def get_identification(rows, unknown_encoding):
    # Init person
    person = None

    if rows:
        for row in rows:
            face_encodings = eval(row[2])
            results = face_recognition.compare_faces(
                [face_encodings], unknown_encoding)
            if True in results:
                person = {
                    "id": row[0],
                    "public_key": row[1],
                    "face_encodings": face_encodings
                }
                return person
    return person


def get_encodings_from_string(face_encodings_string):
    face_encodings_list = eval(face_encodings_string)
    face_encodings_array = np.array(face_encodings_list)
    return face_encodings_array


def check_face_equality(face1, face2):
    str_element_list = ast.literal_eval(face1)
    result = str_element_list == face2
    return result
