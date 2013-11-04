import requests

from db_access import *


class UserData:
    def __init__(self, uname, pword):
        self.username = str(uname)
        #Because eventually we shouldn't be storing passwords anywhere
        self.password_hash = str(pword)


class LoginError(BaseException):
    def __init__(self, reason):
        self.cause = str(reason)


def download_check(auth_data):
    if not login(auth_data.username, auth_data.password_hash):
        raise LoginError("Invalid Credentials")
    files = get_files(auth_data.username)
    for file in files:
        fileurl = "http://localhost:3240/%s" % file
        print fileurl
        filereq = requests.get(fileurl, stream=True)
        with open(file, 'wb') as dl_file:
            for chunk in filereq.iter_content(1024):
                dl_file.write(chunk)


if __name__ == "__main__":
    email = raw_input("Email: ")
    password = raw_input("Password: ")
    download_check(UserData(email, password))


