import requests


class User():
    def __init__(self, email, password, dir, addr):
        self.email = email
        self.password = password
        self.dir = dir
        self.auth_key = 0
        self.addr = addr

    def create(self, passhash):
        url = "http://%s:3240/user/create" % self.addr
        args = {'email': self.email, 'passw': passhash}

        requests.post(url, params=args, verify=False)

        return True

    def login(self):
        url = "http://%s:3240/user/auth" % self.addr
        args = {'email': self.email, 'passw': self.password}

        r = requests.post(url, params=args, verify=False)
        self.auth_key = r.json()['auth_key']
        if self.auth_key == 0:
            return False
        return True

    def update(self, new_email, new_password):
        url = "http://%s:3240/user/update" % self.addr
        args = {'old_email': self.email, 'old_password': self.password, 'new_email': new_email,
                'new_password': new_password}
        r = requests.post(url, params=args, verify=False)
        self.auth_key = r.json()['auth_key']
        if self.auth_key == 0:
            return False
        return True

    def delete(self):
        url = "http://%s:3240/user/delete" % self.addr
        args = {'email': self.email, 'password': self.password}

        requests.post(url, params=args, verify=False)
        return False

    def logout(self):
        self.auth_key = 0
        return True
