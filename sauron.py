#!/usr/bin/env python

import sys
import time
import threading
from getpass import getpass

from watchdog.observers import Observer

from daemon import Daemon
from dir_watcher import DirectoryWatcher
from file_transfer import *
from user import User


class Sauron(Daemon):
    def __init__(self, user_data):
        Daemon.__init__(self, '/tmp/onedir.pid', sys.stdin, sys.stdout, sys.stderr)
        self.user = user_data
        self.last_check = 0.0

    def run(self):
        if not self.user.login():
            print "Invalid user"
            sys.exit(0)

        # Set up file watcher
        flag = threading.Event()
        flag.set()
        file_events = DirectoryWatcher(self.user, flag)
        dir_observer = Observer()
        dir_observer.schedule(file_events, path=self.user.dir, recursive=True)
        dir_observer.start()

        # Watch server for updates
        while True:
            flag.set()
            check_updates(self.last_check, self.user)
            # Necessary because of weird thing where the function seems to return before the work is done
            time.sleep(0.1)
            flag.clear()
            self.last_check = time.time()
            time.sleep(15)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        if 'start' == sys.argv[1]:
            email = raw_input("Email: ")
            password = getpass("Password: ")
            user = User(email, password, sys.argv[2])
            daemon = Sauron(user)
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon = Sauron(None)
            daemon.stop()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop with directory name" % sys.argv[0]
        sys.exit(2)