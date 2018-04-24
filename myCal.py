from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def getWeek(driver):
    events = [driver.find_elements_by_xpath("//div[@jsname='RjPD4e']//h2[@id ='tsc-%s']//..//div[@jscontroller = 'Bo3nHd']" % i) for i in range(7)]
    dayTitles = [driver.find_elements_by_xpath("//h2[@id ='tsc-%s']" % i)[0].text for i in range(7)]
    currWeek = []
    for dayOfEvents, dayTitle in zip(events, dayTitles):
        eventList = [{'time': x.text.split(',')[0], 'name': x.text.split(',')[1]} for x in dayOfEvents]
        currWeek.append({'title':dayTitle,'events':eventList})

    return currWeek

def fakeGetWeek(): #for debugging
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

class myCal:

    def __init__(self):
        fp = webdriver.FirefoxProfile('C:/Users/Fuck You Cortana/AppData/Roaming/Mozilla/Firefox/Profiles/1u4brv9j.autoTest')
        self.driver = webdriver.Firefox(fp)
        self.driver.get("https://calendar.google.com/calendar/r")
        time.sleep(2)
        self.schedule = self.getSchedule()

    def getSchedule(self):
        week1 = getWeek(self.driver)

        nextWeekButton = self.driver.find_element_by_xpath("//div[@class='mUbCce fKz7Od rF3YF EwnKv xEq6pc YTXdJe']")
        nextWeekButton.click()
        time.sleep(1)

        week2 = getWeek(self.driver)

        self.schedule = week1 + week2
        return self.schedule

    def addReminder(self, title, date, oclock):

        day = self.driver.find_element_by_xpath("//div[@jsname='RjPD4e']")
        day.click()
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
        return self.reload()

    def addEvent(self, title, date, startOclock, endOclock):
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
        titleBox.send_keys(Keys.ENTER)
        return self.reload()

    def reload(self):

        todayButton = self.driver.find_element_by_xpath("//div[@class='rbGOge SeRypc']//div[@jscontroller='VXdfxd']")
        todayButton.click()
        return self.getSchedule()
