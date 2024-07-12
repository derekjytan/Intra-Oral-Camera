from tkinter import Tk, Canvas, Button, Label, filedialog, messagebox
import numpy as np
import time
import picamera
import RPi.GPIO as GPIO
import io
import datetime

import board
from adafruit_as7341 import AS7341

#initialize colour sensor
i2c = board.I2C()
sensor = AS7341(i2c)

#Initializing camera
camera = picamera.PiCamera()
ON = True

#Initializing canvas
window = Tk()
canvas = Canvas()

#Window setup and background
window.resizable(False, False)
#window.configure(bg='white')
window['background']='#2e3136'

#VARIABLES#
wScreen = window.winfo_screenwidth()
hScreen = window.winfo_screenheight()

zoom = 1.0
camSat = 0
camContrast = 0
camSharp = 0
camBright=camera.brightness


def centreWindow(wScreen,hScreen):
    x=0
    y=0
    window.geometry(f'{wScreen}x{hScreen}+{x}+{y}')

def preview():
    camera.preview_fullscreen = False
    camera.preview_window = (50,0,1500,1000) # SET DIMENSIONS
    camera.video_stabilization = True
    camera.start_preview()

def zoomIn():
    global zoom
    if zoom >= 0.55:            
        zoom -= 0.05
        
    else:
        print("Max Zoom Reached!")
        zoom = 0.5
    camera.zoom = (0, 0, zoom, zoom)
    zoom_text.config(text=f'Zoom Level: x{zoom:.2f}')
    preview()
    
def zoomOut():
    global zoom
    if zoom <= 0.95:
        try:
            zoom += 0.05
        except:
            zoom = 1
        print("Zoom", zoom*100, "%")
    else:
        print("Min Zoom Reached!")
        zoom = 1.0
    camera.zoom = (0, 0, zoom, zoom)
    zoom_text.config(text=f'Zoom Level: x{zoom:.2f}')
    preview()
    

def brightUp():
    if camera.brightness < 100:
        camera.brightness += 5
    bright_text.config(text=f'Brightness: {camera.brightness}')
    preview()

def brightDown():
    if camera.brightness > 5:
        camera.brightness -= 5
    bright_text.config(text=f'Brightness: {camera.brightness}')
    preview()


def satUp():
    if camera.saturation < 100:
        camera.saturation += 25
    saturation_text.config(text=f'Saturation: {camera.saturation}')
    preview()

def satDown():
    if camera.saturation > -100:
        camera.saturation -= 25
    saturation_text.config(text=f'Saturation: {camera.saturation}')
    preview()

def contrastUp():
    if camera.contrast < 100:
        camera.contrast += 10
    contrast_text.config(text=f'Contrast: {camera.contrast}')
    preview()
    
def contrastDown():
    if camera.contrast > -100:
        camera.contrast -= 10
    contrast_text.config(text=f'Contrast: {camera.contrast}')
    preview()

def sharpUp():
    if camera.sharpness < 100:
        camera.sharpness += 10
    sharp_text.config(text=f'Sharpness: {camera.sharpness}')
    preview()
        
def sharpDown():
    if camera.sharpness > -100:
        camera.sharpness -= 10
    sharp_text.config(text=f'Sharpness: {camera.sharpness}')
    preview()

