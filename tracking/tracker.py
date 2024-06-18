
import cv2
import time
import numpy as np

classify_car = cv2.CascadeClassifier('car.xml')

vid_capture = cv2.VideoCapture('moving_cars')