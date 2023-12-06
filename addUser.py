import customtkinter as ctk
import cv2
from PIL import Image
import os
from pathlib import Path
from datetime import datetime

cwd = os.sep.join(__file__.split(os.sep)[:-1])
width, height = 800, 600


# face_classifier = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def process_frame(_frame):
    frame = cv2.flip(_frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


class App(ctk.CTkFrame):
    cam_h, cam_w = height, width
    pause = False
    frameActive = False

    def onClose(self):
        self.cap.release()
        self.quit()

    def saveFrame(self):
        print("Saving Frame")
        self.form.saveButton.configure(state='disabled')

        id = str(self.form.input_id.get())
        name = str(self.form.input_name.get())

        if not id or not name:
            return print(f"id({id}) or name({name}) is invalid !")

        name = name.replace(" ", "_").lower()

        folderName = str(name) + "_" + str(id)
        folderDest = os.path.join(cwd, "faceAPI", "training", folderName)
        Path(folderDest).mkdir(exist_ok=True)

        filename = os.path.join(folderDest, getCurrentTime().replace(":", "_") + ".jpg")
        cv2.imwrite(filename, self.capturedFrame)

        self.form.saveButton.configure(text="Saved")
        print(f"Frame saved as '{filename}'")
        return 0

    def __init__(self, master):
        super().__init__(master)

        master.title("Add USER")
        self.frameActive = True
        self.master = master

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.cameraLabel = ctk.CTkLabel(master=self, fg_color="transparent")
        self.cameraLabel.grid(row=0, column=0, padx=10, pady=5, sticky='nswe')

        self.form = Form(self)
        self.form.grid(row=1, column=0, sticky='ns')

        self.form.captureButton.configure(command=self.captureFrame)
        self.form.saveButton.configure(command=self.saveFrame)

        self.after(1, self.init)

    def init(self):
        print("asking for videoCapture object from master")
        self.cap = self.master.getCap()
        print("cap", self.cap)
        self.update()

    def show(self):
        self.grid(row=0, column=0, sticky='nswe')

    def captureFrame(self):
        self.pause = not self.pause

        if not self.pause:
            self.form.captureButton.configure(text="Capture")
            self.form.saveButton.configure(state='disabled')

            return
        else:
            self.form.captureButton.configure(text="New")
        _, frame = self.cap.read()

        if _:
            try:
                self.capturedFrame = cv2.flip(frame, 1)
                id = self.form.input_id.get()
                name = self.form.input_name.get()
                print(f"id:{id},name:{name}")

                self.form.saveButton.configure(state='normal')
            except Exception as e:
                print("Error : ", e)

        self.form.saveButton.configure(text="Save")

    def update(self):
        if not self.frameActive:
            return

        if self.pause:
            self.after(1, self.update)
            return
        ret, _frame = self.cap.read()

        if ret:
            try:
                frame = process_frame(_frame)

                # gray_image = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
                # add_box(frame)
                image = Image.fromarray(frame)
                image_obj = ctk.CTkImage(image, size=(self.cam_w, int(self.cam_h)))
                self.cameraLabel.configure(text="", image=image_obj)
            except Exception as e:
                print("Error : ", e)
            finally:
                self.after(1, self.update)
        else:
            self.cap.release()
            self.cameraLabel.destroy()
            self.quit()


class Form(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")
        self.master = master
        self.input_id = ctk.CTkEntry(master=self, width=30, placeholder_text="ID")
        self.input_id.grid(row=0, column=0, sticky='ns', pady=8, padx=5)

        self.input_name = ctk.CTkEntry(master=self, placeholder_text="NAME")
        self.input_name.grid(row=0, column=1, sticky='ns', pady=8, padx=5)

        self.captureButton = ctk.CTkButton(master=self, text="Capture", width=100)
        self.captureButton.grid(row=0, column=2, sticky='e', padx=5, pady=8)

        self.saveButton = ctk.CTkButton(master=self, text='Save', state='disabled', width=100)
        self.saveButton.grid(row=0, column=3, sticky='', padx=5, pady=8)

        self.backButton = ctk.CTkButton(master=self, text='Back', width=100, command=self.goBack)
        self.backButton.grid(row=0, column=4, sticky='', padx=5, pady=8)

    def goBack(self):
        self.frameActive = False

        self.master.master.stopCap()
        self.master.master.setFrame("camera")


if __name__ == "__main__":
    root = ctk.CTk()
    root.getCap = lambda: cv2.VideoCapture(0)

    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.onClose)
    # root.geometry(str(width) + "x" + str(height))
    root.title("ADD USER")

    app.show()
    root.mainloop()
