#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMPORTS
import csv
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import time
import matplotlib.style

matplotlib.style.use('grayscale')

from weatherStation.config import configs
from weatherStation.util import bme280

# date pattern
datePattern = "%Y-%m-%d"
# time pattern
timePattern = "%H:%M:%S"
# file name pattern
file_name_pattern = 'bme280_data_' + datePattern + '.csv'
# name of configuration file
CONFIG_FILE_NAME = 'bme280'

## CSV - field names
DATE = configs.DATE
TIME = configs.TIME
DATE_TIME = configs.DATE_TIME
TIMESTAMP = configs.TIMESTAMP
TEMPERATURE = configs.TEMPERATURE
PRESSURE = configs.PRESSURE
HUMIDITY = configs.HUMIDITY

field_names = [DATE, TIME, TEMPERATURE, PRESSURE, HUMIDITY]


## functions

def log():
	# get path to log directory
	pathToLogDir = configs.getLogDirPath(CONFIG_FILE_NAME)

	# current date
	currentDate = datetime.now()
	# create name of current file of day
	filename = os.path.join(pathToLogDir, currentDate.strftime(file_name_pattern))
	print(filename)
	with open(filename, 'a') as logfile:
		# create new datawriter
		datawriter = csv.DictWriter(logfile, delimiter=',', lineterminator='\n', fieldnames=field_names)
		# check whether the file is new or empty
		if logfile.tell() == 0:
			datawriter.writeheader()

		data = {}
		
		# get current time {HH:MM:SS}
		time = datetime.now().strftime(timePattern)

		# get sensor data
		temperature, pressure, humidity = bme280.readBME280All()

		data[DATE] = currentDate.strftime(datePattern)
		data[TIME] = time
		data[TEMPERATURE] = "{0:.2f}".format(temperature)
		data[PRESSURE] = "{0:.2f}".format(pressure)
		data[HUMIDITY] = "{0:.2f}".format(humidity)
		print(data)
		# write a now row into logging file
		datawriter.writerow(data)


def get_data_from_file(file_name, path_to_log_dir=configs.getLogDirPath(CONFIG_FILE_NAME)):
	"""
	Fetch the data from the BME280 log file. The file contains date, time
	temperature, pressure and humidity.

	Returns
	-------
	pandas DataFrame containing the log data in the file
	"""
	if os.path.isfile(path_to_log_dir + file_name):
		with open(path_to_log_dir + file_name, 'r') as data_file:
			# Advanced CSV loading example
			df = pd.read_csv(
				data_file,  # relative python path to subdirectory
				sep=',',  # Tab-separated value file.
				quotechar="'",  # single quote allowed as quote character
				dtype={DATE: str, TIME: str, TEMPERATURE: float, PRESSURE: float, HUMIDITY: float},
				# Parse the salary column as an integer
				# usecols=['name', 'birth_date', 'salary'].	# Only load the three columns specified.
				# parse_dates=['birth_date'],     			# Intepret the birth_date column as a date
				# skiprows=10,         						# Skip the first 10 rows of the file
				na_values=['.', '??', '-'],  # Take any '.', '-' or '??' values as NA
			)
			df[TIMESTAMP] = (df[DATE] + ' ' + df[TIME]).map(
				lambda x: time.mktime(time.strptime(x, datePattern + ' ' + timePattern)))
			return df
	else:
		return pd.DataFrame()


def get_24_hours_data(t2):
	"""
	@param t2 - current time in seconds
	"""
	# time 24 hours ago
	t1 = t2 - 60 * 60 * 24
	data = pd.DataFrame()
	# data 24 hours ag0
	data = data.append(get_data_from_file(time.strftime(file_name_pattern, time.localtime(t1))))
	# current data
	data = data.append(get_data_from_file(time.strftime(file_name_pattern, time.localtime(t2))))

	mask = (data[TIMESTAMP] >= t1) & (data[TIMESTAMP] <= t2)

	if len(data) <= 0:
		return data
	else:
		return data[mask]


def make_patch_spines_invisible(ax):
	ax.set_frame_on(True)
	ax.patch.set_visible(False)
	for sp in ax.spines.values():
		sp.set_visible(False)


def plot_24_hours(date=time.time(), figsize=configs.fig_size, title=None, file_name=None):
	if title is not None:
		plt.title(title)

	data = get_24_hours_data(date)
	print(data[TIME])

	fig, host = plt.subplots(figsize=figsize)
	fig.subplots_adjust(right=0.9)

	par1 = host.twinx()
	par2 = host.twinx()

	# Offset the right spine of par2.  The ticks and label have already been
	# placed on the right by twinx above.
	par2.spines["right"].set_position(("axes", 1.1))
	# Having been created by twinx, par2 has its frame off, so the line of its
	# detached spine is invisible.  First, activate the frame but make the patch
	# and spines invisible.
	make_patch_spines_invisible(par2)
	# Second, show the right spine.
	par2.spines["right"].set_visible(True)

	# plot the data
	p1, = host.plot(data[TIMESTAMP], data[TEMPERATURE], 'r-', label=TEMPERATURE, linewidth=1)
	p2, = par1.plot(data[TIMESTAMP], data[HUMIDITY], 'g--', label=HUMIDITY, linewidth=1)
	p3, = par2.plot(data[TIMESTAMP], data[PRESSURE], 'b:', label=TEMPERATURE, linewidth=1)

	# host.set_xlim(0, 2)
	# host.set_ylim(0, 2)
	# par1.set_ylim(ymax=100)
	# par2.set_ylim(1, 65)

	# set labels
	host.set_xlabel("time")
	host.set_ylabel(TEMPERATURE + u' [°C]')
	par1.set_ylabel(HUMIDITY + u' [%]')
	par2.set_ylabel(PRESSURE + ' [hPa]')

	# get the color of plotted lines
	host.yaxis.label.set_color(p1.get_color())
	par1.yaxis.label.set_color(p2.get_color())
	par2.yaxis.label.set_color(p3.get_color())

	# text size of the axes
	tkw = dict(size=4, width=1.5)
	# colors of the axes
	host.tick_params(axis='y', colors=p1.get_color(), **tkw)
	par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
	par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
	host.tick_params(axis='x', **tkw)

	# set the ticks of the x axis for each 6th value (full hour)
	host.set_xticks(data[TIMESTAMP][::6])
	host.set_xticklabels(data[TIME].map(lambda x: x[:-3])[::6])
	host.tick_params(axis='x', rotation=45, grid_linestyle='dashed', grid_color='lightgray', )
	host.tick_params(axis='y', grid_alpha=0)
	host.grid(True)

	# plt.grid(axis='both', linestyle='dashed', color='lightgray')

	# get the mean date of the time values for the name of the file
	if file_name is None:
		# file_name = 'hourValues_windlogs_'+time.strftime(datePattern, data[TIMESTAMP][int(len(data[TIMESTAMP])/2)])+'.png'
		file_name = 'testBME280.png'
	print('savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name)

	plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
	plt.close()
