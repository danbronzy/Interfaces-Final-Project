from gtts import gTTS
import subprocess
import myWeather as wc
import datetime
from datetime import timedelta

def speakData(data):
    if data['type'] == 'schedule':
        if data['time'] == 'today':
            todaySched = data['content'][0]
            text = ''.join(todaySched['title'].split(',')) + '.'
            for event in todaySched['events']:
                text += 'At ' + ' '.join(event['time'].split(':')) + ',' + event['name']+ ':....'
        elif data['time'] == 'tomorrow':
            todaySched = data['content'][1]
            text = ''.join(todaySched['title'].split(',')) + '.'
            for event in todaySched['events']:
                text += 'At ' + ' '.join(event['time'].split(':')) + ',' + event['name']+ ':....'
    elif data['type'] == 'weather':
        text = '' 
        for day in data['content']:
            currTime = datetime.datetime.now()
            if day['time'] > currTime and day['time'] < (currTime + timedelta(days = 1)):
                if day['time'].hour in [7,8,9,12,13,14,17,18,19]:
                    oclock = datetime.datetime.strftime(day['time'],'%I %p')
                    cond = day['conditions'][day['conditions'].find(' '):]
                    temp = day['temp']
                    text += 'At ' + oclock + ' the weather is' + cond + ',and a temperature of ' + temp + ':'
    
    
    tts = gTTS(text = text, lang = 'en')
    tts.save('test123.mp3')
    subprocess.Popen(['omxplayer', '-o','local','test123.mp3'])          