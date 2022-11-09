from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import numpy as np
import argparse
import imutils
import cv2
import time
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
import ssl
from email.message import EmailMessage
import os
wi = Tk()
# Define the geometry of the window
wi.geometry("6000x5000")

frame = Frame(wi, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("image1.jpg"))

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)
label.pack()
def play_alarm_sound_function():  # defined function to play alarm post fire detection using threading
    # to play alarm # mp3 audio file is also provided with the code.
    playsound.playsound('fire_alarm.mp3', True)
    print("Fire alarm end")  # to print in consol

def send_mail_function():
   
    email_sender = 'loc22drone@gmail.com'
    email_password = 'urhnzxrusokvtncc'
    email_receiver = 'shishirhebbar74799@gmail.com'
    subject = 'EMERGENCY'
    body = """"
    TEST FIRE EMAIL
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def funct2():
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

def funct3():

    # To access xml file which includes positive and negative images of fire. (Trained images)
    fire_cascade = cv2.CascadeClassifier('C:\\Users\\Hp\\Documents\\git\\Fire_detection_python_project-main\\Fire_detection_python_project_git\\fire_detection_cascade_model.xml')
    # File is also provided with the code.

    # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
    vid = cv2.VideoCapture(0)
    runOnce = False  # created boolean

    while (True):
        Alarm_Status = False
        ret, frame = vid.read()  # Value in ret is True # To read video frame
        # To convert frame into gray color
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(
            frame, 1.2, 5)  # to provide frame resolution

        # to highlight fire with square
        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            print("Fire alarm initiated")
            # To call alarm thread
            threading.Thread(target=play_alarm_sound_function).start()

            if runOnce == False:
                print("Mail send initiated")
                # To call alarm thread
                threading.Thread(target=send_mail_function).start()
                runOnce = True
            if runOnce == True:
                print("Mail is already sent once")
                runOnce = True

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def func():
    wi1 = Tk()

    # Define the geometry of the window
    wi1.geometry("6000x5000")

    frame1 = Frame(wi1, width=600, height=400)
    frame1.pack()
    frame1.place(anchor='center', relx=0.5, rely=0.5)

    # Create an object of tkinter ImageTk
    img1 = ImageTk.PhotoImage(Image.open("image2.jpg"))

    # Create a Label Widget to display the text or Image
    label1 = Label(frame1,image=img1)
    label1.pack()

    #l2 = Label(wi1, text='').pack()
    lab2 = Label(wi1, text="Object detection",bg='Black', fg='White',font=('Arial',30)).place(x=610,y=50)
    bt2 = Button(wi1, text="obj",font=('Arial',20), command=funct2)
    bt2.place(x=720,y=110)

    #l3 = Label(wi1, text='').pack()
    lab3 = Label(wi1, text="Gun fire detection",bg='Black', fg='White',font=('Arial',30)).place(x=600,y=200)
    bt3 = Button(wi1, text="gun",font=('Arial',20), command=funct3)
    bt3.place(x=715,y=260)

    wi1.mainloop()

def funct1():
    
    video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("image.jpeg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while process_this_frame:
    # Grab a single frame of video
        ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

    # Only process every other frame of video to save time
        if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
                name = "Unmatched"

                if match[0]:
                    name = "Known Face"
                    wi.destroy()
                    func()
                    process_this_frame = False
                    #wi.mainloop()
        
                face_names.append(name)

        #process_this_frame = not process_this_frame


    # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 1
            right *= 1
            bottom *= 1
            left *= 1

        # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (51, 221, 82 ), 2)

        # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (51, 221, 82 ), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    

#myfont=font.Font(size=10)
#l1 = Label(wi, text=' ').pack()
lab1 = Label(wi, text="FACE UNLOCK",bg='Black', fg='White',font=('Arial',30)).place(x=610,y=50)
#lab1.place(relx=0.5,rely=0.5,anchor=CENTER)
bt1 = Button(wi, text="Click",font=('Arial',20), command=funct1)
bt1.place(x=710,y=110)
#bt1['font']=myfont

wi.mainloop()