import sys

import requests
import MySQLdb as mdb
from Crypto.Hash import SHA512

import cryption


def upload_file(file_name, file_size, user):
    h = SHA512.new()
    h.update(bytes(user.password))
    key = h.digest()[:32]
    url = 'http://localhost:3240/files'
    params = {'filename': file_name[len(user.dir):], 'username': user.email, 'filesize': file_size}
    #with open(file_name, 'rb') as put_file:
    put_file = cryption.encrypt(key, file_name)
    put_file.seek(0)
    req = requests.put(url, data=put_file, params=params, verify=False)
    req.raise_for_status()

if __name__ == "__main__":
    file_to_upload = raw_input("File to upload? ")
    try:
        upload_file(file_to_upload, 'test1')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)