import time
import threading
import pyaudio
import speech_recognition as sr
import sys
sys.path.append('/home/pi/snowboycopy/snowboy/examples/Python3/')
import snowboydecoder
import os
import playSound
import languageProcessor

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
        if ((command == 'update now') | (command == 'update')):
            self.gui.configText(self.gui.loadingText, 'Updating All')  
            self.gui.updateAll()
        else:
            self.gui.configText(self.gui.loadingText, 'You said ' + command)  
        playSound.threadedSoundPlayer('down.wav')
        os.remove(fname)
        
    def detected_callback(self):
        playSound.threadedSoundPlayer('up.wav')
        self.gui.configText(self.gui.loadingText, 'Listening...')        

        