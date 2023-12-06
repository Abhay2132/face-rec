import customtkinter as ctk
import cv2

import login
import camera
import addUser

class App(ctk.CTk):
    height , width =  600, 1000
    _title = "LOGIN"
    _framesDict = {
        "login": login.Login,
        "camera": camera.App,
        "addUser": addUser.App
    }
    _frameNames = list(_framesDict.keys())
    _currentFrame : ctk.CTkFrame = None
    cap = False
    capActive = False
    def setFrame(self, frameName):
        if not frameName in list(self._framesDict.keys()):
            raise Exception(f"frameName:{frameName} does not exists !")
            return 0
        
        if self._currentFrame:
            self._currentFrame.destroy()
        frame = self._framesDict.get(frameName)
        self._currentFrame = frame(self)
        self._currentFrame.show()

        return 0

    def onLogin(self):
        self.setFrame("camera")
        
    def onNewUserButtonClicked(self):
        self.setFrame("addUser")

    def __init__(self):
        super().__init__()
        self.title(self._title)
        self.geometry(str(self.width)+"x"+str(self.height))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setFrame("login")
        
        # self._frame = login.Login(self)
        # self._frame.grid(row=0, column=0, sticky="nswe")
        
    def getCap(self):
        if not self.capActive:
            self.cap = cv2.VideoCapture(0)
            self.capActive = True
        return self.cap

    def stopCap(self):
        if self.capActive:
            self.cap.release()
            self.capActive = False



if __name__ == "__main__" :
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()