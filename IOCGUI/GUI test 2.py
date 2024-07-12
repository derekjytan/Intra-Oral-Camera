from tkinter import *
#from tkinter.ttk import *
import numpy as np
import time
import picamera
import RPi.GPIO as GPIO
import io
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)   
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)

##STUFF
camera = picamera.PiCamera()
ON = True

window = Tk()
canvas = Canvas()

window.resizable(False, False)
#window.configure(bg='white')
window['background']='#2e3136'

#~VARIABLES~#
wScreen = window.winfo_screenwidth()
hScreen = window.winfo_screenheight()
#w = 1000 #window width
#h = 550 #window height
w=wScreen
h=hScreen

zoom = 1.0
previewTime = 3;

def centreWindow(w,h):
    #x = (wScreen/2) - 500
    #y = (hScreen/2) - 285
    x=0
    y=0
    window.geometry('%dx%d+%d+%d' % (w,h,x,y))

    print(x,y)

def preview():
    camera.preview_fullscreen = False
    camera.preview_window = (50,0,1500,1000) # SET DIMENSIONS
    #camera.preview_window = (475,295,760,340) # SET DIMENSIONS
    camera.video_stabilization = True
    camera.start_preview()

def zoomIn():
    global zoom
    if zoom >= 0.85:
        try:
            zoom -= 0.05

            x = (wScreen/2) - 0.5 * 500/(1 - zoom)
            y = (hScreen/2) - 0.5 * 275/(1 - zoom)
            camera.zoom = (x, y, zoom, zoom)
        except:
            x = (wScreen/2) - 0.5 * 500
            y = (hScreen/2) - 0.5 * 275
            zoom = 1
            pass
       # camera.zoom = (x, y, zoom, zoom)
        print("Zoom", zoom*100, "%")

    else:
        print("Max Zoom Reached!")
        zoom = 0.80
        x = (wScreen/2) - 0.5 * 500/(1 - zoom)
        y = (hScreen/2) - 0.5 * 275/(1 - zoom)
        camera.zoom = (x, y, zoom, zoom)
        #print zoom somewhere
    
    text = Label(window, text=f'Zoom Level: x{zoom:.2f}',font=('Georgia',15),bg='white')
    text.place(x=1640,y=hScreen*(1/2)+5)
    preview()
    
def zoomOut():
    global zoom
    if zoom <= 0.95:
        try:
            zoom += 0.05
            x = (wScreen/2) - 0.5 * 500/(1-zoom)
            y = (hScreen/2) - 0.5 * 275/(1-zoom)
            camera.zoom = (x, y, zoom, zoom)
        except:
            x = (wScreen/2) - 0.5 * 500
            y = (hScreen/2) - 0.5 * 275
            zoom = 1
            pass
        #camera.zoom = (x, y, zoom, zoom)
        print("Zoom", zoom*100, "%")
    else:
        print("Min Zoom Reached!")
        zoom = 1.0
        x = (wScreen/2) - 0.5 * 500/(1-zoom)
        y = (hScreen/2) - 0.5 * 275/(1-zoom)
        camera.zoom = (x, y, zoom, zoom)
        #print zoom somewhere
        
    text = Label(window, text=f'Zoom Level: x{zoom:.2f}',font=('Georgia',15),bg='white')
    text.place(x=1640,y=hScreen*(1/2)+5)
    preview()
    

def brightUp():
    if camera.brightness < 100:
        camera.brightness += 5
    else:
        camera.brightness = 100
    preview()

def brightDown():
    if camera.brightness < 10:
        camera.brightness = 10
    else:
        camera.brightness -= 5
    preview()
    
def satUp():
    if camera.saturation < 100:
        camera.saturation += 25
    else:
        camera.saturation = 100
    preview()
    
def satDown():
    if camera.saturation > -100:
        camera.saturation -= 25
    else:
        camera.saturation = -100
    preview()
   
camContrast = 0

def contrastUp():
    if camera.contrast < 100:
        camera.contrast += 25
    else:
        camera.contrast = 100
    preview()
    print(camera.contrast)
    
def contrastDown():
    if camera.contrast > -100:
        camera.contrast -= 25
    else:
        camera.contrast = 100
    preview()
    print(camera.contrast)
    
def sharpUp():
    if camera.sharpness < 100:
        camera.sharpness += 25
    else:
        camera.sharpness = 100
    preview()
        
def sharpDown():
    if camera.sharpness > -100:
        camera.sharpness -= 25
    else:
        camera.sharpness = 100
    preview()

picCount=0

def still():
    global picCount
    camera.preview_fullscreen = False
    camera.preview_window = (170,-120,860,950)
    camera.start_preview()
    #GPIO.wait_for_edge(17, GPIO.FALLING) 
    time.sleep(1)
    dT=datetime.datetime.now()
    strDT=dT.strftime("%d-%m-%Y, %H-%M")
    camera.capture(f'/home/Jeffrey/Desktop/img{strDT}-{picCount:03d}.jpg')
    picCount+=1
    #camera.capture('/home/Jeffrey/Desktop/image{timestamp}-{counter:03d}.jpg')
    #camera.stop_preview()

vidCount = 0

