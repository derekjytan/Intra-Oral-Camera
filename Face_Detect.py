##pip install opencv-python
##pip install opencv-python-headless


from tkinter import *
from tkinter.ttk import *
import numpy as np
import time
import picamera 
import picamera.array #New
import RPi.GPIO as GPIO 
import io
import datetime
import cv2  # Import OpenCV new

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)

# Camera setup
camera = picamera.PiCamera()
ON = True

window = Tk()
canvas = Canvas()

window.resizable(False, False)
window['background'] = '#2e3136'

# Variables
wScreen = window.winfo_screenwidth()
hScreen = window.winfo_screenheight()
w = wScreen
h = hScreen

zoom = 1.0
previewTime = 3

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#new

def centreWindow(w,h):
    x = 0
    y = 0
    window.geometry('%dx%d+%d+%d' % (w,h,x,y))
    print(x,y)

def preview():
    camera.preview_fullscreen = False
    camera.preview_window = (170, -120, 860, 950)  # Set dimensions
    camera.video_stabilization = True
    camera.start_preview()

def detect_faces(): #new
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        image = stream.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the image with detected faces
        cv2.imshow('Face Detection', image)
        cv2.waitKey(1)  # Show image for 1 ms

def zoomIn():
    global zoom
    if zoom >= 0.85:
        try:
            zoom -= 0.05
            x = (wScreen/2) - 0.5 * 500 * (1 - zoom)
            y = (hScreen/2) - 0.5 * 275 * (1 - zoom)
        except:
            x = (wScreen/2) - 0.5 * 500
            y = (hScreen/2) - 0.5 * 275
            zoom = 1
            pass
        camera.zoom = (x, y, zoom, zoom)
        print("Zoom", zoom * 100, "%")
    else:
        print("Max Zoom Reached!")
        zoom = 0.80
        x = (wScreen/2) - 0.5 * 500 * (1 - zoom)
        y = (hScreen/2) - 0.5 * 275 * (1 - zoom)
        camera.zoom = (x, y, zoom, zoom)
    
    zoom_text.config(text=f'Zoom Level: x{zoom:.2f}')
    preview()

def zoomOut():
    global zoom
    if zoom <= 0.95:
        try:
            zoom += 0.05
            x = (wScreen/2) - 0.5 * 500 * (1 - zoom)
            y = (hScreen/2) - 0.5 * 275 * (1 - zoom)
            camera.zoom = (x, y, zoom, zoom)
        except:
            x = (wScreen/2) - 0.5 * 500
            y = (hScreen/2) - 0.5 * 275
            zoom = 1
            pass
        print("Zoom", zoom * 100, "%")
    else:
        print("Min Zoom Reached!")
        zoom = 1.0
        x = (wScreen/2) - 0.5 * 500 * (1 - zoom)
        y = (hScreen/2) - 0.5 * 275 * (1 - zoom)
        camera.zoom = (x, y, zoom, zoom)
    
    zoom_text.config(text=f'Zoom Level: x{zoom:.2f}')
    preview()

camBright = camera.brightness
def brightUp():
    if camera.brightness < 100:
        camera.brightness += 5
    else:
        camera.brightness = 100
    camBright = camera.brightness
    bright_text.config(text=f'Brightness: {camBright}')
    preview()

def brightDown():
    if camera.brightness > 5:
        camera.brightness -= 5
    else:
        camera.brightness = 5
    camBright = camera.brightness
    bright_text.config(text=f'Brightess: {camBright}')
    preview()

camSat = 0
def satUp():
    if camera.saturation < 100:
        camera.saturation += 25
    else:
        camera.saturation = 100
    camSat = camera.saturation
    saturation_text.config(text=f'Saturation: {camSat}')
    preview()

def satDown():
    if camera.saturation > -100:
        camera.saturation -= 25
    else:
        camera.saturation = -100
    camSat = camera.saturation
    saturation_text.config(text=f'Saturation: {camSat}')
    preview()

camContrast = 0
def contrastUp():
    if camera.contrast < 100:
        camera.contrast += 10
    else:
        camera.contrast = 100
    camContrast = camera.contrast
    contrast_text.config(text=f'Contrast: {camContrast}')
    preview()

def contrastDown():
    if camera.contrast > -100:
        camera.contrast -= 10
    else:
        camera.contrast = -100
    camContrast = camera.contrast
    contrast_text.config(text=f'Contrast: {camContrast}')
    preview()

camSharp = 0
def sharpUp():
    if camera.sharpness < 100:
        camera.sharpness += 10
    else:
        camera.sharpness = 100
    camSharp = camera.sharpness
    sharp_text.config(text=f'Sharpness: {camSharp}')
    preview()

def sharpDown():
    if camera.sharpness > -100:
        camera.sharpness -= 10
    else:
        camera.sharpness = -100
    camSharp = camera.sharpness
    sharp_text.config(text=f'Sharpness: {camSharp}')
    preview()

