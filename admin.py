import requests

def update_user(admin_password, old_email, new_email, new_password):
    url = "http://localhost:3240/user/admin"
    args = {'password': admin_password, 'command': 'change', 'old_email': old_email, 'new_email': new_email, 'new_password': new_password}

    r = requests.post(url, params=args)
    return True

def remove(admin_password, email):
    url = "http://localhost:3240/user/admin"
    args = {'password': admin_password, 'command': 'remove', 'email': email}

    r = requests.post(url, params=args)
    return True

def list_users(admin_password):
    url = "http://localhost:3240/user/admin"
    args = {'password': admin_password, 'command': 'users'}

    r = requests.post(url, params=args)
    return r.json()['users']

def list_files(admin_password, email):
    url = "http://localhost:3240/user/admin"
    args = {'password': admin_password, 'command': 'files', 'email': email}

    r = requests.post(url, params=args)
    return r.json()['files']