def vid():
    global vidCount
    camera.preview_fullscreen = False
    camera.preview_window = (170,-120,860,950)
    camera.start_preview()
   # GPIO.wait_for_edge(17, GPIO.FALLING)
    #time.sleep(1)
    dT=datetime.datetime.now()
    strDT=dT.strftime("%d-%m-%Y, %H-%M")
    camera.start_recording(f'/home/Jeffrey/Desktop/vid{strDT}-{vidCount:03d}.h264')
    
    global recordingButton
    recordingButton = Button(text = "End Video",height = 3,width = 15,command=stopRecording,bg="red")
    recordingButton.pack()
    recordingButton.place(x=((wScreen/4)+67.5),y=(hScreen*(2/3)+165))
    
    global textRecording
    textRecording = Label(window, text="Recording in Progress",font=("Georgia",15),bg="red")
    textRecording.place(x=50,y=(hScreen*(2/3))+140)
        
    #time.sleep(3)
    vidCount+=1
    #GPIO.wait_for_edge(17, GPIO.FALLING)
    #camera.stop_recording()
   # camera.stop_preview()
   
def stopRecording():
    global recordingButton
    camera.stop_recording()
    recordingButton.destroy()
    global textRecording
    textRecording.destroy()
    
def stopProg():
    camera.stop_preview()
    quit()
    
#def recordLed():
    
        
##BUTTONS##
window.title("Raspberry Pi Intraoral Camera ")
centreWindow(w,h)

preview()

zoomInButton = Button(text = "+1",command = zoomIn,height = 3,width = 15)

zoomOutButton = Button(text ="-1",command = zoomOut,height = 3, width = 15)

saturationUpButton = Button(
    text = "+1", height= 2, width=4, command = satUp())

saturationDownButton = Button(
    text = "-1", height= 2, width=4, command = satDown())

brightnessUpButton = Button(
    text = "+1", height= 2, width=4,command=brightUp)

brightnessDownButton = Button(
    text = "-1", height= 2, width=4,command=brightDown)

contrastUpButton = Button(
    text = "+1", height= 2, width=4,command=contrastUp)

contrastDownButton = Button(
    text = "-1", height= 2, width=4,command=contrastDown)

sharpnessUpButton = Button(
    text = "+1", height= 2, width=4,command=sharpUp)

sharpnessDownButton = Button(
    text = "-1", height= 2, width=4,command=sharpDown)

stillButton = Button(
    text = "Photo", height=3,width=15,command=still)

videoButton = Button(
    text = "Video", height=3,width=15,command=vid)

stopButton = Button(
    text = "STOP", height=3,width=15,command=stopProg, bg= "red")
    
    
##PACKING SHIT##
zoomInButton.pack()
#zoomInButton.place(x=((1000/4)+67.5),y=(550*(2/3)))
zoomInButton.place(x=((wScreen/4)+550),y=(hScreen*(2/3)+165))

zoomOutButton.pack()
#zoomOutButton.place(x=((1000/4)-67.5),y=(550*(2/3)))
zoomOutButton.place(x=((wScreen/4)+405),y=(hScreen*(2/3)+165))

saturationUpButton.pack()
#saturationUpButton.place(x=((1000/2)+290),y=100)
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
#stillButton.place(x=((1000/4)-67.5),y=(550*(2/3)+65))
stillButton.place(x=((wScreen/4)-67.5),y=(hScreen*(2/3)+165))

videoButton.pack()
#videoButton.place(x=((1000/4)+67.5),y=(550*(2/3)+65))
videoButton.place(x=((wScreen/4)+67.5),y=(hScreen*(2/3)+165))

stopButton.pack()
stopButton.place(x=((wScreen/2)+705),y=(hScreen*(2/3)+165))

##TEXT##
text = Label(window, text="Saturation",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/2)+125,y=110)
text.place(x=(wScreen/2)+650,y=110)

text = Label(window, text="Brightness",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/2)+125,y=160)
text.place(x=(wScreen/2)+650,y=160)

text = Label(window, text="Contrast",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/2)+125,y=210)
text.place(x=(wScreen/2)+650,y=210)

text = Label(window, text="Sharpness",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/2)+125,y=260)
text.place(x=(wScreen/2)+650,y=260)

text = Label(window, text="Zoom",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/4)-140,y=(550*(2/3))+12.5)
text.place(x=(wScreen/4)+325,y=(hScreen*(2/3))+177.5)

text = Label(window, text="Capture",font=("Georgia",15),fg="white",bg="#2e3136")
#text.place(x=(1000/4)-150,y=(550*(2/3))+77.5)
text.place(x=(wScreen/4)-160,y=(hScreen*(2/3))+177.5)

text = Label(window, text=f'Zoom Level: x{zoom}',font=('Georgia',15),bg='white')
text.place(x=1640,y=hScreen*(1/2)+5)

text = Label(window, text=f"Saturation Level: {camera.saturation}",font=("Georgia",15),bg="white")
text.place(x=1640,y=hScreen*(1/2)+29)

text = Label(window, text=f'Contrast Level: {camera.contrast}',font=('Georgia',15),bg='white')
text.place(x=1640,y=hScreen*(1/2)+53)

text = Label(window, text=f"Sharpness Level: {camera.sharpness}",font=("Georgia",15),bg="white")
text.place(x=1640,y=hScreen*(1/2)+77)


#SQUARE FOR SETTINGS
canvas.create_rectangle(2, 2,220,112, fill="white", outline = "black",width=2)
canvas.configure(bg="white",height=111,width=220)
canvas.place(x=1630,y=hScreen*(1/2)-2)

window.mainloop()


