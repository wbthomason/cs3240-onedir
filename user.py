import requests


class User():
    def __init__(self, email, password, dir):
        self.email = email
        self.password = password
        self.dir = dir
        self.auth_key = 0

    def create(self):
        url = "http://localhost:3240/user/create"
        args = {'email': self.email, 'passw': self.password}

        r = requests.post(url, params=args)
        
        return True

    def login(self):
        url = "http://localhost:3240/user/auth"
        args = {'email': self.email, 'passw': self.password}

        r = requests.post(url, params=args)
        self.auth_key = r.json()['auth_key']
        if self.auth_key == 0:
            return False
        return True

    def update(self, new_email, new_password):
        url = "http://localhost:3240/user/update"
        args = {'old_email': self.email, 'old_password': self.password, 'new_email': new_email, 'new_password': new_password}

        r = requests.post(url, params=args)
        self.auth_key = r.json()['auth_key']
        if self.auth_key == 0:
            return False
        return True

    def delete(self):
        url = "http://localhost:3240/user/delete"
        args = {'email': self.email, 'password': self.password}

        r = requests.post(url, params=args)
        return False

    def logout(self):
        self.auth_key = 0
        return True