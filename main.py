import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import pytesseract
from tkinter.scrolledtext import ScrolledText 
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title = window_title
        self.style = ThemedStyle(window)
        self.style.set_theme("breeze")
        self.video_source = video_source

        #open vid source
        self.vid = VideoCapture(video_source)

        #canvas for video render
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        
        self.btn_snapshot = ttk.Button(window, text="Scan", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.stext = ScrolledText(window, width=50, height=10)
        self.stext.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = 15
        self.update()

        self.window.mainloop()

    #loop to render frames continuosuly
    def update(self):

        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

    def snapshot(self):
        #get a frame from video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            custom_config = r'--oem 3 --psm 6'
            output_text = pytesseract.image_to_string(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), config = custom_config)
            print(output_text)
            self.stext.insert(tkinter.INSERT, output_text)
            self.stext.insert(tkinter.END, "___END___")
            

class VideoCapture:
    def __init__(self, video_source=0):
        #Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        #get the width and height of vid source
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    #Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                #this return a boolean success flag and the frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

App(tkinter.Tk(), "OCR Reader")
