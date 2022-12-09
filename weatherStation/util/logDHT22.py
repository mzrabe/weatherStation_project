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

# import the required library to read the sensor data
# from the BME280 sensor. In case the script/module is
# not running on a raspberry pi a dummy library will import
# which simulate sensor data.
if 'raspberrypi' in os.uname():
	import Adafruit_DHT
else:
	from weatherStation.util import SensorSimulator as Adafruit_DHT

# Get the system specific configuration which are set up
# individual from the system user.
from weatherStation.config import configs
from weatherStation.util import humidity

matplotlib.style.use('grayscale')


# date pattern
datePattern = "%Y-%m-%d"
# time pattern
timePattern = "%H:%M:%S"
# file name pattern
file_name_pattern = 'dht22_data_' + datePattern + '.csv'
# name of configuration file
CONFIG_FILE_NAME = 'dht22'

## CSV - field names
DATE = configs.DATE
TIME = configs.TIME
DATE_TIME = configs.DATE_TIME
TIMESTAMP = configs.TIMESTAMP
TEMPERATURE = configs.TEMPERATURE
# pressure value is not available for this sensor
PRESSURE = configs.PRESSURE
HUMIDITY = configs.HUMIDITY

field_names = [DATE, TIME, TEMPERATURE, PRESSURE, HUMIDITY]


## functions

def log():
	# get path to log directory
	pathToLogDir = configs.getLogDirPath(CONFIG_FILE_NAME)

	# current date
	current_date = datetime.now()
	# create name of current file of day
	filename = os.path.join(pathToLogDir, current_date.strftime(file_name_pattern))

	with open(filename, 'a') as logfile:
		# create new data_writer
		data_writer = csv.DictWriter(logfile, delimiter=',', lineterminator='\n', fieldnames=field_names)
		# check whether the file is new or empty
		if logfile.tell() == 0:
			data_writer.writeheader()

		data = {}

		# get current time {HH:MM:SS}
		time_str = datetime.now().strftime(timePattern)
		#TODO
		# get log date of the last x minutes
		# filter out the outliers
		# get the data of the last 60 minutes -> the last 6 values
		# values = get_24_hours_data(time.time())[-6]

		# get sensor data, as float, if an error occurred a tuple of (None, None) will
		# return
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 14)

		data[DATE] = current_date.strftime(datePattern)
		data[TIME] = time_str

		# The sensor DHT22 does not measure the pressure.
		data[PRESSURE] = "-"

		# In case both values are None
		# the delivered values from the sensor are invalid.
		# Additionally check the valid temperature and humidity
		# range according to the data sheet of the DHT22
		# {@link https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf}

		#TODO Furthermore check if the current measured values
		# are outliers

		# check the range of temperature
		if (-40 <= temperature <= 80) or temperature is not None:
			data[TEMPERATURE] = "{0:.2f}".format(temperature)
		else:
			data[TEMPERATURE] = '-'
		# check the range of the humidity
		if (0 <= humidity <= 100) or humidity is not None:
			data[HUMIDITY] = "{0:.2f}".format(humidity)
		else:
			data[HUMIDITY] = '-'

		# Try to approximate the current value with the paste
		# values since 60 minutes ago

		#TODO hier noch weiter machen
		# ~ values = values.append(data)
		# ~ outliers = util.find_outlier(values)
		# ~ if outliers[-1] == true:
			
			
		# write a now row into logging file
		data_writer.writerow(data)


def get_data_from_file(file_name, path_to_log_dir=configs.getLogDirPath(CONFIG_FILE_NAME)):
	"""
    Fetch the data from the DHT22 log file. The file contains date, time
    temperature and humidity.

    Returns
    -------
    pandas DataFrame containing the log data in the file
    """
	if os.path.isfile(os.path.join(path_to_log_dir,file_name)):
		with open(os.path.join(path_to_log_dir,file_name), 'r') as data_file:
			try:
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
			except pd.errors.EmptyDataError:
				return pd.DataFrame()
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

	# create a new column seconds
	mask = (data[TIMESTAMP] >= t1) & (data[TIMESTAMP] <= t2)

	if len(data) <= 0:
		return data
	else:
		return data[mask]

