import os
import cv2
import face_recognition

host = 'http://192.168.0.7'
port = 8000
stream_url = 'stream.mjpg'

url = host + ':' + str(port) + '/' + stream_url

cap = cv2.VideoCapture(url)


def initKnownEncodings(self):
    # make a list of all the available images
    known_faces = os.listdir('dataset')
    known_faces_encodings = []
    for file in known_faces:
        image = face_recognition.load_image_file('dataset/' + file)
        encoding = face_recognition.face_encodings(image)[0]
        known_faces_encodings.append(encoding)
    self.known_faces = known_faces
    self.known_faces_encodings = known_faces_encodings


def process_frame(self, frame):
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


while True:
  ret, frame = cap.read()
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    exit(0)