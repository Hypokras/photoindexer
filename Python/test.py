#!/usr/bin/env python
# coding: utf8
import os
import os.path
import exifread
import database


def indexing(pathtoimage):
	imagepath = os.path.abspath(pathtoimage)
	if not os.path.exists(imagepath):
		return [160, "Der Pfad %s existiert nicht" % imagepath]
	foldername = os.path.dirname(imagepath)
	filename = os.path.basename(imagepath)
	f = open(imagepath, 'rb')
	try:
		tags = exifread.process_file(f, details=False)
	except:
		return [160, "Irgendetwas beim Lesen der EXIF-Daten ging schief bei %s" % imagepath]
	if tags == {}:
		return [160, "File %s enthält keine EXIF-Daten" % imagepath]
	f.close()
	tags['dir_foldername'] = foldername
	tags['dir_filename'] = filename
	a = database.writedict(tags)
	if a[0] == 200:
		return a
	elif a[0] == 102:
		a = database.altertable(list(tags))
		if a[0] != 200:
			a.append("altertable hat nicht funktioniert\n")
			return a
		a = database.writedict(tags)
		if a[0] != 200:
			a.append("writedict hat trotz altertable nicht funktioniert\n")
			return a
	else:
		a.append("irgendetwas ging total schief")
		return [160, "test"]


# Ueber alle Files im photofolder loopen

def loopinfolder(photofolder):
	#logfile erstellen.
	logfile = open("/tmp/photoindexer.log", "a")
	logfile.write("Dies ist das Logfile\n")
	logfile.close()
	database.initdb()
	# Dateien zählen
	anzahldateien = 0
	for root, dirs, files in os.walk(photofolder):
		for n in files:
			anzahldateien = anzahldateien + 1
	counter = 0
	for root, dirs, files in os.walk(photofolder):
		for n in files:
			counter = counter + 1
			a = indexing(root + "/" + n)
			if a[0] == 160:
				logfile = open("/tmp/photoindexer.log", "a")
				for x in a:
					logfile.writelines(str(x))
				logfile.close()
				print "Bearbeite File %s von %s\n" % (str(counter), str(anzahldateien))
			elif a[0] != 200:
				a.append("indexierung unterbrochen")
				logfile = open("/tmp/photoindexer.log", "a")
				for x in a:
					logfile.writelines(str(x))
				logfile.close()
				return a
			else:
				print "Bearbeite File %s von %s\n" % (str(counter), str(anzahldateien))
				
			



