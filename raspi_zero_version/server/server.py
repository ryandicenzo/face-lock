import os
import cv2
import face_recognition
import threading
import csv
import sys

from PIL import Image, ImageTk
from gpiozero import LED
from time import sleep

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from support import resting_state_support


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("957x442+628+328")
        top.title("Facelock")
        top.configure(borderwidth="2")
        top.configure(background="#e8e8e8")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.773, rely=0.747, height=24, width=107)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''New User''')

        self.stream = tk.Label(top)
        self.stream.place(relx=0.021, rely=0.045, height=391, width=584)
        self.stream.configure(activebackground="#f9f9f9")
        self.stream.configure(activeforeground="black")
        self.stream.configure(background="#d9d9d9")
        self.stream.configure(disabledforeground="#a3a3a3")
        self.stream.configure(foreground="#000000")
        self.stream.configure(highlightbackground="#d9d9d9")
        self.stream.configure(highlightcolor="black")
        self.stream.configure(width=584)

        self.avatar = tk.Label(top)
        self.avatar.place(relx=0.69, rely=0.068, height=281, width=264)
        self.avatar.configure(background="#d9d9d9")
        self.avatar.configure(disabledforeground="#a3a3a3")
        self.avatar.configure(foreground="#000000")
        self.avatar.configure(width=264)


class RestingScreen(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()


    def run(self):
        self.vp_start_gui()

    def vp_start_gui(self):
        '''Starting point when module is the main routine.'''
        global val, w, root
        root = tk.Tk()
        top = Toplevel1(root)
        self.top = top

        resting_state_support.init(root, top)
        root.mainloop()

    w = None

    def create_Toplevel1(self, root, *args, **kwargs):
        '''Starting point when module is imported by another program.'''
        global w, w_win, rt
        rt = root
        w = tk.Toplevel(root)
        top = Toplevel1(w)
        resting_state_support.init(w, top, *args, **kwargs)
        return (w, top)

    def destroy_Toplevel1(self):
        global w
        w.destroy()
        w = None

    def show_avatar(self, avatar):
        avatar_label = self.top.avatar

        avatar_label.configure(image=avatar)

        # necessary to keep a reference to image so it is not removed by garbage collector
        avatar_label.image = avatar

        return False

    def update_stream(self, frame):
        self.top.stream.configure(image=frame)
        self.top.stream._backbuffer_ = frame

class Server:
    with open('ip_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        next(reader) # pass over template row

        info = next(reader)

        try:
            host = info[0]
        except:
            print('Please specify host in ip_data')
        try:
            port = info[1]
        except:
            print('Please specify port in ip_data')

    stream_url = 'stream.mjpg'

    def __init__(self):

        # launch gui
        self.screen = RestingScreen()

        # load default avatar

        default_avatar = self.cv2_to_tkinter(cv2.imread('../resources/default-avatar.jpg'))
        self.screen.show_avatar(default_avatar)

        # initialize face encodings
        self.initKnownEncodings()

        url = self.host + ':' + str(self.port) + '/' + self.stream_url
        cap = cv2.VideoCapture(url)

        # initalize gpio / led
        self.green = LED(17)
        self.lock = LED(26)

        fps = 24
        delay = 3

        reset = fps * delay
        timer = 0

        while True:
            ret, frame = cap.read()

            tki_frame = self.cv2_to_tkinter(frame)
            self.screen.update_stream(tki_frame)

            if (timer <= 0):
                if (self.process_frame(frame)):
                    timer = reset
            else:
                timer -= 1

            if cv2.waitKey(1) == 27:
                exit(0)

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

    def unlock_door(self):
        self.lock.on()

    def lock_door(self):
        self.lock.off()

    def cv2_to_tkinter(self, cv2_image):
        tki = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)))
        return tki

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

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_faces[first_match_index]

                self.lock.blink(5,0,1)
                self.green.blink(1,0.3,3) # flash LED once for one second
                print("Recognized " + name)

                tki_avatar = self.cv2_to_tkinter(cv2.imread('dataset/' + name))
                self.screen.show_avatar(tki_avatar)
                return True
            else:
                self.green.blink(0.05, 0.05, 10)

        return False

s = Server()
