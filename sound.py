from scipy.signal import bilinear
import os
import errno
import pyaudio
from scipy.signal import lfilter
import numpy
from tkinter import *
from tkinter.ttk import *
from tk_tools import *
from tkinter import messagebox
import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
import ssl
from email.message import EmailMessage
import os
def send_mail_function2():
   
    email_sender = 'loc22drone@gmail.com'
    email_password = 'urhnzxrusokvtncc'
    email_receiver = 'shishirhebbar74799@gmail.com'
    subject = 'EMERGENCY'
    body = """"
    THERE IS A POSSIBILITY OF GUNSHOTS OF ABOVE 80 DECIBELS HEARD AT 36.13379407735641 LATITUDE AND 72.69994205020329 LONGITUDE
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

root = Tk()
root.title('Decibel Meter')
root.grid()
gaugedb = RotaryScale(root, max_value=120.0, unit=' dBA')
gaugedb.grid(column=1, row=1)
led = Led(root, size=50)
led.grid(column=3, row=1)
led.to_red(on=False)
Label(root, text='Too Loud').grid(column=3, row=0)
Label(root, text='Max').grid(column=2, row=0)
Label(root, text='Calibration (dB)').grid(column=4, row=0)
maxdb_display = SevenSegmentDigits(
    root, digits=3, digit_color='#00ff00', background='black')
maxdb_display.grid(column=2, row=1)
CHUNKS = [4096, 9600]
CHUNK = CHUNKS[1]
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATES = [44300, 48000]
RATE = RATES[1]
offset = StringVar()
offset.set('0')
spinbox = Spinbox(root, from_=-20, to=20,
                  textvariable=offset, state='readonly')
spinbox.grid(column=4, row=1)
appclosed = False


def close():
    global appclosed
    root.destroy()
    appclosed = True
    stream.stop_stream()
    stream.close()
    pa.terminate()


def A_weighting(fs):
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997

    NUMs = [(2*numpy.pi * f4)**2 * (10**(A1000/20)), 0, 0, 0, 0]
    DENs = numpy.polymul([1, 4*numpy.pi * f4, (2*numpy.pi * f4)**2],
                         [1, 4*numpy.pi * f1, (2*numpy.pi * f1)**2])
    DENs = numpy.polymul(numpy.polymul(DENs, [1, 2*numpy.pi * f3]),
                         [1, 2*numpy.pi * f2])
    return bilinear(NUMs, DENs, fs)


NUMERATOR, DENOMINATOR = A_weighting(RATE)


def rms_flat(a):
    return numpy.sqrt(numpy.mean(numpy.absolute(a)**2))


pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT,
                 channels=CHANNEL,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)


def update_max_if_new_is_larger_than_max(new, max):
    if new > max:
        return new
    else:
        return max


def listen(old=0, error_count=0, min_decibel=100, max_decibel=0):
    global appclosed
    while True:
        try:
            try:
                block = stream.read(CHUNK)
            except IOError as e:
                if not appclosed:
                    error_count += 1
                    messagebox.showerror(
                        "Error, ", " (%d) Error recording: %s" % (error_count, e))
            else:
                decoded_block = numpy.fromstring(block, numpy.int16)
                y = lfilter(NUMERATOR, DENOMINATOR, decoded_block)
                new_decibel = 20*numpy.log10(rms_flat(y))+int(offset.get())
                old = new_decibel
                gaugedb.set_value(float('{:.2f}'.format(new_decibel)))
                max_decibel = update_max_if_new_is_larger_than_max(
                    new_decibel, max_decibel)
                maxdb_display.set_value(str(int(float(str(max_decibel)))))
                if new_decibel > 80:
                    led.to_red(on=True)
                    print("Gun fire detected")
                    send_mail_function2()
                else:
                    led.to_red(on=False)
            root.update()
        except TclError:
            break


root.protocol('WM_DELETE_WINDOW', close)
listen()
