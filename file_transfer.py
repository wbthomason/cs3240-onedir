from urllib2 import HTTPError

import requests

from add_file import *


def check_updates(time, user):
    print "Checking server for updates"
    files = get_files(time, user)
    download_files(files, user)


def get_files(last_check, user):
    url = "http://localhost:3240/check"
    print "CHECKING AT TIME %f" % last_check
    args = {'email': user.email, 'last_check': float(last_check)}
    r = requests.get(url, params=args)
    print r.json()
    files = r.json()
    return files


def download_files(files, user):
    for file_name in files:
        local_file = user.dir + file_name
        fileurl = "http://localhost:3240/files"
        print "downloading file " + file_name
        filereq = requests.get(fileurl, params={'filename': file_name, 'username': user.email}, stream=True)
        print "Downloading to: %s" % local_file
        with open(local_file, 'wb') as dl_file:
            for chunk in filereq.iter_content(1024):
                dl_file.write(chunk)


def file_upload(file_path, user):
    try:
        upload_file(file_path, user)
        print file_path + " pushed to server"

    except HTTPError as e:
        print e.reason()


def file_delete(file_path, user):
    # Dummy Code
    print file_path + " removed from server"