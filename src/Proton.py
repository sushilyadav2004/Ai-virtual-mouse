import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbcontrol


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Proton, how may I help you?")

# Functions for system controls
def increase_volume():
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current + 0.1)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    reply(f"Volume increased to {int(new_volume * 100)} percent")

def decrease_volume():
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current - 0.1)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    reply(f"Volume decreased to {int(new_volume * 100)} percent")

def increase_brightness():
    current = sbcontrol.get_brightness(display=0)
    if isinstance(current, (list, tuple)):
        current = current[0] if current else 0
    new_brightness = min(100, current + 10)
    sbcontrol.fade_brightness(new_brightness, start=current)
    reply(f"Brightness increased to {new_brightness} percent")

def decrease_brightness():
    current = sbcontrol.get_brightness(display=0)
    if isinstance(current, (list, tuple)):
        current = current[0] if current else 0
    new_brightness = max(0, current - 10)
    sbcontrol.fade_brightness(new_brightness, start=current)
    reply(f"Brightness decreased to {new_brightness} percent")

def scroll_up():
    pyautogui.scroll(120)
    reply("Scrolled up")

def scroll_down():
    pyautogui.scroll(-120)
    reply("Scrolled down")

def scroll_left():
    pyautogui.hscroll(-120)
    reply("Scrolled left")

def scroll_right():
    pyautogui.hscroll(120)
    reply("Scrolled right")
# Audio to String
def record_audio():
    try:
        with sr.Microphone() as source:
            r.pause_threshold = 0.8
            voice_data = ''
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=5, timeout=5)

            voice_data = r.recognize_google(audio)
            print(f"You said: {voice_data}")
            return voice_data.lower()
    except sr.RequestError:
        print('Service is down')
        reply('Sorry my Service is down. Please check your Internet connection')
        return ''
    except sr.UnknownValueError:
        print('Could not understand audio')
        time.sleep(1)  # Add delay to prevent flooding logs
        return ''
    except sr.WaitTimeoutError:
        print('No speech detected')
        time.sleep(1)  # Add delay to prevent flooding logs
        return ''
    except Exception as e:
        print(f'Microphone error: {e}')
        return ''


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.replace('proton','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()
        
    
    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')

    elif 'stop' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        reply('Stopping Proton. Goodbye!')
        app.ChatBot.close()
        sys.exit()
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # System control commands
    elif 'increase volume' in voice_data or 'volume up' in voice_data:
        increase_volume()
        
    elif 'decrease volume' in voice_data or 'volume down' in voice_data:
        decrease_volume()
        
    elif 'increase brightness' in voice_data or 'brightness up' in voice_data:
        increase_brightness()
        
    elif 'decrease brightness' in voice_data or 'brightness down' in voice_data:
        decrease_brightness()
        
    elif 'scroll up' in voice_data:
        scroll_up()
        
    elif 'scroll down' in voice_data:
        scroll_down()
        
    elif 'scroll left' in voice_data:
        scroll_left()
        
    elif 'scroll right' in voice_data:
        scroll_right()
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()

# Voice assistance is ready - gesture recognition can be launched via voice command
reply('Voice assistance is active. Say "Proton Launch Gesture Recognition" to start gesture control.')

voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if voice_data and 'proton' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except Exception as e:
            print(f"Runtime exception while processing command: {e}")
            reply("An error occurred. Say 'exit', 'terminate', or 'stop' to close Proton.")
            continue
        


