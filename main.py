import tkinter
import cv2

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title = window_title

        self.window.mainloop()

App(tkinter.Tk(), "OCR Reader")
