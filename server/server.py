import os
import cv2
import face_recognition

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
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("941x400+615+126")
        top.title("Facelock")
        top.configure(borderwidth="2")
        top.configure(background="#e6f7ff")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.744, rely=0.825, height=24, width=107)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''New User''')

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=0.648, rely=0.075, relheight=0.708
                           , relwidth=0.301)
        self.Canvas1.configure(background="#d9d9d9")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.configure(width=283)

        self.Canvas2 = tk.Canvas(top)
        self.Canvas2.place(relx=0.032, rely=0.075, relheight=0.833
                           , relwidth=0.588)
        self.Canvas2.configure(background="#d9d9d9")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(highlightbackground="#d9d9d9")
        self.Canvas2.configure(highlightcolor="black")
        self.Canvas2.configure(insertbackground="black")
        self.Canvas2.configure(relief="ridge")
        self.Canvas2.configure(selectbackground="#c4c4c4")
        self.Canvas2.configure(selectforeground="black")
        self.Canvas2.configure(width=553)

class Server:
    host = 'http://192.168.0.7'
    port = 8000
    stream_url = 'stream.mjpg'

    def __init__(self):

        # initialize face encodings
        self.initKnownEncodings()

        url = self.host + ':' + str(self.port) + '/' + self.stream_url
        self.cap = cv2.VideoCapture(url)

        # initalize gpio / led
        self.green = LED(17)

        # only unlock door every (delay) seconds

        fps = 24
        delay = 3

        self.reset = fps * delay
        self.timer = 0

        self.vp_start_gui()


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

    def process_frame(self):

        ret, frame = self.cap.read()

        # cv2.imshow("img", frame)

        if (self.timer <= 0):
            if (self.find_approved_user(frame)):
                timer = self.reset
        else:
            self.timer -= 1

        if cv2.waitKey(1) == 27:
            exit(0)

        self.root.after(0, self.process_frame)



    def find_approved_user(self, frame):
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
                self.green.on()
                sleep(2)
                self.green.off()
                return True

        return False


    def vp_start_gui(self):
        '''Starting point when module is the main routine.'''
        global val, w, root
        self.root = tk.Tk()
        top = Toplevel1 (self.root)
        resting_state_support.init(self.root, top)

        self.root.mainloop()

    w = None
    def create_Toplevel1(self, root, *args, **kwargs):
        '''Starting point when module is imported by another program.'''
        global w, w_win, rt
        rt = root
        w = tk.Toplevel (root)
        top = Toplevel1 (w)
        resting_state_support.init(w, top, *args, **kwargs)
        return (w, top)

    def destroy_Toplevel1(self):
        global w
        w.destroy()
        w = None


s = Server()
