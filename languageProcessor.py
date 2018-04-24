import re
import datetime
from datetime import timedelta

transcription = 'remind me tomorrow morning to go to the gym'

if transcription[:9] == 'remind me':
    #setting a reminder
    time = re.findall(r'remind me (.*?) (?:to|that)',transcription)[0]

    #get current info
    now = datetime.datetime.now()
    currMonth = now.month
    currDay = now.day
    currHour = now.hour
    currMinute = now.minute

    #evaluate relative dates (month and day)
    if (('today' in time) | ('this' in time)):
        day = currDay
        month = currMonth
    elif 'tomorrow' in time:
        newTime =  now + timedelta(days = 1)
        day = newTime.day
        month = newTime.month
    # elif time.find('on ') != -1:
    #     a=1
    else:
        day = currDay
        month = currMonth

    #evaluate times
    if ('morning' in time):
        hour = '09'
        minute = '00'
    elif ('afternoon' in time):
        hour = '13'
        minute = '00'
    elif ('evening' in time):
        hour = '18'
        minute = '00'
    elif ('night' in time):
        hour = '21'
        minute = '00'

    action = re.findall(r'(?:to |that )(.*)',transcription)[0]
    parsedDate = 'Date: {1} {0} time: {2}{3} action: {4}'.format(day, month, hour, minute, action)
    print(parsedDate)
