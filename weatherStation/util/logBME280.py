#!/usr/bin/python
#-*- coding: utf-8 -*-

# IMPORTS
import csv
import os
from datetime import datetime
import bme280
import appdirs

# date pattern
datePattern = "%Y-%m-%d"
# time pattern
timePattern = "%H:%M:%S"
# name of configuration file
CONFIG_FILE_NAME = 'bme280'

def run():
	# get path to log directory
	pathToLogDir = ''
	configPath = os.path.join(appdirs.user_config_dir('weatherStation'),CONFIG_FILE_NAME)
	
	if os.path.isfile(configPath):
		configFile = open(configPath,'r')
		# Read the first line of the configuration file
		# which specified the path where the log files
		# should store.
		pathToLogDir = configFile.readline()
	else:
		print 'Please define the path where the log files should stored in the config-file :',configPath
		return
	
	#current date
	currentDate = datetime.now().strftime(datePattern)
	# create name of current file of day
	filename = os.path.join(pathToLogDir,'bme280_data_'+currentDate+'.csv')

	# check if file exsist
	if os.path.isfile(filename):
		# file exsist, open an append new charaters
		datafile = open(filename, "a")
	else:
		# file not exsist, create and open new fiel
		datafile = open(filename, "wb")

	# create new datawriter
	datawriter = csv.writer(datafile, delimiter=',',lineterminator='\n')
	
	data = []

	# get current time {HH:MM:SS}
	time = datetime.now().strftime(timePattern)

	# get sensor data
	temperature, pressure, humidity = bme280.readBME280All()

	data.append(currentDate)
	data.append(time)
	data.append("{0:.2f}".format(temperature))
	data.append("{0:.2f}".format(pressure))
	data.append("{0:.2f}".format(humidity))

	# write a now row into logging file
	datawriter.writerow(data)
	datafile.close()

if __name__ == "__main__":
	run()
