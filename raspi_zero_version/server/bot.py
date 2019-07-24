# import the libraries
import os
import face_recognition
import cv2
import multiprocessing
import imutils
import time
import RPi.GPIO as GPIO


from imutils.video import VideoStream
from multiprocessing import Process
from datetime import datetime


class Bot:

    def process_frame(self, frame, t):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert image from BGR (openCV) to RGB (face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_faces_encodings, face_encoding)

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_faces[first_match_index]
                print(name)
                self.unlockDoor()
                time.sleep(3)
                self.lockDoor()
                return True
        return False

    def lockDoor(self):
        GPIO.output(37, False)

    def unlockDoor(self):
        GPIO.output(37, True)



    def display_stream(self):

        counter = 0
        refresh = 10

        reset = 0

        while True:
            frame = self.cam.read()
            #cv2.imshow('Video', frame)
            if (counter % refresh == 0):
                greeted_person = self.process_frame(frame, counter)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            counter += 1


    def initKnownEncodings(self):
        # make a list of all the available images
        known_faces = os.listdir('dataset')

        known_faces_recordings = {}
        known_faces_encodings = []

        desired_width = 320


        for file in known_faces:
            original = cv2.imread('dataset/' + file)
            height, width, _ = original.shape
            scale =  desired_width / width
            newX,newY = original.shape[1]*scale, original.shape[0]*scale
            image = cv2.resize(original, (int (newX), int (newY)))
            cv2.imwrite('dataset/' + file, image)

            image = face_recognition.load_image_file('dataset/' + file)
            encoding = face_recognition.face_encodings(image)[0]
            known_faces_encodings.append(encoding)

        self.known_faces = known_faces
        self.known_faces_encodings =known_faces_encodings

    def initGPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(37, GPIO.OUT)
        self.lockDoor()

    def __init__(self):

        self.initKnownEncodings()
        self.initGPIO()
        self.cam = VideoStream(src=0).start()
        time.sleep(2.0)

        self.display_stream()

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

        # Then cleanup GPIO pins
        GPIO.cleanup()

