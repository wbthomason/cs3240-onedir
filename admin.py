import requests

def update_user(old_email, new_email, new_password):
    url = "http://localhost:3240/user/update"
    args = {'command': 'change', 'old_email': old_email, 'new_email': new_email, 'new_password': new_password}

    r = requests.post(url, params=args)
    self.auth_key = r.json()['auth_key']
    if self.auth_key == 0:
        return False
    return True

def remove(email):
    url = "http://localhost:3240/user/update"
    args = {'command': 'remove', 'email': email}

    r = requests.post(url, params=args)
    self.auth_key = r.json()['auth_key']
    if self.auth_key == 0:
        return False
    return True

def list_users():
    url = "http://localhost:3240/user/update"
    args = {'command': 'users'}

    r = requests.post(url, params=args)
    return r.json()['users']

def list_files(email):
	url = "http://localhost:3240/user/update"
    args = {'command': 'files', 'email': email}

    r = requests.post(url, params=args)
    return r.json()['files']