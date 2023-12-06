import sys
import threading
import time
import customtkinter as ctk
import addUser
import faceAPI.mainAPI
import ui_
from PIL import Image
import cv2
import os
from pathlib import Path
from multiprocessing import Array, Process, Manager
from datetime import datetime

cwd = os.sep.join(__file__.split(os.sep)[:-1])
Path(os.path.join(cwd, "reports")).mkdir(exist_ok=True)


# print("Current Time =", current_time)
def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


sys.path.append("faceAPI")
from faceAPI import mainAPI

width, height = 800, 600

cwd = os.sep.join(__file__.split(os.sep)[:-1])


def setData(d):
    d['kill'] = False
    d['frame_processed'] = False
    d['frame'] = []
    d['data'] = ([], [])


def identifyFaces(_dict):
    from faceAPI import mainAPI
    mainAPI.FaceAPI.init()

    while True:
        time.sleep(0.004)
        # print("bg:", _dict['frame_processed'], ", data:", _dict['data'])
        if _dict['kill']:
            break
        if len(_dict['frame']) < 1 or (_dict['frame_processed']):
            continue

        frame = _dict['frame']
        persons, locs = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
        if len(locs) > 0:
            _dict['data'] = (persons, locs)
        # print(persons, locs)
        _dict['frame_processed'] = True


class App(ctk.CTkFrame):
    lastTime = 0
    lastFpsTick = 0
    data = {"persons": [], "face_locations": []}
    lastFrame = False
    kill = False
    arr = [0, 0]
    frameRatio = 9 / 16
    frameActive = True

    # sharedArr = Array('i')
    faceAPIProcess = False
    lastLocations = ([], [])  # (persons[], face_locations[])
    savedPersons = set(mainAPI.SavedEncoding.getPersons())

    foundPersonsID = set()
    lastProcessedFrameAt = time.time()

    def onNewFace(self):
        return 0

    def openNewUserDialog(self):
        self.master.stopCap()
        self.master_.unbind("<Configure>")
        self.master_.onNewUserButtonClicked()
        self.frameActive = False

    def stopThread(self):
        self.kill = True
        self.quit()

    def __init__(self, master):
        super().__init__(master=master)
        self.cam_h = master.height
        self.cam_w = master.width
        master.title("Face-Mark : Attendance Perfected")
        self.master_ = master
        master.bind("<Configure>", self.on_resize)

        master.protocol("WM_DELETE_WINDOW", self.stopThread)
        # self.title("Abhay")

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

        self.manager = Manager()
        self._dict = self.manager.dict()

        setData(self._dict)
        self.process = Process(target=identifyFaces, args=(self._dict,))

        self.mainFrame.label.bind("<Button-1>", lambda *args: self.initCamera())
        self.rightFrame.reportButton.configure(command=self.save_report)
        self.leftFrame.trainBtn.configure(command=self.train)
        # self.after(200, self.initCamera)

    def _train(self):
        mainAPI.SavedEncoding.trainModel("hog")
        self.leftFrame.trainBtn.configure(text="Train", state="normal")
        mainAPI.SavedEncoding.loadEncoding()
        self.leftFrame.loadSavedPersons()

    def train(self):
        self.leftFrame.trainBtn.configure(text="Training ...", state="disabled")
        self.after(100, self._train)

    def initCamera(self):
        # self.mainFrame.label.configure(text="Starting Camera ...")
        self.cap = self.master_.getCap()
        mainAPI.FaceAPI.init()
        self.process.start()
        self.update()
        self.lastProcessedFrameAt = time.time()
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

        if not self.frameActive:
            return
        # return 0
        ret, frame = self.cap.read()

        self.frameRatio = frame.shape[0] / frame.shape[1]
        if ret:
            try:
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self._dict['frame'] = frame

                # print(self._dict)

                if (self._dict["frame_processed"]):
                    # print("fg:", self._dict['frame_processed'], "data:", self._dict['data'])
                    self.lastProcessedFrameAt = time.time()
                    print("data",self._dict["data"])
                    self._dict["frame"] = frame
                    self.lastLocations = self._dict['data']
                    self._dict["frame_processed"] = False
                    persons = self.lastLocations[0]
                    for (id, name) in persons:
                        if id == -1:
                            continue
                        if id not in self.foundPersonsID:
                            self.foundPersonsID.add(id)
                            self.rightFrame.userList.addUser(id, name)

                if (time.time() - self.lastProcessedFrameAt) > 3:
                    self.lastLocations = ([], [])
                # print("timeFrame", time.time()-self.lastProcessedFrameAt)
                # (persons, face_locations) = mainAPI.FaceAPI.identify(frame, mainAPI.SavedEncoding.encodings)
                (persons, face_locations) = self.lastLocations

                # print(f"Persons:{persons},locs:{face_locations}")
                if (len(face_locations) > 0):
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

    def open_popup(self, text="ALERT"):
        top = ctk.CTkToplevel(self)
        top.geometry("900x100")
        top.title("Child Window")
        ctk.CTkLabel(top, text=text).pack()

    def show(self):
        self.grid(row=0, column=0, sticky="nswe")

    def save_report(self):

        # if
        body = ""
        outputFile = os.path.join(cwd, "reports", getCurrentTime().replace(":", "_") + ".txt")
        for id in self.foundPersonsID:
            body += id + " "
        #
        with open(Path(outputFile), "w") as f:
            f.write(body)

        self.open_popup(f"REPORT GENERATED in './Report/{os.path.basename(outputFile)}' Directory")

    def on_resize(self, event):
        w = self.mainFrame.winfo_width()
        h = self.frameRatio * w

        self.cam_h = h
        self.cam_w = w
        self.mainFrame.label.configure(height=h)  # , text=("width :" +str(self.mainFrame.winfo_width())+"px"))


if __name__ == "__main__":
    # ctk.set_default_color_theme("green")

    ctk.set_appearance_mode("light")

    root = ctk.CTk()
    root.geometry(str(width) + "x" + str(height))
    root.title("Camera")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    app = App(root)
    app.show()

    root.mainloop()
