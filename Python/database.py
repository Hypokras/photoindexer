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

def writescript(scriptpath):
    # DB verbindung aufbauen.
    try:
    	conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
    except:
	#TODO Meldung "Datenbankverbindung konnte nicht hergestellt werden"
	pass
    try:
    	cur = conn.cursor()
	cur.execute(open(scriptpath, "r").read())
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

############################################################

def readquery(query):
	try:
    		conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
	except:
		#TODO Meldung "Datenbankverbindung konnte nicht hergestellt werden"
		pass
	try:	
		cur = conn.cursor()
		cur.execute(query)
		result = cur.fetchall()
		cur.close()
		conn.close()
	except:
		#TODO Meldung " Es konnte nicht aus der Datenbank gelesen werden"
		pass
		result = False
	# DB Output to Dictionary
	return result

############################################################

# Datenbank initialisieren

def initdb():
	# Existieren die gewuenschten Table?
	query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
	tables = readquery(query)
	if not test in tables[0]:
		# Die gewuenschten Tables erstellen.
		writescript("../PostgreSQL/test_table.sql")
		#TODO Was wenn Script nicht ausgefuehrt werden kann?
	return True

def altertable(columns):
	# Table um Columns welche noch nicht existieren erweitern.
	#
	# Columns auslesen.
	query = "SELECT column_name FROM information_schema.columns WHERE table_name ='test';"
	result = readquery(query)
	oldcolumns = []
	for x in result:
		oldcolumns.append(str(x[0]))
	# Noch nicht vorhandene Columns erstellen
	oldcolumns = set(oldcolumns)
	columns = set(columns)
	newcolumns = list(columns - oldcolumns)
	for x in newcolumns:
		query = "ALTER TABLE test ADD COLUMN %s character varying;" % x
		write(query)
	return True
	
	
		
	










