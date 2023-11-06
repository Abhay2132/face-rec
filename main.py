import sys
import threading
import time
import customtkinter as ctk
import ui_
from PIL import Image
import cv2
from pathlib import Path
from multiprocessing import Array , Process

sys.path.append("faceAPI")
from faceAPI import mainAPI

width, height = 800, 600


# Set the width and height 

class App(ctk.CTk):
    cam_h, cam_w = 800, 200
    lastTime = 0
    lastFpsTick = 0
    data = {"persons": [], "face_locations": []}
    lastFrame = False
    kill = False

    sharedArr = Array('i')
    faceAPIProcess = False

    def stopThread(self):
        self.kill = True
        self.quit()

    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.stopThread)
        self.geometry("800x400")
        self.title("Abhay")

        self.mainFrame = ui_.MainFrame(self)
        self.leftFrame = ui_.LeftFrame(self)
        self.rightFrame = ui_.RightFrame(self)

        self.grid_columnconfigure((0, 2), minsize=150);
        self.grid_columnconfigure(1, weight=1, minsize=500);
        self.grid_rowconfigure(0, minsize=150, weight=1);

        padx = 3
        pady = 6

        self.mainFrame.grid(padx=padx, pady=pady, row=0, column=1, sticky="nswe")
        self.leftFrame.grid(row=0, padx=padx, pady=pady, column=0, sticky="nswe")
        self.rightFrame.grid(row=0, padx=padx, pady=pady, column=2, sticky="nswe")

        self.bind("<Configure>", self.on_resize)

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.update()
        mainAPI.FaceAPI.init()
        # self.faceAPIThread = threading.Thread(target=App.identifyFaces, args=(self,))
        # self.faceAPIThread.start()

    def updateFPS(self):
        now = time.time()

        if int(now - self.lastFpsTick) >= 1:
            dt = (now - self.lastTime)
            fps = 1 / dt
            self.mainFrame.fps.configure(text='fps : ' + str(int(fps)))
            self.lastFpsTick = now

    def update(self):
        self.updateFPS()
        self.lastTime = time.time()

        ret, frame = self.cap.read()

        if ret:
            try:
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # (persons, face_locations) = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
                self.lastFrame = frame
                if len(self.data["face_locations"]) > 0:
                    mainAPI.FaceAPI.drawBox(frame, self.data["face_locations"], self.data["persons"])

                image = Image.fromarray(frame)
                image_obj = ctk.CTkImage(image, size=(self.cam_w, int(self.cam_h)))
                self.mainFrame.label.configure(text="", image=image_obj)
            except Exception as e:
                print("Error : ", e)
            finally:
                self.after(1, self.update)
        else:
            self.cap.release()
            self.mainFrame.label.destroy()
            self.quit()

    @staticmethod
    def identifyFaces(arr):
        while (not arr[2]):
            frame = arr[0]
            (persons, face_locations) = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
            arr[1] = (persons, face_locations)
            # time.sleep(0.01)

    def on_resize(self, event):
        # screen_height = event.height
        # screen_width = event.width
        # width = screen_width - 300
        w = self.mainFrame.winfo_width()
        h = 9 / 16 * w

        self.cam_h = h
        self.cam_w = w
        self.mainFrame.label.configure(height=h)  # , text=("width :" +str(self.mainFrame.winfo_width())+"px"))


if __name__ == "__main__":
    # ctk.set_default_color_theme("green")
    ctk.set_appearance_mode("light")
    app = App()
    app.after(2000, app.initCamera)
    app.mainloop()