def still():
    camera.preview_fullscreen = False
    camera.preview_window = (170,-120,860,950)
    camera.start_preview() 
    time.sleep(2)
    camera.stop_preview()

    temp_path = '/tmp/temp_image.jpg'
    camera.capture(temp_path, use_video_port = True)
    
    wave_quantity = sensor.channel_630nm
    
    if wave_quantity > 150:
        circle.itemconfig(LED, fill='red')
    else :
        circle.itemconfig(LED, fill='green')
    window.update()
 
    save_path = filedialog.asksaveasfilename(
        title="Save Photo",
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
 
    if save_path:
        with open(temp_path, 'rb') as temp_file:
            with open(save_path, 'wb') as output_file:
                output_file.write(temp_file.read())
    
    circle.itemconfig(LED, fill='black')
    window.update()
    camera.start_preview()
    
temp_video_path = '/tmp/temp_video.h264'

def vid():
    camera.preview_fullscreen = False
    camera.preview_window = (170,-120,860,950)
    camera.start_preview()
    
    global temp_video_path
    camera.start_recording(temp_video_path)
    
    global recordingButton
    recordingButton = Button(text = "End Video",height = 3,width = 15,command=stopRecording,bg="red")
    recordingButton.pack()
    recordingButton.place(x=((wScreen/4)+67.5),y=(hScreen*(2/3)+165))
    
    global textRecording
    textRecording = Label(window, text="Recording in Progress",font=("Georgia",15),bg="red")
    textRecording.place(x=50,y=(hScreen*(2/3))+140)
        
   
def stopRecording():
    camera.stop_recording()
    camera.stop_preview()
    save_path = filedialog.asksaveasfilename(
        title="Save Video",
        defaultextension=".h264",
        filetypes=[("H.264 files", "*.h264"), ("All files", "*.*")]
    )

    global temp_video_path
    if save_path:
        with open(temp_video_path, 'rb') as temp_file:
            with open(save_path, 'wb') as output_file:
                output_file.write(temp_file.read())
        print(f"Video saved to {save_path}")
        
    global recordingButton
    recordingButton.destroy()
    
    global textRecording
    textRecording.destroy()
    
    camera.start_preview()
    
def stopProg():
    camera.stop_preview()
    quit()    
        
window.title("Raspberry Pi Intraoral Camera ")
centreWindow(wScreen,hScreen)

##BUTTONS##
preview()

zoomInButton = Button(text = "+1",command = zoomIn,height = 3,width = 15)
zoomOutButton = Button(text ="-1",command = zoomOut,height = 3, width = 15)
saturationUpButton = Button(text = "+1", height= 2, width=4, command = satUp)
saturationDownButton = Button(text = "-1", height= 2, width=4, command = satDown)
brightnessUpButton = Button(text = "+1", height= 2, width=4,command=brightUp)
brightnessDownButton = Button(text = "-1", height= 2, width=4,command=brightDown)
contrastUpButton = Button(text = "+1", height= 2, width=4,command=contrastUp)
contrastDownButton = Button(text = "-1", height= 2, width=4,command=contrastDown)
sharpnessUpButton = Button(text = "+1", height= 2, width=4,command=sharpUp)
sharpnessDownButton = Button(text = "-1", height= 2, width=4,command=sharpDown)
stillButton = Button(text = "Photo", height=3,width=15,command=still)
videoButton = Button(text = "Video", height=3,width=15,command=vid)
stopButton = Button(text = "STOP", height=3,width=15,command=stopProg, bg= "red")
    
    
##PACKING AND PLACING##
zoomInButton.pack()
zoomInButton.place(x=((wScreen/4)+550),y=(hScreen*(2/3)+165))

zoomOutButton.pack()
zoomOutButton.place(x=((wScreen/4)+405),y=(hScreen*(2/3)+165))

saturationUpButton.pack()
saturationUpButton.place(x=((wScreen/2)+850),y=100)

saturationDownButton.pack()
saturationDownButton.place(x=((wScreen/2)+780),y=100)

brightnessUpButton.pack()
brightnessUpButton.place(x=((wScreen/2)+850),y=150)

brightnessDownButton.pack()
brightnessDownButton.place(x=((wScreen/2)+780),y=150)
    
contrastUpButton.pack()
contrastUpButton.place(x=((wScreen/2)+850),y=200)

contrastDownButton.pack()
contrastDownButton.place(x=((wScreen/2)+780),y=200)

sharpnessUpButton.pack()
sharpnessUpButton.place(x=((wScreen/2)+850),y=250)
    
sharpnessDownButton.pack()
sharpnessDownButton.place(x=((wScreen/2)+780),y=250)
    
stillButton.pack()
stillButton.place(x=((wScreen/4)-67.5),y=(hScreen*(2/3)+165))

videoButton.pack()
videoButton.place(x=((wScreen/4)+67.5),y=(hScreen*(2/3)+165))

stopButton.pack()
stopButton.place(x=((wScreen/2)+705),y=(hScreen*(2/3)+165))

##TEXT##
text = Label(window, text="Saturation",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/2)+650,y=110)

text = Label(window, text="Brightness",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/2)+650,y=160)

text = Label(window, text="Contrast",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/2)+650,y=210)

text = Label(window, text="Sharpness",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/2)+650,y=260)

text = Label(window, text="Zoom",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/4)+325,y=(hScreen*(2/3))+177.5)

text = Label(window, text="Capture",font=("Georgia",15),fg="white",bg="#2e3136")
text.place(x=(wScreen/4)-160,y=(hScreen*(2/3))+177.5)

zoom_text = Label(window, text=f'Zoom Level: x{zoom}',font=('Georgia',15),bg='white')
zoom_text.place(x=1640,y=hScreen*(1/2)+5)

saturation_text = Label(window, text=f'Saturation: {camera.saturation}',font=("Georgia",15),bg="white")
saturation_text.place(x=1640,y=hScreen*(1/2)+101)

bright_text = Label(window, text=f'Brightness: {camera.brightness}',font=('Georgia',15),bg='white')
bright_text.place(x=1640,y=hScreen*(1/2)+29)

contrast_text = Label(window, text=f'Contrast: {camera.contrast}',font=('Georgia',15),bg='white')
contrast_text.place(x=1640,y=hScreen*(1/2)+53)

sharp_text = Label(window, text=f'Sharpness: {camera.sharpness}',font=("Georgia",15),bg="white")
sharp_text.place(x=1640,y=hScreen*(1/2)+77)


#SQUARE FOR SETTINGS
canvas.create_rectangle(2, 2,220,135, fill="white", outline = "black",width=2)
canvas.configure(bg="white",height=135,width=220)
canvas.place(x=1630,y=hScreen*(1/2)-2)

#fluorescense led
circle = Canvas(window, width=100, height=100, bg="#2e3136", highlightthickness=0)
circle.place(x=((wScreen/4)-170), y=(hScreen*(2/3)+165))
LED = circle.create_oval(0, 0, 60, 60, fill="black", outline="white", width=2)

window.mainloop()




