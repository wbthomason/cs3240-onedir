#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import bcrypt
import MySQLdb as mdb


def connect():
    return mdb.connect('stardock.cs.virginia.edu', 'cs4720dhk3yt', 'fall2013', 'cs4720dhk3yt')


def create_account(email, password, db):
    cur = db.cursor()

    create_new_user = "INSERT INTO local_users( email, password ) VALUES ( '%s', '%s' )" % ( email, password )
    cur.execute(create_new_user)
    db.commit()


def update_account(old_email, old_password, new_email, new_password, db):
    cur = db.cursor()

    update_user = "UPDATE local_users SET email='%s', password='%s' WHERE email='%s'" % (
    new_email, new_password, old_email)
    cur.execute(update_user)
    db.commit()
    return True


def delete_account(email, db):
    cur = db.cursor()

    delete_user = "DELETE FROM local_users WHERE email='%s'" % (email)
    cur.execute(delete_user)
    db.commit()
    return True


def login(email, password, db):
    cur = db.cursor()

    get_login = "SELECT password FROM local_users WHERE email='%s'" % (email)
    cur.execute(get_login)
    res = cur.fetchone()

    return bcrypt.hashpw(password, res[0]) == res[0]


def get_dirs(email, db):
    cur = db.cursor()

    get_dirs = "SELECT dirs FROM local_users WHERE email='%s'" % (email)
    cur.execute(get_dirs)
    res = cur.fetchone()

    try:
        return res[0].split(',')
    except:
        return []


def set_dirs(email, dirs, db):
    new_dirs = ""
    for i in range(len(dirs) - 1):
        new_dirs += dirs[i] + ','

    new_dirs += dirs[-1]

    cur = db.cursor()

    update_dirs = "UPDATE local_users SET dirs='%s' WHERE email='%s'" % (new_dirs, email)
    cur.execute(update_dirs)
    db.commit()


def get_id(email, db):
    cur = db.cursor()
    cur.execute("SELECT id FROM local_users WHERE email='%s'" % email)
    return cur.fetchone()[0]


def add_dir(email, dir, db):
    dirs = get_dirs(email, db)
    dirs.append(dir)

    set_dirs(email, dirs, db)


def get_files(email, db):
    cur = db.cursor()

    get_files = "SELECT files FROM local_users WHERE email='%s'" % (email)
    cur.execute(get_files)
    res = cur.fetchone()

    try:
        return res[0].split(',')
    except:
        return []


def add_file(email, filename, db):
    cur = db.cursor()
    file_list = "SELECT files FROM local_users WHERE email='%s'" % email
    cur.execute(file_list)
    res = cur.fetchone()
    all_files = "%s" % filename
    if res[0] is not None:
        all_files += "," + res[0]
    print "Adding %s for %s" % (all_files, email)
    file_add = "UPDATE local_users SET files='%s' WHERE email='%s'" % (all_files, email)
    cur.execute(file_add)
    db.commit()

# Admin commands

def list_users(db):
    cur = db.cursor()

    list_users = "SELECT email FROM local_users"
    cur.execute(list_users)

    users = []
    res = cur.fetchall()

    for row in res:
        users.append(row[0])

    return users


# Note: This won't work right now, because of the changed signatures
if __name__ == "__main__":
    loggedIn = False
    user = ""

    print "###################################################"
    print ""
    print "Welcome to the local user account management system! Type a command to begin."

    print ""
    print "###################################################"
    print ""

    print "Available commands:"
    print "create - creates a new local user account"
    print "login - logs in to a given local user account"
    print "logout - logs out of the current local user account"
    print "add [arg1] - [arg1] specifies whether to add a file ([arg1] = file) or directory ([arg1] = dir)"
    print "print [arg1] - [arg1] specifies whether to print all files ([arg1] = file) or all directories ([arg1] = dir)"

    print ""
    print "###################################################"
    while True:
        print ""
        input = raw_input("Enter a command: ").split()
        cmd = input[0]
        try:
            arg1 = input[1]
        except:
            arg1 = ""

        if cmd == "create":
            username = raw_input("Username: ")
            password = raw_input("Password: ")
            confirm = raw_input("Confirm Password: ")
            while password != confirm:
                print "Passwords do not match! Please try again."
                password = raw_input("Password: ")
                confirm = raw_input("Confirm Password: ")

            try:
                create_account(username, password)
                print "Account created!"

            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        elif cmd == "login":
            username = raw_input("Username: ")
            password = raw_input("Password: ")

            try:
                while not login(username, password):
                    print "Incorrect username or password! Please try again."
                    username = raw_input("Username: ")
                    password = raw_input("Password: ")

                print "Login successful!"
                loggedIn = True
                user = username

            except mdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        elif cmd == "logout":
            loggedIn = False
            user = ""

        elif cmd == "add":
            if loggedIn:
                if arg1 == "dir":
                    dirName = raw_input("Path: ")

                    try:
                        add_dir(user, dirName)
                        print "Directory added!"

                    except mdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])

                if arg1 == "file":
                    fileName = raw_input("Path: ")

                    try:
                        add_file(user, fileName)
                        print "File added!"

                    except mdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
            else:
                print "You must log in first."

        elif cmd == "print":
            if loggedIn:
                if arg1 == "dir":
                    try:
                        print get_dirs(user)

                    except mdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])

                if arg1 == "file":
                    try:
                        print get_files(user)

                    except mdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
            else:
                print "You must log in first."
        elif cmd == "quit":
            sys.exit()
