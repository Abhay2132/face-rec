import customtkinter as ctk
import login
import camera

class App(ctk.CTk):
    _title = "LOGIN"
    _framesDict = {
        "login": login.Login,
        "camera": camera.App
    }
    _frameNames = list(_framesDict.keys())
    _currentFrame : ctk.CTkFrame = None

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

    def __init__(self):
        super().__init__()
        self.title(self._title)
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setFrame("login")
        
        # self._frame = login.Login(self)
        # self._frame.grid(row=0, column=0, sticky="nswe")


if __name__ == "__main__" :
    app = App()
    app.mainloop()