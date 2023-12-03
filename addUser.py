import customtkinter as ctk
import cv2
from PIL import Image

width, height = 800, 600

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def process_frame(_frame):
    frame = cv2.flip(_frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
def add_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(100, 100))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    # return faces

class App(ctk.CTk):
    cam_h, cam_w = height, width
    pause = False

    def onClose(self):
        self.cap.release()
        self.quit()

    def saveFrame(self):
        print("Saving Frame")
        return 0
    def __init__(self, cap):
        super().__init__()

        self.cap = cap
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        self.geometry(str(width) + "x" + str(height))
        self.title("ADD USER")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.cameraLabel = ctk.CTkLabel(master=self, fg_color="#333aaa")
        self.cameraLabel.grid(row=0, column=0, padx=10, pady=5, sticky='nswe')

        self.form = Form(self)
        self.form.grid(row=1, column=0, sticky='ns')

        self.form.captureButton.configure(command=self.captureFrame)
        self.form.saveButton.configure(command=self.saveFrame)



    def captureFrame(self):
        self.pause = True
        _, frame = self.cap.read()

        if _:
            try:
                self.capturedFrame = process_frame(frame)
                id = self.form.input_id.get()
                name = self.form.input_name.get()
                print(f"id:{id},name:{name}")

                self.form.saveButton.configure(state='normal')
            except Exception as e:
                print("Error : ", e)

    def update(self):
        if self.pause:
            self.after(1, self.update)
            return
        ret, _frame = self.cap.read()

        if ret:
            try:
                frame = process_frame(_frame)

                # gray_image = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
                add_box(frame)
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
        super().__init__(master=master, fg_color="#abbaab")

        self.input_id = ctk.CTkEntry(master=self, width=30, placeholder_text="ID")
        self.input_id.grid(row=0, column=0, sticky='ns', pady=8, padx=5)

        self.input_name = ctk.CTkEntry(master=self, placeholder_text="NAME")
        self.input_name.grid(row=0, column=1, sticky='ns', pady=8, padx=5)

        self.captureButton = ctk.CTkButton(master=self, text="Capture")
        self.captureButton.grid(row=0, column=2, sticky='e', padx=5, pady=8)

        self.saveButton = ctk.CTkButton(master=self, text='Save', state='disabled')
        self.saveButton.grid(row=0, column=3, sticky='ns', padx=5, pady=8)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    app = App(cap)
    app.after(1, app.update)
    app.mainloop()
