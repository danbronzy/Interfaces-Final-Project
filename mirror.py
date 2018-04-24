import gui
import threadedListener
import myCal
import importlib

if __name__ == '__main__':

    importlib.reload(myCal)
    importlib.reload(threadedListener)
    importlib.reload(gui)

    calendar = myCal.myCal()
    GUI = gui.gui(calendar)
    listen = threadedListener.listener(GUI)
    GUI.launch()
