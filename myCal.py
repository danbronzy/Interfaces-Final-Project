from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

class myCal:

    def __init__(self):
        
        self.DEBUG = False
        
        if not self.DEBUG:
            options = Options()
            options.add_argument("-headless")
            fp = webdriver.FirefoxProfile('firefoxProfile')
            self.driver = webdriver.Firefox(firefox_profile = fp, options = options)
            self.driver.get("https://calendar.google.com/calendar/r")
            time.sleep(2)
        #self.schedule = self.getSchedule()

    def getSchedule(self):
        time.sleep(2)
        week1 = self.getWeek()

        nextWeekButton = self.driver.find_element_by_xpath("//div[@class='mUbCce fKz7Od rF3YF EwnKv xEq6pc YTXdJe']")
        nextWeekButton.click()
        time.sleep(1)

        week2 = self.getWeek()

        self.schedule = week1 + week2
        return self.schedule

    def addReminder(self, title, date, oclock):
        if self.DEBUG: return
        day = self.driver.find_element_by_xpath("//div[@jsname='RjPD4e']")
        day.click()
        time.sleep(3)#firefox was too slow on rPi
        reminderButton = self.driver.find_elements_by_xpath("//content[@class='kx3Hed']//span[@class='XSQHmd']")[1]
        time.sleep(.1) #avoids double click which just messes everything up
        reminderButton.click()
        dateBox = self.driver.find_elements_by_xpath("//input[@id='xStDaIn']")[1]
        dateBox.click()
        dateBox.send_keys(Keys.BACKSPACE)
        dateBox.send_keys(date)
        dateBox.send_keys(Keys.ENTER)
        timeBox = self.driver.find_elements_by_xpath("//input[@id='xStTiIn']")[1]
        timeBox.click()
        timeBox.send_keys(Keys.BACKSPACE)
        timeBox.send_keys(oclock)
        timeBox.send_keys(Keys.ENTER)
        titleBox = self.driver.find_element_by_xpath("//div[@class='aCsJod oJeWuf']//div[@class='aXBtI Wic03c']//div[@class='Xb9hP']//input[@class='whsOnd zHQkBf']")
        titleBox.send_keys(title)
        titleBox.send_keys(Keys.ENTER)


    def addEvent(self, title, date, startOclock, endOclock):
        if self.DEBUG: return
        day = self.driver.find_element_by_xpath("//div[@jsname='RjPD4e']")
        day.click()
        time.sleep(.1)
        dateBox = self.driver.find_elements_by_xpath("//input[@id='xStDaIn']")[0]
        dateBox.click()
        dateBox.send_keys(Keys.BACKSPACE)
        dateBox.send_keys(date)
        dateBox.send_keys(Keys.ENTER)
        timeBox1 = self.driver.find_element_by_xpath("//input[@id='xStTiIn']")
        timeBox1.click()
        timeBox1.send_keys(Keys.BACKSPACE)
        timeBox1.send_keys(startOclock)
        timeBox1.send_keys(Keys.ENTER)
        timeBox2 = self.driver.find_element_by_xpath("//input[@id='xEnTiIn']")
        timeBox2.click()
        timeBox2.send_keys(Keys.BACKSPACE)
        timeBox2.send_keys(endOclock)
        timeBox2.send_keys(Keys.ENTER)
        titleBox = self.driver.find_element_by_xpath("//div[@class='aCsJod oJeWuf']//div[@class='aXBtI Wic03c']//div[@class='Xb9hP']//input[@class='whsOnd zHQkBf']")
        titleBox.send_keys(title)


    def reload(self):
        if self.DEBUG: return self.fakeGetWeek()
        
        todayButton = self.driver.find_element_by_xpath("//div[@class='rbGOge SeRypc']//div[@jscontroller='VXdfxd']")
        todayButton.click()
        return self.getSchedule()
    
    def getWeek(self):
        events = [self.driver.find_elements_by_xpath("//div[@jsname='RjPD4e']//h2[@id ='tsc-%s']//..//div[@jscontroller = 'Bo3nHd']" % i) for i in range(7)]
        dayTitles = [self.driver.find_elements_by_xpath("//h2[@id ='tsc-%s']" % i)[0].text for i in range(7)]
        currWeek = []
        for dayOfEvents, dayTitle in zip(events, dayTitles):
            eventList = [{'time': x.text.split(',')[0], 'name': x.text.split(',')[1]} for x in dayOfEvents]
            currWeek.append({'title':dayTitle,'events':eventList})

        return currWeek
    
    def fakeGetWeek(self): #for debugging
        
        schedule = [{'events': [], 'title': 'No events, Sunday, April 22'},
                {'events': [{'name': ' Reminder: Get my laundry', 'time': '12:01pm'},
                {'name': ' Reminder: Get my suit dry-cleaned', 'time': '12:48pm'},
                {'name': ' work', 'time': '3:30pm to 4:30pm'}],
                'title': '3 events, Monday, April 23'},
                {'events': [{'name': ' go home', 'time': '11:30am to 12:30pm'},
                {'name': ' eat', 'time': '5pm to 6pm'}],
                'title': '2 events, Tuesday, April 24'},
                {'events': [{'name': ' Reminder: do someting', 'time': '12pm'},
                {'name': ' eat again?', 'time': '5:30pm to 6pm'}],
                'title': '2 events, Wednesday, April 25'},
                {'events': [], 'title': 'No events, Thursday, April 26'},
                {'events': [{'name': ' eat again!', 'time': '1:30pm to 2:30pm'}],
                'title': '1 event, Friday, April 27'},
                {'events': [], 'title': 'No events, Saturday, April 28'},
                {'events': [], 'title': 'No events, Sunday, April 29'},
                {'events': [], 'title': 'No events, Monday, April 30'},
                {'events': [{'name': ' Reminder: Take my account off Cox', 'time': '8am'}],
                'title': '1 event, Tuesday, May 1'},
                {'events': [], 'title': 'No events, Wednesday, May 2'},
                {'events': [], 'title': 'No events, Thursday, May 3'},
                {'events': [], 'title': 'No events, Friday, May 4'},
                {'events': [], 'title': 'No events, Saturday, May 5'}]
        return schedule
    
