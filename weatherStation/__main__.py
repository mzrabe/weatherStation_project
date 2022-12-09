#!usr/bin/python

import time
import sys
import matplotlib
# important to use on raspberry pi without display/monitor
matplotlib.use('Agg')
from weatherStation.util import logBME280, aneometer, logDHT22, plotChart
from weatherStation.web import htmlInterface

GROUP_CHART = ['--group-chart']
WIND_CHART = ['--wind-chart']
LOG_DHT22 = ['--log-dht22']
LOG_BME280 = ['--log-bme280']
LOG_WIND = ['--log-wind']
WEB_SERVICE = ['--website']
HELP = ['--help', '-h']

if __name__ == '__main__':
	for s in sys.argv[1:]:
		if s in GROUP_CHART:
			plotChart.plot_group_chart(
				logBME280.get_24_hours_data_absolut(time.time()),
				logDHT22.get_24_hours_data_absolut(time.time()),
				title='Temperature, pressure and humidity of last 24h')
		elif s in LOG_DHT22:
			print('Log DHT22 sensor.')
			logDHT22.log()
		elif s in LOG_BME280:
			print('Log BME280 sensor.')
			logBME280.log()
		elif s in LOG_WIND:
			print('Start log cup anemometer.')
			aneometer.start_logging()
		elif s in WEB_SERVICE:
			print('Start website')
			htmlInterface.run_website()
		elif s in WIND_CHART:
			print('Print wind velocity chart.')
			plotChart.plot_hour_wind_log_chart(
				aneometer.hourly_average_wind_velocity(
					aneometer.get24HouresData(time.time()),start=(time.time()-24*60*60)*1000, end=time.time()*1000),
					fileName='windChart.png',
					title='Wind Velocity of last 24h')
		elif s in HELP:
			print('Use one of the following commands.\n\n\t'
				'--group-chart\t Plot a group chart (temperature, humidity and pressure\n\t'
				' of the last 24 hours from the BME280 and the DHT22 sensor.\n'
				'\t--wind-chart\tPlot a chart of the mean hour wind velocity of\n\t'
				'the last 24 hours.\n'
				'\t--log-dht22\tRead the sensor data of the DHT22 and write the values\n\t'
				'in the defined logging file.\n'
				'\t--log-bme280\tRead the sensor data of the BM280 and write the values\n\t'
				'in the defined logging file\n'
				'\t--log-wind\tStart the script to log the wind velocity.\n'
				'\t--website\tStart running the website.\n'
				'\t--help, -h\tSee this help message.')
		else:
			print(s, ' unknown command.')