picCount = 0
def still():
    global picCount
    camera.preview_fullscreen = False
    camera.preview_window = (170, -120, 860, 950)
    camera.start_preview()
    time.sleep(1)
    dT = datetime.datetime.now()
    strDT = dT.strftime("%d-%m-%y, %H-%M")
    camera.capture(f'/home/Jeffrey/Desktop/img{strDT}-{picCount:03d}.jpg')
    picCount += 1
    detect_faces() #new

vidCount = 0
def vid():
    global vidCount
    camera.preview_fullscreen = False
    camera.preview_window = (170, -120, 860, 950)
    camera.start_preview()
    dT = datetime.datetime.now()
    strDT = dT.strftime("%d-%m-%y, %H-%M")
    camera.start_recording(f'/home/Jeffrey/Desktop/vid{strDT}-{vidCount:03d}.h264')

    global recordingButton
    recordingButton = Button(text="End Video", height=3, width=15, command=stopRecording, bg="red")
    recordingButton.pack()
    recordingButton.place(x=((wScreen / 4) + 67.5), y=(hScreen * (2 / 3) + 165))

    global textRecording
    textRecording = Label(window, text="Recording in Progress", font=("Georgia", 15), bg="red")
    textRecording.place(x=50, y=(hScreen * (2 / 3)) + 140)

    vidCount += 1

def stopRecording():
    global recordingButton
    camera.stop_recording()
    recordingButton.destroy()
    global textRecording
    textRecording.destroy()

def stopProg():
    camera.stop_preview()
    quit()

# GUI setup
window.title("Raspberry Pi Intraoral Camera")
centreWindow(w,h)

preview()

zoomInButton = Button(text="+1", command=zoomIn, height=3, width=15)
zoomOutButton = Button(text="-1", command=zoomOut, height=3, width=15)
saturationUpButton = Button(text="+1", height=2, width=4, command=satUp)
saturationDownButton = Button(text="-1", height=2, width=4, command=satDown)
contrastUpButton = Button(text="+1", height=2, width=4, command=contrastUp)
contrastDownButton = Button(text="-1", height=2, width=4, command=contrastDown)
sharpnessUpButton = Button(text="+1", height=2, width=4, command=sharpUp)
sharpnessDownButton = Button(text="-1", height=2, width=4, command=sharpDown)
brightnessUpButton = Button(text="+1", height=2, width=4, command=brightUp)
brightnessDownButton = Button(text="-1", height=2, width=4, command=brightDown)
picButton = Button(text="Picture", height=3, width=15, command=still)
vidButton = Button(text="Video", height=3, width=15, command=vid)
endButton = Button(text="Quit", height=3, width=15, command=stopProg)

zoomInButton.pack()
zoomOutButton.pack()
saturationUpButton.pack()
saturationDownButton.pack()
contrastUpButton.pack()
contrastDownButton.pack()
sharpnessUpButton.pack()
sharpnessDownButton.pack()
brightnessUpButton.pack()
brightnessDownButton.pack()
picButton.pack()
vidButton.pack()
endButton.pack()

zoomInButton.place(x=((wScreen/4)-25), y=(hScreen*(2/3)+10))
zoomOutButton.place(x=((wScreen*(3/4))-155), y=(hScreen*(2/3)+10))
picButton.place(x=((wScreen*(3/4))-155), y=(hScreen*(2/3)+60))
vidButton.place(x=((wScreen*(3/4))-155), y=(hScreen*(2/3)+110))
endButton.place(x=((wScreen*(3/4))-155), y=(hScreen*(2/3)+160))

# Display text for various settings
zoom_text = Label(window, text=f'Zoom Level: x{zoom:.2f}', font=("Georgia", 15), bg="#2e3136", fg="white")
zoom_text.pack()
zoom_text.place(x=(wScreen*(3/4)-160), y=(hScreen*(2/3)-60))

bright_text = Label(window, text=f'Brightness: {camBright}', font=("Georgia", 15), bg="#2e3136", fg="white")
bright_text.pack()
bright_text.place(x=100, y=(hScreen*(2/3)-60))

saturation_text = Label(window, text=f'Saturation: {camSat}', font=("Georgia", 15), bg="#2e3136", fg="white")
saturation_text.pack()
saturation_text.place(x=100, y=(hScreen*(2/3)-40))

contrast_text = Label(window, text=f'Contrast: {camContrast}', font=("Georgia", 15), bg="#2e3136", fg="white")
contrast_text.pack()
contrast_text.place(x=100, y=(hScreen*(2/3)-20))

sharp_text = Label(window, text=f'Sharpness: {camSharp}', font=("Georgia", 15), bg="#2e3136", fg="white")
sharp_text.pack()
sharp_text.place(x=100, y=(hScreen*(2/3)))

window.mainloop()
