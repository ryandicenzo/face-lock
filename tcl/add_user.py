#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.24.1
#  in conjunction with Tcl version 8.6
#    Jul 12, 2019 06:52:35 PM PDT  platform: Windows NT

import sys

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

import add_user_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    add_user_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    add_user_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("435x584+1096+172")
        top.title("Facelock")
        top.configure(borderwidth="2")
        top.configure(background="#3f3f3f")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.name_input = tk.Text(top)
        self.name_input.place(relx=0.092, rely=0.788, relheight=0.058
                , relwidth=0.814)
        self.name_input.configure(background="white")
        self.name_input.configure(font="TkTextFont")
        self.name_input.configure(foreground="black")
        self.name_input.configure(highlightbackground="#d9d9d9")
        self.name_input.configure(highlightcolor="black")
        self.name_input.configure(insertbackground="black")
        self.name_input.configure(selectbackground="#c4c4c4")
        self.name_input.configure(selectforeground="black")
        self.name_input.configure(width=354)
        self.name_input.configure(wrap="word")

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.092, rely=0.736, height=19, width=36)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(borderwidth="3")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(text='''Name''')

        self.TButton2 = ttk.Button(top)
        self.TButton2.place(relx=0.092, rely=0.873, height=25, width=146)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Take Photo''')

        self.TButton1 = ttk.Button(top)
        self.TButton1.place(relx=0.575, rely=0.873, height=25, width=146)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Set as current user''')

        self.stream = tk.Label(top)
        self.stream.place(relx=0.092, rely=0.034, height=401, width=354)
        self.stream.configure(activebackground="#f9f9f9")
        self.stream.configure(activeforeground="black")
        self.stream.configure(background="#d9d9d9")
        self.stream.configure(disabledforeground="#a3a3a3")
        self.stream.configure(foreground="#000000")
        self.stream.configure(highlightbackground="#d9d9d9")
        self.stream.configure(highlightcolor="black")

if __name__ == '__main__':
    vp_start_gui()





