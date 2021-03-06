

import cv2
import argparse
import os

from face_recognition.preprocess import *
from face_recognition.recognition import *
from face_recognition.database import *


def read_img(file):
    im = cv2.imread(file, 0)
    return im

def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def predict_face(img):
    d = Database()
    e = Eigenfaces(d)
    img = read_img(img)
    img = preprocess(img)
    res = e.predict(img)
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify \
        a facial image against the database")

    parser.add_argument("-i", "--img", help="The path to the image to recognize", required=False)
    parser.add_argument("-e", "--evaluate", help="A flag to evaluate the accuracy of the algorithm", required=False, default=None, action='store_true')

    args = parser.parse_args()
    if args.evaluate:
        energies = [0.85]
        metrics = ['l2_norm']
        tops = [5]

        for energy in energies:
            for metric in metrics:
                for top in tops:
                    d = Database()
                    e = Eigenfaces(d, energy=energy)
                    res = e.evaluate(metric=metric, top=top)
                    print(energy, metric, top, res)
                    print("ACCURACY IS ", res*100, "%")

    elif os.path.exists(args.img):
        res = predict_face(args.img)
        print(res)
        
    else:
        print("Please enter a valid path to an image to recognize")
    
