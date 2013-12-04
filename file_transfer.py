from urllib2 import HTTPError
import cStringIO

import requests
from Crypto.Hash import SHA512
import os

from add_file import *
import cryption


def check_updates(time, user):
    print "Checking server for updates"
    files = get_files(time, user)
    download_files(files, user)


def get_files(last_check, user):
    url = "http://localhost:3240/check"
    print "CHECKING AT TIME %f" % last_check
    args = {'email': user.email, 'last_check': float(last_check)}
    r = requests.get(url, params=args, verify=False)
    print r.json()
    files = r.json()
    return files


def download_files(files, user):
    h = SHA512.new()
    h.update(bytes(user.password))
    key = h.digest()[:32]
    for file_name in files:
        local_file = user.dir + file_name
        fileurl = "http://localhost:3240/files"
        print "downloading file " + file_name
        filereq = requests.get(fileurl, params={'filename': file_name, 'username': user.email}, stream=True,
                               verify=False)
        print "Downloading to: %s" % local_file
        dl_file = cStringIO.StringIO()
        #with open(local_file, 'wb') as dl_file:
        for chunk in filereq.iter_content(1024):
            dl_file.write(chunk)
        dl_file.seek(0)
        cryption.decrypt(key, local_file, dl_file)


def file_upload(file_path, user):
    try:
        file_size = os.stat(file_path).st_size
        print file_size
        upload_file(file_path, user)
        print file_path + " pushed to server"

    except HTTPError as e:
        print e.reason()


def file_delete(file_path, user):
    # Dummy Code
    print file_path + " removed from server"