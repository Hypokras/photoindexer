#!/usr/bin/env python
# coding: utf8
import psycopg2

# Datenbank Verbindung
n1="imageindexer"	#database name
n2="imageindexer"	#database user
n3="vmpostgre01"	#host
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
	value = []
	for x in tables:
		value.append(x[0])
	if not "photoindex" in value:
		# Die gewuenschten Tables erstellen.
		writescript("../PostgreSQL/photoindex_table.sql")
	if not "multiplephoto" in value:
		writescript("../PostgreSQL/multiplephoto_table.sql")
		#TODO Was wenn Script nicht ausgefuehrt werden kann?
	return tables

# Alter Table

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

# Write dict
# Schreibt Dictionary in Table test und kontrolliert ob Eintrag mehrmals vorhanden ist. Falls Ja timestamp und Image_Model in Table multiplephoto schreiben.

def writedict(dictionary):
	# Query aus dict erstellen
	columns = ""
	values = ""
	intvalues = ["Image_ExifOffset", "EXIF_SubjectDistanceRange", "EXIF_FlashPixVersion", "EXIF_ExifVersion", "EXIF_FocalLengthIn35mmFilm", "EXIF_InteroperabilityOffset", "Thumbnail_JPEGInterchangeFormat", "EXIF_ExifImageLength", "EXIF_CompressedBitsPerPixel", "EXIF_ExposureBiasValue", "Image_GPSInfo", "Thumbnail_JPEGInterchangeFormatLength", "EXIF_ExifImageWidth", "GPS_GPSAltitudeRef", "EXIF_FocalLength", "Image_XResolution", "EXIF_ISOSpeedRatings", "Image_YResolution", "Thumbnail_XResolution", "Thumbnail_YResolution"]
	timestamps = ["Image_DateTime", "EXIF_DateTimeOriginal", "EXIF_DateTimeDigitized"]
	for x in dictionary:
		y = x.replace(' ', '_')
		if str(dictionary[x]):
			columns = columns + y + ", "
			if y in intvalues:
				values = values + str(dictionary[x]) + ", "
			elif y in timestamps:
				controltimestamp = y
				controlvalue = "TIMESTAMP \'" + str(dictionary[x])[:4] + "-" + str(dictionary[x])[5:7] + "-" + str(dictionary[x])[8:] + "\', "
				values = values + controlvalue
			else:
				values = values + "\'" + str(dictionary[x]).replace('"', '\\"') + "\', "
	columns = columns[:len(columns) - 2]
	values = values[:len(values) - 2]
	query = "INSERT INTO TABLE test (" + columns + ") VALUES (" + values + ");"
	write(query)
	# Kontrolle, ob Eintrag schon in DB anhand eines Timestamp und Image_Model.
	# Wenn ja wird Timestamp und Image_Model in Table multiplephoto geschrieben.
	#TODO ueberpruefen ob timestamp und Image_Model vorhanden ist
	query = "SELECT id WHERE " + controltimestamp + " = " + controlvalue + " AND Image_Model = \'" + dictionary['Image Model'].replace('"', '\\"') + "\';"
	searchresult = readquery(query)
	if len(searchresult) == 0:
		# Konnte nicht in DB schreiben
		pass
	elif len(searchresult) == 1:
		# Eintrag ist nur ein Mal in DB
		pass
	else:
		# Eintrag ist mehrmals in DB
		# Timestamp und Image_Model in Table multiplephoto schreiben
		query = "INSERT INTO TABLE multiplephoto (" + controltimestamp + ", Image_Model) VALUES (" + controlvalue + ", \'" + dictionary['Image Model'].replace('"', '\\"') + "\');"
		write(query)
	return query
	
		
	










