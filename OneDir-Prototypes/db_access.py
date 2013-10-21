#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'password', 'testdb');

    cur = con.cursor()
    cur.execute("SELECT * FROM test")

    res = cur.fetchone()
    
    print res
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()