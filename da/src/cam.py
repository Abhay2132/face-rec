from tkinter import *
import cv2 
import time
from PIL import Image, ImageTk 

vid = cv2.VideoCapture(0) 
width, height = 800, 400
# Set the width and height 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

app = Tk() 
app.bind('<Escape>', lambda e: app.quit()) 

label_widget = Label(app) 
label_widget.pack() 

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

lastTime = 0
lastFps = 0
def open_camera(): 
	_, frame = vid.read() 
	frame = cv2.flip(frame, 1)
	now = time.time()

	global lastTime
	global lastFps
	global fps
	if(now - lastFps >= 1):
		lastFps = now	
		tick = now - lastTime
		fpsCount = 1/tick
		fps.configure(text="FPS : "+str(int(fpsCount)))


	opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
	gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(4,4))
	for (x, y, w, h) in faces:
		cv2.rectangle(opencv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

	captured_image = Image.fromarray(opencv_image) 
	photo_image = ImageTk.PhotoImage(image=captured_image) 

	label_widget.photo_image = photo_image 
	label_widget.configure(image=photo_image) 
	label_widget.after(1, open_camera) 
	
	lastTime = now

# button1 = Button(app, text="Open Camera", command=open_camera) 
# button1.pack() 
label_widget.after(10, open_camera)

fps = Label(app,text="FPS : 0")
fps.pack()
app.mainloop() 
