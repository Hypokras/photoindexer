#!/usr/bin/env python
# coding: utf8
import os
import os.path
import exifread
import database


# Definitionen
photofolder = "/home/imageindexer/"




def indexing(pathtoimage):
	imagepath = os.path.abspath(pathtoimage)
	foldername = os.path.dirname(imagepath)
	filename = os.path.basename(imagepath)
	f = open(imagepath, 'rb')
	tags = exifread.process_file(f)
	exif_datetimeoriginal = str(tags['EXIF DateTimeOriginal'])
	datetime = exif_datetimeoriginal[:4] + "-" + exif_datetimeoriginal[5:7] + "-" + exif_datetimeoriginal[8:]
	imagemodel = str(tags['Image ImageDescription'])
	#TODO Kontrollen fehlen, Tags sind nicht einheitlich...
	query = "insert into test (name, path, datetime, imagemodel) values ('%s', '%s', TIMESTAMP '%s', '%s');" %(filename, foldername, datetime, imagemodel)
	status = database.write(query)
	return [foldername, filename, datetime, imagemodel, status]


