from math import ceil
import picamera
import sys
import getopt
import datetime
from time import strftime, sleep
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def findIdOfFolder(folderName, drive):
        fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in fileList:
                if file1['title'] == folderName:
                        return file1['id']
                

def snapPicture(camera, folder):
        fileName = "%s.jpg" % (strftime("%Y-%m-%d %I.%M.%S %p"))
        camera.capture('%s/%s' % (folder,fileName))
	print "image captured: %s/%s" % (folder,fileName)
        return fileName

def uploadImage(fileName, folder, folderId, drive):
        fileToUpload = drive.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': folderId}], 'title': 'image1.jpg'})
        fileToUpload.SetContentFile('%s/%s' % (folder,fileName))
        fileToUpload['title'] = fileName
	sleep(20)

	while True:
		try:
        		fileToUpload.Upload()
        		print "Successfully uploaded image %s" % (fileName)
			break
		except:
			print "Failed uploading image %s" % (fileName)
			sleep(10)
def timeAtNextMinute(roundMinute):
	tm = datetime.datetime.now()
    	upmins = ceil(float(tm.minute)/roundMinute)*roundMinute
    	diffmins = upmins - tm.minute
    	newtime = tm + datetime.timedelta(minutes=diffmins,microseconds=-tm.microsecond)
    	newtime = newtime.replace(second=0)
    	return newtime

def main(argv):
	startMin = -1
	upload = False
	start = datetime.datetime.min
	end = datetime.datetime.max
	folder = 'images'

	try:
		opts, args = getopt.getopt(argv,"huf:m:t:",['upload', "minute=", "time="])
	except getopt.GetoptError:
		print 'camera.py -f <folder> -m <round minute time to take picture> -t <start time - end time (e.g. 10:00-21:00)>'
	for opt, arg in opts:	
		if opt in ('-m', '-minute'):
			startMin = int(arg)
		elif opt in ('-t', '-time'):
			start, end = [datetime.datetime.strptime(t, "%H:%M") for t in arg.split("-")]
			print "camera will be activated daily between %02i:%02i and %02i:%02i" % (start.hour, start.minute, end.hour, end.minute)
		elif opt in ('-u', '-upload'):
			upload = True
		elif opt in ('-f', '-folder'):
			folder = arg

	if upload:
		gauth = GoogleAuth()
        	gauth.LoadCredentialsFile('mycreds.txt')
		if gauth.credentials is None:
        		gauth.LocalWebserverAuth()
        	elif gauth.access_token_expired:
                	gauth.Refresh()
        	else:
               		gauth.Authorize()
        	gauth.SaveCredentialsFile("mycreds.txt")

		drive = GoogleDrive(gauth)

        	folderId = findIdOfFolder(folder, drive)
	
	camera = picamera.PiCamera()
	camera.vflip = True
	camera.hflip = True

	while True:
		dt = datetime.datetime.now()
		startTime = dt.replace(hour=start.hour,minute=start.minute,second=0,microsecond=0)
		if startTime > dt:
			startTime += datetime.timedelta(days =- 1)
		secondsDiff = abs(min(end,start) - max(end,start)).seconds
		endTime = startTime + datetime.timedelta(seconds = secondsDiff)
		
		print "%s, %s" % (startTime, endTime)
		if dt < startTime or dt > endTime:
			print "Inactive. Will resume at %s" % startTime
			sleepTime = (startTime - dt).seconds
			sleep(sleepTime)
		
		fileName = snapPicture(camera, folder)
		if upload:
			uploadImage(fileName,folder, folderId,drive)
		
		if startMin != -1:
			# nextPicTime = timeAtNextMinute(startMin)
			nextPicTime = dt + datetime.timedelta(minutes=startMin)
			print "Next picture at: %s" % (nextPicTime)
			sleepTime = (nextPicTime - datetime.datetime.now()).seconds
			sleep(sleepTime)
		else:
			break


if __name__ == "__main__":
   main(sys.argv[1:])
