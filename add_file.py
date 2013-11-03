from twisted.web import client

import requests
import db_access
import MySQLdb as mdb
import sys


def upload_file():
    url = 'http://posttestserver.com/post.php'
    files = {'file': open(sys.argv[1])}
    req = requests.post(url, files=files)

if __name__ == "__main__":
    try:
        if db_access.login("knox.dru@gmail.com", "password"):
            upload_file()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)