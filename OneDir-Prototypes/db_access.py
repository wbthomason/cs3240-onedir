#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys

def connect():
	return mdb.connect('stardock.cs.virginia.edu', 'cs4720dhk3yt', 'fall2013', 'cs4720dhk3yt');

def create_account(email, password):
	db = connect()
	cur = db.cursor()
	
	create_new_user = "INSERT INTO local_users( email, password ) VALUES ( '%s', '%s' )" % ( email, password )
	cur.execute( create_new_user )
	db.commit()
	
def login(email, password):
	db = connect()
	cur = db.cursor()
	
	get_login = "SELECT password FROM local_users WHERE email='%s'" % (email)
	cur.execute( get_login )
	res = cur.fetchone()
	
	return password == res[0]
	
def get_dirs(email):
	db = connect()
	cur = db.cursor()
	
	get_dirs = "SELECT dirs FROM local_users WHERE email='%s'" % (email)
	cur.execute( get_dirs )
	res = cur.fetchone()
	
	return res[0].split(',')

def set_dirs(email, dirs):
	new_dirs = ""
	for i in range(len(dirs) - 1):
		new_dirs += dirs[i] + ','
	
	new_dirs += dirs[-1]
	
	db = connect()
	cur = db.cursor()
	
	update_dirs = "UPDATE local_users SET dirs='%s' WHERE email='%s'" % (new_dirs, email)
	cur.execute( update_dirs )
	db.commit()
	
def add_dir(email, dir):
	dirs = get_dirs(email)
	dirs.append(dir)
	
	set_dirs(email, dirs)
	
def get_files(email):
	db = connect()
	cur = db.cursor()
	
	get_files = "SELECT files FROM local_users WHERE email='%s'" % (email)
	cur.execute( get_files )
	res = cur.fetchone()
	
	return res[0].split(',')

try:
	#create_account("knox.dru@gmail.com", "password")
    if login("knox.dru@gmail.com", "password"):
		print get_dirs("knox.dru@gmail.com")
		set_dirs("knox.dru@gmail.com", ["test/dir"])
		print get_dirs("knox.dru@gmail.com")
		add_dir("knox.dru@gmail.com", "test2/dir2")
		print get_dirs("knox.dru@gmail.com")
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)