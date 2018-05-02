import myCal
from gtts import gTTS
import subprocess

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
    tts = gTTS(text = text, lang = 'en')
    tts.save('test123.mp3')
    subprocess.Popen(['omxplayer', '-o','local','test123.mp3'])


