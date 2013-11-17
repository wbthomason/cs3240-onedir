import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from file_transfer import *

class DirectoryWatcher( FileSystemEventHandler ):
	def on_created(self, event):
		if not event.is_directory:
			file_upload(event.src_path)
		else:
			# Do we need to handle directories?
			pass

	def on_deleted(self, event):
		if not event.is_directory:
			file_delete(event.src_path)
		else:
			# Do we need to handle directories?
			pass
		

	def on_modified(self, event):
		if not event.is_directory:
			file_upload(event.src_path)
		else:
			# Do we need to handle directories?
			pass

	def on_moved(self, event):
		if not event.is_directory:
			file_delete(event.src_path)
			file_upload(event.dest_path)
		else:
			# Do we need to handle directories?
			pass