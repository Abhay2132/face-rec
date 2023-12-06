import sys
import threading
import time
import customtkinter as ctk
import addUser
import faceAPI.mainAPI
import ui_
from PIL import Image
import cv2
from pathlib import Path
from multiprocessing import Array, Process, Manager

sys.path.append("faceAPI")
from faceAPI import mainAPI

width, height = 800, 600


def setData(d):
    d['kill'] = False
    d['frame_processed'] = False
    d['frame'] = []
    d['data'] = ([],[])


def identifyFaces(_dict):
    from faceAPI import mainAPI
    mainAPI.FaceAPI.init()

    while True:
        time.sleep(0.004)
        # print("bg:", _dict['frame_processed'], ", data:", _dict['data'])
        if _dict['kill']:
            break
        if len(_dict['frame']) < 1 or (_dict['frame_processed']) :
            continue

        frame = _dict['frame']
        persons, locs = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
        if len(locs) > 0:
            _dict['data'] = (persons, locs)
        # print(persons, locs)
        _dict['frame_processed'] = True

class App(ctk.CTk):
    cam_h, cam_w = height, width
    lastTime = 0
    lastFpsTick = 0
    data = {"persons": [], "face_locations": []}
    lastFrame = False
    kill = False
    arr = [0, 0]
    frameRatio = 9/16

    # sharedArr = Array('i')
    faceAPIProcess = False
    lastLocations = ([], []) # (persons[], face_locations[])

    def openNewUserDialog(self):
        self.newUserDialog = addUser.App(self.cap)
        self.newUserDialog.mainloop()

    def stopThread(self):
        self.kill = True
        self.quit()

    def __init__(self):
        super().__init__()
        
        self.protocol("WM_DELETE_WINDOW", self.stopThread)
        self.geometry(str(width) + "x" + str(height))
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

        self.leftFrame.addImage.configure(command=self.openNewUserDialog)
        self.bind("<Configure>", self.on_resize)

        self.manager = Manager()
        self._dict = self.manager.dict()

        setData(self._dict)
        self.process = Process(target=identifyFaces, args=(self._dict,))

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        mainAPI.FaceAPI.init()
        self.process.start()
        self.update()
        return 0

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

        # return 0
        ret, frame = self.cap.read()

        self.frameRatio = frame.shape[0]/frame.shape[1]
        if ret:
            try:
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self._dict['frame'] = frame

                # print(self._dict)

                if(self._dict["frame_processed"]):
                    print("fg:", self._dict['frame_processed'], "data:", self._dict['data'])
                    self._dict["frame"] = frame
                    self.lastLocations = self._dict['data']
                    self._dict["frame_processed"] = False

                # (persons, face_locations) = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
                (persons, face_locations) = self.lastLocations

                # print(f"Persons:{persons},locs:{face_locations}")
                if(len(face_locations) > 0):
                    mainAPI.FaceAPI.drawBox(frame, face_locations, persons)

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

    def on_resize(self, event):
        w = self.mainFrame.winfo_width()
        h = self.frameRatio * w

        self.cam_h = h
        self.cam_w = w
        self.mainFrame.label.configure(height=h)  # , text=("width :" +str(self.mainFrame.winfo_width())+"px"))


if __name__ == "__main__":
    # ctk.set_default_color_theme("green")
    ctk.set_appearance_mode("light")
    app = App()
    app.after(2000, app.initCamera)
    app.mainloop()
