from tkinter import *
from tkinter.ttk import *
import myWeather as we
import rssParser as rp
import importlib
import datetime
from time import strptime
import re


class gui:

    def __init__(self, calendar):
        self.calendar = calendar

        #make root
        self.root1 = Tk()
        self.root1.title('Smart Mirror')
        self.root1.attributes("-fullscreen", True)
        self.root1['bg']="black"
        self.root1.attributes("-topmost", True)
        self.root1.bind("<Escape>", self.close)

        # Style options
        s=Style()
        s.configure('large.TLabel', background = 'black', font='verdana 20', foreground = 'white')
        s.configure('medium.TLabel', background = 'black', font='verdana 14', foreground = 'white')
        s.configure('small.TLabel', background = 'black', font='verdana 10', foreground = 'white')
        s.configure('description.TLabel', background = 'black', font='verdana 8', foreground = 'white')
        s.configure('smallDescription.TLabel', background = 'black', font='verdana 6', foreground = 'white')
        s.configure('imgCont.TFrame',background = 'black')

        self.calFrame = Frame(self.root1, style = 'imgCont.TFrame')
        self.calFrame.place(rely=0, relx=0, x=0, y=0, anchor=NW)
        self.newsFrame = Frame(self.root1, style = 'imgCont.TFrame')
        self.newsFrame.place(rely=1.0, relx=0, x=0, y=0, anchor=SW)
        self.weatherFrame= Frame(self.root1, style = 'imgCont.TFrame')
        self.weatherFrame.place(rely=0, relx=1.0, x=0, y=0, anchor=NE)
        
        self.makeClock()
        self.updateAll()
        self.makeLoading()
        

    def updateAll(self):
        self.makeWeather()
        self.makeNews()
        self.makeCalendar()
        self.lastUpdated = datetime.datetime.now()
        self.updated.configure(text = 'Last updated: ' + datetime.datetime.now().strftime("%I:%M:%S"))
        
    def close(self, *args):
        self.root1.destroy()

    def makeWeather(self):
        #clear frame
        self.destroyChildrenOf(self.weatherFrame)
        
        #weather frame
        weatherData = we.getWeather()

        tempNum = Label(self.weatherFrame, text=weatherData[0]['temp'] + '°', style = 'large.TLabel')
        tempNum.grid(row = 0, column = 0, sticky = 'NSE')

        path = "images//" + weatherData[0]['iconID']+".gif"
        photo = PhotoImage(file = path)
        # photo = photo.zoom(2,2)
        imgFrame = Frame(self.weatherFrame, style  = 'imgCont.TFrame')
        condImg = Label(imgFrame, image = photo, style = 'medium.TLabel')
        condImg.image = photo
        condImg.grid(sticky = 'EW')
        imgFrame.grid(row = 0, column = 1, sticky = 'NSEW')
        condFrame = Frame(self.weatherFrame, style  = 'imgCont.TFrame')
        condFrame.grid(row = 1, column = 0, columnspan = 2, sticky = 'EW')
        currConditions = Label(condFrame, text=weatherData[0]['conditions'], style = 'medium.TLabel', justify = 'center')
        currConditions.pack()

        for i in range(len(weatherData) - 1):
            forecastFrame = Frame(self.weatherFrame, style  = 'imgCont.TFrame')
            forecastFrame.grid(columnspan = 2, sticky = 'EW')

            forecast = weatherData[i+1]
            time = forecast['time'][-5:]
            temp = forecast['temp'] + '°'
            conds = forecast['conditions']
            path = "images//" + forecast['iconID'] + ".gif"
            photo = PhotoImage(file = path)
            photo = photo.subsample(2, 2)
            condImg = Label(forecastFrame, image = photo, style = 'medium.TLabel')
            condImg.image = photo
            condImg.grid(row = 0, column = 0)
            forecastLabel = Label(forecastFrame, text = time + ' | ' + temp + ' | ' + conds, style = 'small.TLabel')
            forecastLabel.grid(row = 0, column = 1, sticky = 'E')

    def makeNews(self):
        #News frame
        #clear frame
        self.destroyChildrenOf(self.newsFrame)

        newsTitle = Label(self.newsFrame, text = 'News | Politics', style = 'medium.TLabel')
        newsTitle.grid(row = 0, column = 0, sticky = 'NSEW')

        newsInfoFrame = Frame(self.newsFrame, style = 'imgCont.TFrame')
        newsInfoFrame.grid(row = 1, column = 0, sticky = 'EW')

        newsData = rp.parseFeed()
        for article in newsData:
            artTitle = Label(newsInfoFrame, text = '➤ ' + article['title'], style = 'description.TLabel', wraplength = self.root1.winfo_screenwidth()*(5/8), justify = 'left')
            artDesc = Label(newsInfoFrame, text = '↳' + article['description'], style = 'smallDescription.TLabel', wraplength = self.root1.winfo_screenwidth()*(5/8), justify = 'left')
            artTitle.grid(padx = 10, sticky = 'EW')
            artDesc.grid(padx = 33, sticky = 'EW')

    def makeCalendar(self):
        #clear frame
        self.destroyChildrenOf(self.calFrame)
        schedule = self.calendar.reload()

        self.futureSchedule = []
        for day in schedule:
            date = day['title']
            monthText = re.findall(r', (\w*) \d{1,2}', date)[0]
            currMonth = int(datetime.datetime.now().month)
            currDay = int(datetime.datetime.now().day)
            calMonth = strptime(monthText,'%B').tm_mon
            calDay = int(date[-2:])
            
            if calMonth > currMonth:
                self.futureSchedule.append(day)
            elif (calDay >= currDay and calMonth == currMonth):
                self.futureSchedule.append(day)
                
        calInfoFrame = Frame(self.calFrame, style = 'imgCont.TFrame')
        calInfoFrame.grid(row = 0, column = 0, sticky = 'EW')
        numDaysDisplayed = 5
        for day in self.futureSchedule[:numDaysDisplayed]:
            dayLabel = Label(calInfoFrame, text = '➤ ' + day['title'], style = 'description.TLabel')
            dayLabel.grid(sticky = 'EW')
            for event in day['events']:
                eventLabel = Label(calInfoFrame, text = event['time'] + ': ' + event['name'], style = 'smallDescription.TLabel')
                eventLabel.grid(padx = 23, sticky = 'EW')

    def makeLoading(self):
        self.loadingFrame = Frame(self.root1, style = 'imgCont.TFrame')
        self.loadingFrame.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)
        self.loadingText = Label(self.loadingFrame, style = 'description.TLabel')
        self.loadingText.grid()

    def makeClock(self):

        self.clockFrame = Frame(self.root1, style = 'imgCont.TFrame')
        self.updated = Label(self.clockFrame, style = 'smallDescription.TLabel', text = 'Last Updated: ')
        self.updated.grid()
        self.clock = Label(self.clockFrame, style = 'large.TLabel', text = datetime.datetime.now().strftime("%I:%M:%S"))
        self.clockFrame.place(rely=0,relx=0.5,anchor = N)
        self.clock.grid()
        self.date = Label(self.clockFrame, style = 'description.TLabel', text = datetime.datetime.now().strftime("%b %d"), justify = 'left')
        self.date.grid()

    def configText(self, widget, newText):
        widget.configure(text = newText)

    def destroyChildrenOf(self, parent):
        for child in parent.winfo_children():
            child.destroy()

    def updateClock(self):
        if (datetime.datetime.now() - self.lastUpdated).total_seconds() > 3600:
            self.updateAll()
            self.updated.configure(text = 'Last updated: ' + datetime.datetime.now().strftime("%I:%M:%S"))
        self.clock.configure(text = datetime.datetime.now().strftime("%I:%M:%S"))
        self.date.configure(text = datetime.datetime.now().strftime("%b %d"))
        self.root1.after(1000, self.updateClock)
    def addReminder(self, data):
        print(data)
        date = data[0] + ' ' + data[1]
        oclock = data[2]
        title = data[3]
        self.calendar.addReminder(title, date, oclock)
        self.makeCalendar()
        
    def launch(self):
        #show
        self.root1.focus_force()
        self.root1.after(1000,self.updateClock)
        self.root1.mainloop()
