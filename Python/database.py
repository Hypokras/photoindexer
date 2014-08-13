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
	return [101, "Datenbankverbindung konnte nicht hergestellt werden\n"]
    try:
    	cur = conn.cursor()
    	cur.execute(dbquery)
    	conn.commit()
    	cur.close()
    	conn.close()
    except:
	return [102, "Es konnte nicht in Datenbank geschrieben werden\n"]
    return [200, "Folgender Query wurde ausgefuehrt:\n" + dbquery + "\n"]

############################################################

def writescript(scriptpath):
    # DB verbindung aufbauen.
    try:
    	conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
    except:
	return [101, "Datenbankverbindung konnte nicht hergestellt werden\n"]
    try:
    	cur = conn.cursor()
	cur.execute(open(scriptpath, "r").read())
    	conn.commit()
    	cur.close()
    	conn.close()
    except:
	return [102, "Es konnte nicht in Datenbank geschrieben werden\n"]
    return [200, "Folgendes Script wurde ausgefuehrt:\n" + scriptpath + "\n"]

############################################################

def read(table, bedingung=""):
	try:
    		conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
	except:
		return [101, "Datenbankverbindung konnte nicht hergestellt werden\n"]
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
		return [103, "Es konnte nicht aus Datenbank gelesen werden\n"]
	# DB Output to Dictionary
	return [200, results]

############################################################

def readquery(query):
	try:
    		conn = psycopg2.connect(database=n1, user=n2, host=n3, password=n4)
	except:
		return [101, "Datenbankverbindung konnte nicht hergestellt werden\n"]
	try:	
		cur = conn.cursor()
		cur.execute(query)
		results = cur.fetchall()
		cur.close()
		conn.close()
	except:
		return [103, "Es konnte nicht aus Datenbank gelesen werden\n"]
	# DB Output to Dictionary
	return [200, results]

############################################################

# Datenbank initialisieren

def initdb():
	# Existieren die gewuenschten Table?
	query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
	a = readquery(query)
	if a[0] != 200:
		return a.append("Tables konnten nicht aus DB gelesen werden\n")
	tables = a[1]
	value = []
	for x in tables:
		value.append(x[0])
	if not "photoindex" in value:
		# Die gewuenschten Tables erstellen.
		a = writescript("../PostgreSQL/photoindex_table.sql")
		if a[0] != 200:
			return a.append("Table photoindex konnte nicht erstellt werden\n")
	if not "multiplephoto" in value:
		a = writescript("../PostgreSQL/multiplephoto_table.sql")
		if a[0] != 200:
			return a.append("Table multiplephoto konnte nicht erstellt werden\n")
	return [200, tables]

# Alter Table

def altertable(columns):
	# Table um Columns welche noch nicht existieren erweitern.
	#
	# Columns auslesen.
	query = "SELECT column_name FROM information_schema.columns WHERE table_name ='photoindex';"
	a = readquery(query)
	if a[0] != 200:
		return a.append("Column namen konnten nicht gelesen werden\n")
	result = a[1]
	x = []
	for a in columns:
		x.append(a.replace(' ', '_').lower())
	columns = x
	oldcolumns = []
	for x in result:
		oldcolumns.append(str(x[0]))
	# Noch nicht vorhandene Columns erstellen
	newcolumns = []
	for x in columns:
		if not x in oldcolumns:
			newcolumns.append(x)
	if not newcolumns:
		return [110, "Es gibt keine neuen Columns zum erstellen\n"]
	for x in newcolumns:
		query = "ALTER TABLE photoindex ADD COLUMN %s character varying;" % x
		a = write(query)
		if a[0] != 200:
			return a.append("Folgender Querie hat nicht funktioniert:\n" + query + "\n")
	return [200, "Alter Table scheint funktioniert zu haben"]

# Write dict
# Schreibt Dictionary in Table test und kontrolliert ob Eintrag mehrmals vorhanden ist. Falls Ja timestamp und Image_Model in Table multiplephoto schreiben.

def writedict(dictionary):
	# Query aus dict erstellen
	columns = ""
	values = ""
	controlvalue = ""
	intvalues = ['image_exifoffset', 'exif_subjectdistancerange', 'exif_flashpixversion', 'exif_exifversion', 'exif_focallengthin35mmfilm', 'exif_interoperabilityoffset', 'thumbnail_jpeginterchangeformat', 'exif_exifimagelength', 'exif_compressedbitsperpixel', 'exif_exposurebiasvalue', 'image_gpsinfo', 'thumbnail_jpeginterchangeformatlength', 'exif_exifimagewidth', 'gps_gpsaltituderef', 'exif_focallength', 'image_xresolution', 'exif_isospeedratings', 'image_yresolution', 'thumbnail_xresolution', 'thumbnail_yresolution']
	timestamps = ["image_datetime", "exif_datetimeoriginal", "exif_datetimedigitized"]
	for x in dictionary:
		y = x.replace(' ', '_').lower()
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
	query = "INSERT INTO photoindex (" + columns + ") VALUES (" + values + ");"
	a = write(query)
	if a[0] != 200:
		return a.append("Folgender Query hat nicht funktioniert:\n" + query + "\n")
	# Kontrolle, ob Eintrag schon in DB anhand eines Timestamp und Image_Model.
	# Wenn ja wird Timestamp und Image_Model in Table multiplephoto geschrieben.
	#TODO ueberpruefen ob timestamp und Image_Model vorhanden ist
	try:
		if not controlvalue or not str(dictionary['Image Model']):
			return [121, "Es sind zu wenig Argumente fuer die douplettenueberpruefung vorhanden\n"]
	except:
		return [121, "Es sind zu wenig Argumente fuer die douplettenueberpruefung vorhanden\n"]
	query = "SELECT id FROM photoindex WHERE " + controltimestamp + " = " + controlvalue[:len(controlvalue) - 2] + " AND image_model = \'" + str(dictionary['Image Model']).replace('"', '\\"') + "\';"
	a = readquery(query)
	if a[0] != 200:
		return a.append("Folgender Query hat nicht funktioniert:\n" + query + "\n")
	searchresult = a[1]
	if len(searchresult) == 0:
		# Konnte nicht in DB schreiben
		return [120, "Der zuvor ausgefuehrte Query konnte nicht wieder aus der DB gelesen werden\n"]
		pass
	elif len(searchresult) == 1:
		# Eintrag ist nur ein Mal in DB
		pass
	else:
		# Eintrag ist mehrmals in DB
		# Timestamp und Image_Model in Table multiplephoto schreiben
		query = "INSERT INTO multiplephoto (" + controltimestamp + ", Image_Model) VALUES (" + controlvalue + "\'" + str(dictionary['Image Model']).replace('"', '\\"') + "\');"
		a = write(query)
		if a[0] != 200:
			return a.append("Folgender Query hat nicht funktioniert:\n" + query + "\n")
	return [200, "Photo scheint erfolgreich indexiert worden zu sein\n"]
	
		
	










