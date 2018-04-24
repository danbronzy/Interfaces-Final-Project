import time
import threading
import pyaudio
import speech_recognition as sr
import re
import datetime
from datetime import timedelta

class listener(threading.Thread):

    def __init__(self, gui):

        self.gui = gui
        threading.Thread.__init__(self)
        self.daemon = True
        self.r = sr.Recognizer()
        self.r.energy_threshold = 1000;
        self.start()

    def run(self):

         while True:
            with sr.Microphone(None, 16000) as source:
                self.gui.configText(self.gui.loadingText, 'Listening...')
                audio = self.r.listen(source, None, 5.0)

            self.gui.configText(self.gui.loadingText, 'Thinking...')
            try:
                transcription = self.r.recognize_google(audio)
                self.gui.configText(self.gui.loadingText, 'You said: ' + transcription)
            except:
                transcription = ''
                self.gui.configText(self.gui.loadingText, 'There was an error transcribing')

            if transcription[:9] == 'remind me':
                #setting a reminder
                time = re.findall(r'remind me (.*?) (?:to|that)',transcription)[0]

                #get current info
                now = datetime.datetime.now()
                currMonth = now.month
                currDay = now.day
                currHour = now.hour
                currMinute = now.minute

                #evaluate relative dates
                if (time.find('today') != -1) | (time.find('this') != -1):
                    day = currDay
                    month = currMonth
                elif time.find('tomorrow') != -1:
                    newTime =  now + timedelta(days = 1)
                    day = newTime.day
                    month = newTime.month
                elif time.find('on ') != -1:
                    a=1
                else:
                    day = currDay
                    month = currMonth

                #evaluate times
                if (time.find('morning') != -1):
                    hour = '09'
                    minute = '00'
                elif (time.find('afternoon') != -1):
                    hour = '13'
                    minute = '00'
                elif (time.find('evening') != -1):
                    hour = '18'
                    minute = '00'
                elif (time.find('night') != -1):
                    hour = '21'
                    minute = '00'


                action = re.findall(r'(?:to |that )(.*)',list[i])[0]

            time.sleep(5)
