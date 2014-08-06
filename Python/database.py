#!/usr/bin/env python
# coding: utf8
import psycopg2

# Datenbank Verbindung
n1="imageindexer"	#database name
n2="imageindexer"	#database user
n3="vmpostgre01"		#host
n4="123456"		#password


############################################################

def write(dbquery):
    # DB verbindung aufbauen.
    try:
    	conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
    except:
	#TODO Meldung "Datenbankverbindung konnte nicht hergestellt werden"
	pass
    try:
    	cur = conn.cursor()
    	cur.execute(dbquery)
    	conn.commit()
    	cur.close()
    	conn.close()
    except:
	pass
	#TODO Meldung "Es konnte nicht in Datenbank geschrieben werden"

############################################################

def read(table, bedingung=""):
	try:
    		conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
	except:
		#TODO Meldung "Datenbankverbindung konnte nicht hergestellt werden"
		pass
	try:	
		cur = conn.cursor()
		cur.execute("SELECT * FROM " + table + " " + bedingung +";")
		#names = cur.description
		#value = cur.fetchall()
		columns = [column[0] for column in cur.description]
		results = []
		for row in cur.fetchall():
			results.append(dict(zip(columns, row)))
		cur.close()
		conn.close()
	except:
		#TODO Meldung " Es konnte nicht aus der Datenbank gelesen werden"
		pass
		results = False
	# DB Output to Dictionary
	return results
