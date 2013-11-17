#!/usr/bin/env python

import sys, time
from daemon import Daemon
from dir_watcher import DirectoryWatcher
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_transfer import *
from user import User

class Sauron(Daemon):
	def __init__(self, directory, user):
		Daemon.__init__(self, '/tmp/daemon-example.pid', sys.stdin, sys.stdout, sys.stderr)
		self.dir = directory
		self.user = user
		self.last_check = None
	
	def run(self):
		if not self.user.login():
			print "Invalid user"
			sys.exit(0)
	
		# Set up file watcher
		file_events = DirectoryWatcher()
		dir_observer = Observer()
		dir_observer.schedule(file_events, path=self.dir, recursive=True)
		dir_observer.start()
		
		# Watch server for updates
		while True:
			time.sleep(15)
			self.last_check = time.clock()
			check_updates(self.last_check, self.user.auth_key)	

if __name__ == "__main__":
	if len(sys.argv) == 3:
		if 'start' == sys.argv[1]:
			email = raw_input("Email: ")
			password = raw_input("Password: ")
			user = User(email, password)
			
			daemon = Sauron(sys.argv[2], user)
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon = Sauron(sys.argv[2], None)
			daemon.stop()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop with directory name" % sys.argv[0]
		sys.exit(2)