def get_24_hours_data_absolut(t2):
	"""
	@param t2 - current time in seconds
	"""

	# current data
	data = get_24_hours_data(t2)

	if len(data) <= 0:
		return data
	else:
		return humidity.absolute_humidity_df(data)

def get_data(starttime, endtime):
	"""
	@param starttime - start time in [seconds]
	@param endtime - end time in [seconds]
	"""
	data = pd.DataFrame()
	
	# loop through the loging file to collect all the data between the 
	# start and end time
	for fname in os.listdir(configs.getLogDirPath(CONFIG_FILE_NAME)):
		if os.path.isfile(os.path.join(configs.getLogDirPath(CONFIG_FILE_NAME), fname)) == False:
			continue
		
		try:
			filetime = time.mktime(time.strptime(fname,file_name_pattern))
		except ValueError:
			#print fname, 'matchs not the filepattern', file_name_pattern
			continue
		if starttime <= filetime and endtime+24*60*60 >= filetime:
			#print fname
			data = data.append(get_data_from_file(fname))

	# create a new column seconds
	mask = (data[TIMESTAMP] >= starttime) & (data[TIMESTAMP] <= endtime+24*60*60)
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
	# par2 = host.twinx()

	# Offset the right spine of par2.  The ticks and label have already been
	# placed on the right by twinx above.
	# par2.spines["right"].set_position(("axes", 1.1))
	# Having been created by twinx, par2 has its frame off, so the line of its
	# detached spine is invisible.  First, activate the frame but make the patch
	# and spines invisible.
	# make_patch_spines_invisible(par2)
	# Second, show the right spine.
	# par2.spines["right"].set_visible(True)

	# plot the data
	p1, = host.plot(data[TIMESTAMP], data[TEMPERATURE], 'r-', label=TEMPERATURE, linewidth=1)
	p2, = par1.plot(data[TIMESTAMP], data[HUMIDITY], 'g--', label=HUMIDITY, linewidth=1)
	# p3, = par2.plot(data[TIMESTAMP], data[PRESSURE], 'b:', label=TEMPERATURE, linewidth=1)

	# host.set_xlim(0, 2)
	# host.set_ylim(0, 2)
	# par1.set_ylim(ymax=100)
	# par2.set_ylim(1, 65)

	# set labels
	host.set_xlabel("time")
	host.set_ylabel(TEMPERATURE + u' [°C]')
	par1.set_ylabel(HUMIDITY + u' [%]')
	# par2.set_ylabel(PRESSURE + ' [hPa]')

	# get the color of plotted lines
	host.yaxis.label.set_color(p1.get_color())
	par1.yaxis.label.set_color(p2.get_color())
	# par2.yaxis.label.set_color(p3.get_color())

	# text size of the axes
	tkw = dict(size=4, width=1.5)
	# colors of the axes
	host.tick_params(axis='y', colors=p1.get_color(), **tkw)
	par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
	# par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
	host.tick_params(axis='x', **tkw)

	# set the ticks of the x axis for each 6th value (full hour)
	host.set_xticks(data[TIMESTAMP][::6])
	host.set_xticklabels(data[TIME].map(lambda x: x[:-3])[::6])
	host.tick_params(axis='x', rotation=45, grid_linestyle='dashed', grid_color='lightgray')
	host.tick_params(axis='y', grid_alpha=0)
	host.grid(True)

	# plt.grid(axis='both', linestyle='dashed', color='lightgray')

	# get the mean date of the time values for the name of the file
	if file_name is None:
		# file_name = 'hourValues_windlogs_'+time.strftime(datePattern, data[TIMESTAMP][int(len(data[TIMESTAMP])/2)])+'.png'
		file_name = 'testDHT22.png'
	print('savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name)

	plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
	plt.close()
