import time
import threading
import pyaudio
import speech_recognition as sr
import sys
sys.path.append('/home/pi/snowboycopy/snowboy/examples/Python3/')
import snowboydecoder
import os
#import playSound
import languageProcessor
import subprocess
import dataSpeaker

class listener(threading.Thread):

    def __init__(self, gui):
        
        self.gui = gui
        threading.Thread.__init__(self)
        self.daemon = True
        self.r = sr.Recognizer()
        self.r.energy_threshold = 1000;
        self.start()

    def run(self):
        self.gui.configText(self.gui.loadingText, 'Say \'Smart Mirror\' to get started')
        detector = snowboydecoder.HotwordDetector("smart_mirror.pmdl", sensitivity=0.5, audio_gain=1)
        detector.start(detected_callback = self.detected_callback, audio_recorder_callback = self.audio_recorder_callback)
        
    def audio_recorder_callback(self, fname):
        self.gui.configText(self.gui.loadingText, "Thinking...")
        with sr.AudioFile(fname) as src:
            audio = self.r.record(src)
        
        try:
            transcription = self.r.recognize_google(audio)
        except sr.UnknownValueError:
            self.gui.configText(self.gui.loadingText, "You talk funny, try again idiot")
        except sr.RequestError:
            self.gui.configText(self.gui.loadingText, "Google sucks and messed up")
        command = languageProcessor.evaluate(transcription)
        if (command['command'] == 'update'):
            self.gui.configText(self.gui.loadingText, 'Updating All')  
            self.gui.updateAll()
        elif command['command'] == 'reminder':
            parsedDate = 'Date: {0} {1} time: {2} action: {3}'.format(*command['data'])
            self.gui.configText(self.gui.loadingText, 'Adding Reminder | ' + parsedDate)
            self.gui.addReminder(command['data'])
        elif command['command'] == 'exit':
            self.gui.close()
        elif command['command'] == 'repeat schedule':
            dataSpeaker.speakData({'type':'schedule','time':command['data'],'content':self.gui.futureSchedule})
        
        elif command['command'] == 'unknown':
            self.gui.configText(self.gui.loadingText, 'Command Unknown. You said ' + command['data'])  
        
        
        #playSound.threadedSoundPlayer('down.wav')
        subprocess.Popen(['omxplayer', '-o','local','down.wav'])
        os.remove(fname)
        
    def detected_callback(self):
        #playSound.threadedSoundPlayer('up.wav')
        subprocess.Popen(['omxplayer', '-o','local','up.wav'])
        self.gui.configText(self.gui.loadingText, 'Listening...')        

        