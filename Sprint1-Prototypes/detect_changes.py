import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class OneDirEventHandler(FileSystemEventHandler):
	def on_created(self, event):
		print "Created %s" % event.src_path

	def on_deleted(self, event):
		print "Deleted %s" % event.src_path

	def on_modified(self, event):
		print "Modified %s" % event.src_path

	def on_moved(self, event):
		print "Moved %s to %s" % (event.src_path, event.dest_path)

if __name__ == '__main__':
	onedirEvents = OneDirEventHandler()
	onedirObserver = Observer()
	direc = raw_input("Path to directory to watch: ")
	onedirObserver.schedule(onedirEvents, path=direc, recursive=True)
	onedirObserver.start()

	while True:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			print "\nEnding..."
			onedirObserver.stop()
			onedirObserver.join()
			break