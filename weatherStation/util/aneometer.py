#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Functions to calculate the wind velocity, to store and load the data from
saved files. The path of the wind log file has to be defined on the  

Created by Moritz Zahn
Email : zahn.moritz@posteo.de
"""

## IMPORTS
import csv
import os
from datetime import datetime, time
import appdirs

import math as Math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time

if 'raspberrypi' in os.uname():
	import RPi.GPIO as gpio

import threading
from signal import *

import matplotlib.style

matplotlib.style.use('grayscale')

from weatherStation.config import configs

## Properties
# name of configuration file
CONFIG_FILE_NAME = 'anemometer'
# date pattern
datePattern = "%Y-%m-%d"
# log file pattern
filePattern = 'windLogs_%Y-%m-%d.csv'

# Beschriftung der x-Achse
labels = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
          '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

## Properties of the cup anemometer to measure wind velocity

# cup diameter in [m]
d = 0.036
# radius to center of cup [m]
r1 = 0.052
# radius of center between outer radius of hub and cup center
r0 = 0.022

# cross sectional surface of cup
A1 = Math.pi / 4 * d ** 2
# projection surface of the bar
A0 = 0.024 * 0.002

# coefficient of friction of the cup
cw = 1.2

# factors to calculate the tip-speed ratio
D = 3.36 * A1 * r1 + 4. * cw * A0 * r0 ** 2. / r1
E = 0.66 * A1 * r1 - cw * A0 * r0 ** 3. / r1 ** 2.

# estimated bearing friction 
Mr = 0.000015

# estimated air density [kg/m^3]
rho = 1.2


## funtions related to calculate the wind velocity

def lam(u):
	"""
	Calculation of the tip-speed rationas as function of the peripheral speed
	"""
	F = D / E + 2 * Mr / (rho * u * E)
	return F / 2 - np.sqrt((F / 2) ** 2 - A1 * r1 / E)


def u(time, r=r1):
	"""
	Calculation the peripheral speed as function of the time difference for one rotation.
	"""
	return 2 * Math.pi * r1 / (time / 1000.)


def v(t):
	"""
	Calculation of the wind velocity [m/s] as function of the time difference for one rotation.
	"""
	u_velocity = u(t)
	F = D / E + 2 * Mr / (rho * u_velocity * E)
	return u_velocity / (F / 2 - np.sqrt((F / 2) ** 2 - A1 * r1 / E))


## function to write and read the data from the logging files

def getDataFromFile(fileName, pathToLogDir=configs.getLogDirPath(CONFIG_FILE_NAME)):
	"""
	Fetch the data from the wind log file. The file contains the time
	(milliseconds since 01.01.1970) when the  magnet of the
	hemispherical cup anemometer passed the hall sensor. One row per time.

	The method returns the times as numpy array of type float.
	"""
	data = np.genfromtxt(pathToLogDir + fileName, delimiter=',', dtype=float)

	return data


## functions for plotting the data

def get24HouresData(t2):
	"""
	@param t2 - current time in seconds
	"""
	# time 24 hours before
	t1 = t2 - 60 * 60 * 24
	# file name of 24 hours ago
	file1 = time.strftime(filePattern, time.localtime(t1))
	data1 = getDataFromFile(file1)
	# current file name
	file2 = time.strftime(filePattern, time.localtime(t2))
	data2 = getDataFromFile(file2)

	return np.append(data1[data1 >= t1 * 1e3], data2[data2 <= t2 * 1e3])


def plotWindLogChart(data):
	"""
	Make a plot of the given wind log data as moving average.

	@param data - time after the cup anemometer passed the sensor in [ms] since 1.1.1970
	"""
	# todo das muss ich noch richtig machen und überprüfen
	# Get the windlog data of weather station Berlin Tegel
	# tegelDaten = [x.split(';') for x in open(windlogsDir+'/tegelDaten.txt','r').readlines()]

	# Fetch time and date of the wind velocity data
	# xTegel = np.array([time.mktime(time.strptime(x[1],'%Y%m%d%H')) for x in tegelDaten],dtype=float) * 1000
	# Fetch the wind velocity in convert them into km/h
	# yTegel = np.array([x[3] for x in tegelDaten],dtype=float) *3.6

	# calculate the time difference between one cup anemometer rotation
	timeDiff = data[1:-1] - data[0:-2]
	# time between to time logs
	x = (data[1:-1] + data[0:-2]) / 2.

	# create a figure for plotting the data
	fig = plt.figure(figsize=(24, 12))
	ax = plt.subplot(111)
	plt.title('Datei : ' + fname)
	plt.xlabel('Time')
	plt.ylabel('Wind velocity [km/h]')

	step = 1
	r = 1

	vAvg = v(timeDiff[::step]) * 3.6

	vGMAvg = []

	for i in range(vAvg.size):
		vGMAvg.append(sum(vAvg[max(0, i - r):min(vAvg.size, i + r)]) / (min(vAvg.size, i + r) - max(0, i - r)))

	ax.plot(x[:-1:step], vGMAvg[:-1], '-', label='Mittelwert - gleitendes Mittel r = ' + str(r), linewidth=1)

	# create the x axis (time axis) labels
	xlabels = np.arange(x[0], x[-1], (x[-1] - x[0]) / 24)
	labels = []
	for xi in xlabels:
		labels.append(time.strftime('%H:%M Uhr', time.localtime(xi / 1000)))

	plt.xticks(xlabels, labels, rotation='vertical')
	plt.legend()
	plt.ylim(ymin=0, ymax=40)
	# format='png'
	plt.savefig('test.png', format='png', bbox_inches='tight')
	print('test.png', 'saved as png ...')


def hourly_average_wind_velocity(data, start=None, end=None):
	"""
	Make a plot of the given wind log data. Before plotting the values averaging
	before for each time interval.

	@param data - time after the cup anemometer passed the sensor in [ms] since 1.1.1970

	Parameters
	----------
	data : time after the cup anemometer passed the sensor in [ms] since 1.1.1970
	start : start time of data in milliseconds, as default first entry of data
	end : end time of data in milliseconds, as default last entry of data
	fileName : file name of the chart to save
	figsize : size of the chart in inches
	title : titel of the chart

	Returns
	----------
	@return - list with the hourly average wind velocity, [time, wind velocity]
	"""

	if start == None:
		start = data[0]
	if end == None:
		end = data[-1]

	xValues = []
	yValues = []

	# time interval, one houre in milliseconds
	timeInterval = 3600000
	# start time in milliseconds, full houre
	startTime = round(start / timeInterval - 0.5) * timeInterval

	# calculate the average in the time interval
	while startTime < end:
		endTime = startTime + timeInterval
		dataInHoure = data[(data >= startTime) & (data < endTime)]

		if dataInHoure.size == 0:
			# in case there are no data in the time interval
			mean = 0.0;
		else:
			# calculate time difference
			timeDiff = dataInHoure[1:-1] - dataInHoure[0:-2]
			# calculate the wind velocity in [km/h]
			vAvg = v(timeDiff) * 3.6

			if vAvg.size != 0:
				# calculate the average value
				mean = np.sum(vAvg) / vAvg.size
			else:
				mean = 0.0

		xValues.append((startTime + endTime) / 2.0)
		yValues.append(mean)

		startTime = endTime

	return [xValues, yValues]


##
# todo Das muss noch angepasst werden
def plotWindVelocityCharts(winlogsDir=configs.getLogDirPath(CONFIG_FILE_NAME)):
	for root, dirs, files in os.walk(windlogsDir):
		files = sorted(files)

		newFormateTime = time.mktime(time.strptime('2018-03-05', '%Y-%m-%d'))
		print(newFormateTime)

		for fname in files:
			if fname.replace('.csv', '.png') not in files:
				if newFormateTime > time.mktime(time.strptime(fname, 'windLogs_%Y-%m-%d.csv')):
					makeWindLogDia(os.path.join(root, fname))
				else:
					makeWindLogDia2(os.path.join(root, fname))
		# walk over each file
		for fname in files:
			# allow only .csv files, otherwise continue
			if '.csv' not in fname or 'houreValues.csv' == fname:
				continue
			# does the data already plotted
			if alreadyAsPNG(files, fname[-14:-4]):
				print('data of file -', fname, '- already plotted')
				continue

			# time of data file in seconds
			timeOfDataFile = time.mktime(time.strptime(fname, 'windLogs_%Y-%m-%d.csv'))

			if startDate >= timeOfDataFile:
				print('file', fname, 'ignored (startDate)')
				continue
			if newFormateTime > timeOfDataFile:
				# old formate: from,average,min,max

				# print 'Get data from ',fname,'...'
				# print 'file',fname,'ignored (oldFileFormate)'
				# continue
				print('Get data from ', fname, '...')
				try:
					data = np.array([float(x.split(',')[0]) for x in open(windlogsDir + '/' + fname, 'r').readlines()],
					                dtype=float)
				except ValueError:
					print('ValueError')
					lineNumber = 1
					for x in open(windlogsDir + '/' + fname, 'r').readlines():
						try:
							xfloat = float(x)
							lineNumber = lineNumber + 1
						except ValueError:
							print('ValueError in file', fname)
							print(x, 'in line', lineNumber + 1, 'cannot convert in a float!')
							break
					break

				startTime = time.mktime(time.strptime(fname + '-' + str(0), 'windLogs_%Y-%m-%d.csv-%H'))

				xValues = []
				yValues = []

#
#
#

# Log script version 2. Difference to version 1 is that every signal of
# the anemometer will save into the log file since the 5th marche 2018.

SAVE_DIRECTORY = configs.getLogDirPath(CONFIG_FILE_NAME)

logs = []


def getCurrentTime():
	"""
	# Get the current time in miliseconds
	"""
	return time.time() * 1000


def getLogFileName():
	"""
	Get the name of the log file which has
	the pattern 'windLogs_%Y-%m-%d.csv'.
	"""
	return time.strftime(filePattern, time.localtime())


def getAverageMinMaxValues(logs):
	"""
	- calculate the elapsed time between the logs
	- find the min and max elapsed time
	- calculate the average
	return (average, min, max) in milisecond
	"""
	# if there is only 1 value in the list
	# then forget it... shit happends
	if len(logs) <= 1:
		return
	#	print logs
	# calculate the difference
	diff = []
	for i in range(len(logs) - 1):
		diff.append(logs[i + 1] - logs[i])
	#	print diff

	minValue = min(diff)
	maxValue = max(diff)
	avg = sum(diff) / len(diff)

	#	print avg,min,max
	# return the values
	return avg, minValue, maxValue


def write_time_in_log_file(logs):
	"""
	Write the list of logs into a log file.
	"""

	# if nothing is in the list
	if logs == None or len(logs) == 0:
		return

	fileName = getLogFileName()

	# check if the log directory exist, if not
	# create it
	if not os.path.isdir(SAVE_DIRECTORY):
		os.makedirs(SAVE_DIRECTORY)

	filePath = SAVE_DIRECTORY + fileName
	#	print filePath
	# check if the log file exist, if not
	# create a new one, otherwise append the
	# logs to the end of the file
	if os.path.isfile(filePath):
		logFile = open(filePath, 'a')
	else:
		logFile = open(filePath, 'w')

	# write the logs into the file
	for log in logs:
		logFile.write(str(log) + "\n")

	logFile.flush()
	logFile.close()


class saveThread(threading.Thread):
	"""
	Thread class to write the logs into
	the log file.
	"""

	def __init__(self, logs):
		threading.Thread.__init__(self)
		self.logs = logs

	def run(self):
		if len(self.logs) >= 2:
			write_time_in_log_file(logs)


def start_logging():
	print('Start wind logging script ...')
	hallSig = False
	global logs

	def onExit(*args):
		"""
		Function which performs a clean of the
		GPIO interface and saves the last logs
		into the log file, if the script is terminate
		of the signal SOGABRT, SIGINT or SIGTERM
		"""
		print('Clean and save logs befor exit ...')
		gpio.cleanup()
		st = saveThread(logs[:])
		st.start()
		print('Exit script ...\n')
		os._exit(0)

	# define what happens if the program is
	# killed by these signals
	for sig in (SIGABRT, SIGINT, SIGTERM):
		signal(sig, onExit)

	# setting for the GPIO interface
	gpio.setmode(gpio.BCM)
	# input of the hall sensor
	gpio.setup(24, gpio.IN)
	# output for the LED, only for testing
	#gpio.setup(24, gpio.OUT)

	# Endless loop which logs time of
	# a signals from the anemomenter
	while True:
		# magnet is in front of the sensor
		if gpio.input(24) == 0:
			# turn LED on, only for testing
			#gpio.output(24, gpio.HIGH)

			# magnet has passed the sensor
			if hallSig == False:
				hallSig = True
				logs.append(getCurrentTime())
				if len(logs) == 10:
					st = saveThread(logs[:])
					st.start()
					# writeTimeInLogFile(logs[:])
					logs = []

		# magnet is away of the sensor
		else:
			# turn LED out, only for testing
			#gpio.output(24, gpio.LOW)
			# reset the signal to false, to
			# recognise a new pass of the
			# magnet along the sensor
			if hallSig:
				hallSig = False

		time.sleep(0.005)
	# END while True loop

	# clean up the GPIO interface
	gpio.cleanup()
	#	writeTimeInLogFile(getAverageMinMaxValues(logs))
	print('End of logging ...')


# END main()

if __name__ == "__main__":
	start_logging()
