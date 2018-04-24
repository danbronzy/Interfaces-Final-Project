import time
import re
import random
import myCal
import datetime
from time import strptime


list = []
for i in range(10):
    s='remind me'
    times = [
    'at 3pm',
    'at 3pm on April 28',
    'in 3 hours',
    'in 30 minutes',
    'today at 6 pm',
    'this evening',
    'this night',
    'tomorrow',
    'tomorrow evening',
    'tomorrow at 9am',
    'on the 29th at 9am',
    'on the 18th'
    ]
    actions = [
    'to eat',
    'to go to the gym',
    'to call my home',
    'to get my stuff on friday',
    'that I need paper',
    'that I need to go to the gym',
    'to do that thing'
    ]
    list.append(' '.join([s,times[random.randrange(len(times))],actions[random.randrange(len(actions))]]))
a='remind me to'
a.find('asdasd')
a[:9]
list
for i in range(len(list)):
    print(re.findall(r'remind me (.*?) (?:to|that)',list[i])[0])
    print(re.findall(r'(?:to |that )(.*)',list[i])[0])

schedule = myCal.fakeGetWeek()
schedule
futureSchedule = []
for day in schedule:
    date = day['title']
    monthText = re.findall(r', (\w*) \d{1,2}', date)[0]
    if (strptime(monthText,'%B').tm_mon > int(datetime.datetime.now().month) or
        int(date[-2:]) >= int(datetime.datetime.now().day)):

        futureSchedule.append(day)

futureSchedule
