from math import ceil
import picamera
import sys
import argparse
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
	sleep(20)	# often time lag before you can upload to google drive

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

	parser = argparse.ArgumentParser(description="Raspberry Spy")
	parser.add_argument('-f', '--folder', help="Folder to store pictures", required=False, default="images")
	parser.add_argument('-m', '--minute', help="Frequency in minutes of pictures", required=False, default=-1)
	parser.add_argument('-t', '--time', help="Time during which camera will be activated every day (e.g. 10:00-21:00)", default=None)
	parser.add_argument('-u', '--upload', help="Upload to Google Drive", action='store_true', required=False, default=False)

	options = parser.parse_args(argv)

	if options.time is None:
		start = datetime.datetime.min
		end = datetime.datetime.max 
	else:
		start, end = [datetime.datetime.strptime(t, "%H:%M") for t in options.time.split("-")]

	if options.upload:
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
		folderId = findIdOfFolder(options.folder, drive)
	
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
		
		if dt < startTime or dt > endTime:
			print "Inactive. Will resume at %s" % startTime
			sleepTime = (startTime - dt).seconds + 1
			sleep(sleepTime)
			dt = datetime.datetime.now()
		
		fileName = snapPicture(camera, options.folder)
		if options.upload:
			uploadImage(fileName,folder, folderId,drive)
		
		if options.minute != -1:
			nextPicTime = dt + datetime.timedelta(minutes=startMin)
			print "Next picture at: %s" % (nextPicTime)
			sleepTime = (nextPicTime - datetime.datetime.now()).seconds
			sleep(sleepTime)
		else:
			break


if __name__ == "__main__":
	main(sys.argv[1:])
