import re
import datetime
from datetime import timedelta
from time import strptime

def transcribe(transcription):

    if transcription[:9] == 'remind me':
        #setting a reminder
        currTime = re.findall(r'remind me (.*?) (?:to|that)',transcription)[0]
        currTime
        #get current info
        now = datetime.datetime.now()
        currMonth = str(now.month)
        currDay = str(now.day)
        currHour = str(now.hour)
        currMinute = str(now.minute)
        month = currMonth
        day = currDay
        hour = currHour + currMinute

        if 'in ' in currTime: #travel in time x amounts of timeunit
            futureTime = now

            if 'minute' in currTime:
                numMins = re.findall(r'(\d*) minute', currTime)
                if numMins: futureTime = futureTime + timedelta(minutes = int(numMins[0]))
            if 'hour' in currTime:
                numHours = re.findall(r'(\d*) hour', currTime)
                if numHours: futureTime = futureTime + timedelta(hours = int(numHours[0]))
            if 'day' in currTime:
                numDays = re.findall(r'(\d*) day', currTime)
                if numDays: futureTime = futureTime + timedelta(days = int(numDays[0]))

            day = str(futureTime.day)
            month = str(futureTime.month)
            hour = str(futureTime.hour) + str(futureTime.minute)
        else:
            #evaluate relative dates (month and day)
            if (('today' in currTime) | ('this' in currTime) | ('tonight' in currTime)):
                day = currDay
                month = currMonth
            elif 'tomorrow' in currTime:
                newTime =  now + timedelta(days = 1)
                day = str(newTime.day)
                month = str(newTime.month)
            elif 'on ' in currTime:
                date = re.findall(r'on ([^at]*)', currTime)[0]
                monthText = date[:date.find(' ')]
                month = strptime(monthText,'%B').tm_mon
                day = date[date.find(' ')+1:]
            else:
                day = currDay
                month = currMonth

            #evaluate times
            if ('morning' in currTime):
                hour = '0900'
            elif ('afternoon' in currTime):
                hour = '1300'
            elif ('evening' in currTime):
                hour = '1800'
            elif (('night' in currTime) | ('tonight' in currTime)):
                hour = '2100'
            elif 'at ' in currTime:
                hour = re.findall(r'at ([^on]*)',currTime)[0]

        action = re.findall(r'(?:to |that )(.*)',transcription)[0]
        if re.findall('[0-9]{4}',hour):
            if int(hour[:2])<12:
                hour += 'am'
        parsedDate = 'Date: {1} {0} time: {2} action: {3}'.format(day, month, hour, action)
        return parsedDate
currTime = 'on april 18th'
re.findall(r'on ([^at]*)', currTime)
