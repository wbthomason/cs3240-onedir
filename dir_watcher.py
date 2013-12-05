from watchdog.events import FileSystemEventHandler
from file_transfer import *


class DirectoryWatcher(FileSystemEventHandler):
    def __init__(self, user, flag):
        FileSystemEventHandler.__init__(self)
        self.user = user
        self.flag = flag

    def on_created(self, event):
        if event.is_directory and not self.flag.is_set():
            upload_file(event.src_path, 0, self.user, True)

    def on_deleted(self, event):
        if not self.flag.is_set():
            file_delete(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and not self.flag.is_set():
            file_upload(event.src_path, self.user)
        else:
            # Do we need to handle directories?
            pass

    def on_moved(self, event):
        if not event.is_directory:
            file_delete(event.src_path)
            file_upload(event.dest_path, self.user)
        else:
            # Do we need to handle directories?
            pass