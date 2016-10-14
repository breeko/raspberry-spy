from crontab import CronTab
from subprocess import call
from time import strftime
from os import getcwd
from random import randint

class Camera(object):
	comment_prefix = "raspberry-spy-"

	def __init__(self, flip_vertical=False, flip_horizontal=False, rotate=0):
		self.flip_vertical = flip_vertical
		self.flip_horizontal = flip_horizontal
		self.rotate = rotate

	def new_job(self, folder=None, minute=None, hour=None, month=None, day_of_month=None, day_of_week=None):
		cron = CronTab(user=True)
		fileName = "%s.jpg" % (strftime("%Y-%m-%d %I.%M.%S %pe"))
		if folder is None:
			folder = "images"

		cmd = "raspistill -vf -hf -o %s/%s/$(date '+%%m-%%d-%%y_%%H:%%M:%%S').jpg" % (getcwd(), folder)
		
		if minute is None and hour is None and month is None and day_of_month is None and day_of_week is None:
			call(cmd)
			return None
		else:
			while True:
				cron_id = '%04d' % randint(0,9999)
				conflicting_cron_jobs = self.get_cron_job(cron_id)
				if len(conflicting_cron_jobs) == 0: break

			job = cron.new(command=cmd,comment="%s%s" % (self.comment_prefix, cron_id))

			if minute is None: minute = "*"
			if hour is None: hour = "*"
			if month is None: month = "*"
			if day_of_month is None: day_of_month = "*"
			if day_of_week is None: day_of_week = "*"
			job.setall(minute, hour, day_of_month, month, day_of_week)
			
			cron.write()
			return job

	def delete_job(self, cron_id=None):
		cron = CronTab(user=True)
		jobs = self.get_cron_job(cron_id, cron=cron)
		for job in jobs:
			cron.remove(job)
		cron.write()
		return jobs

	def get_cron_job(self, cron_id=None, cron = None):
		if cron is None:
			cron = CronTab(user=True)
		if cron_id is None:
			return [job for job in cron.find_command("raspistill")]
		return [job for job in cron.find_comment("%s%s" % (self.comment_prefix, cron_id))]