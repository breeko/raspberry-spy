from math import ceil
#import picamera
import sys
import argparse
import datetime
from time import strftime, sleep
import threading

class Camera(object):
    
    def capture(self, filename):
        print "snap!"
#        self.camera.capture(filename)
    
    def getActions(self, actionID=None):
        actions = []
        threads = [thread for thread in self.threads if actionID is None or thread.threadID == actionID]
        for thread in threads:
            action = {
                'id': thread.threadID,
                'time': thread.time,
                'minutes': thread.minutes,
                'folder': thread.folder,
                'active': thread.active,
                'started': thread.started,
                'completed': thread.completed
                }
            actions.append(action)
        return actions

    def snapPicture(self, folder=None, time=None, minutes=None):
        if folder is None:
            folder = self.folder
        thread = CameraThread(len(self.threads)+1, folder=folder, camera=self, time=time, minutes=minutes)
        thread.start()
        self.threads.append(thread)
        return thread
        
    def stopActions(self, actionIDs):
        threadsToStop = [thread for thread in self.threads if thread.threadID == actionIDs]
        for thread in threadsToStop:
            thread.active = False
    
    def __init__(self, folder='images'):
        self.folder = folder
        self.threads = []
#        self.camera = picamera.PiCamera()
#        self.camera.vflip = True
#        self.camera.hflip = True

class CameraThread(threading.Thread):
    def __init__(self, threadID, folder, camera, time=None, minutes=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.time = time
        self.minutes = minutes
        self.folder = folder
        self.camera = camera
        self.active = True
        self.started = datetime.datetime.now()
        self.completed = None
        
    def run(self):
        print "Starting " + self.name
        if self.time is None:
            start = datetime.datetime.min
            end = datetime.datetime.max 
        else:
            start, end = [datetime.datetime.strptime(t, "%H:%M") for t in self.time.split("-")]

        while True:
            dt = datetime.datetime.now()
            startTime = dt.replace(hour=start.hour,minute=start.minute,second=0,microsecond=0)
            if startTime > dt:
                startTime += datetime.timedelta(days =- 1)
            secondsDiff = abs(min(end,start) - max(end,start)).seconds
            endTime = startTime + datetime.timedelta(seconds = secondsDiff)

            if dt < startTime or dt > endTime:
                sleepTime = (startTime - dt).seconds + 1
                for second in range(sleepTime):
                    if self.active:
                        sleep(1)
                    else:
                        self.endThread()
                        return
                dt = datetime.datetime.now()

            # snap picture
            fileName = "%s.jpg" % (strftime("%Y-%m-%d %I.%M.%S %p"))
            self.camera.capture('%s/%s' % (self.folder,fileName))

            if self.minutes is not None:
                # repeat
                nextPicTime = dt + datetime.timedelta(minutes=self.minutes)
                print "Next picture at: %s" % (nextPicTime)
                sleepTime = (nextPicTime - datetime.datetime.now()).seconds
                for second in range(sleepTime):
                    if self.active:
                        sleep(1)
                    else:
                        self.endThread()
                        return
            else:
                self.endThread()
                return

    def endThread(self):
        self.camera.stopActions([self])
        self.active = False
        self.completed = datetime.datetime.now()