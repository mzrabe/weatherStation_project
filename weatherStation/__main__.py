#!usr/bin/python

import time
import sys
import matplotlib

matplotlib.use('Agg')
from weatherStation.util import logBME280, aneometer, logDHT22, plotChart
from weatherStation.web import htmlInterface

GROUP_CHART = ['--group-chart']
WIND_CHART = ['--wind-chart']
LOG_DHT22 = ['--log-dht22']
LOG_BME280 = ['--log-bme280']
LOG_WIND = ['--log-wind']
WEB_SERVICE = ['--website']

if __name__ == '__main__':
	for s in sys.argv:
		if s in GROUP_CHART:
			# todo : replace time.time.now()
			plotChart.plot_group_chart(
				logBME280.get_24_hours_data(time.mktime(time.strptime('2019-11-26 23:59', '%Y-%m-%d %H:%M'))),
				logDHT22.get_24_hours_data(time.mktime(time.strptime('2019-11-26 23:59', '%Y-%m-%d %H:%M'))))
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
					aneometer.get24HouresData(time.mktime(time.strptime('2019-07-01 23:59', '%Y-%m-%d %H:%M'))),
					fileName='windChart.png'))
		else:
			print(s, ' unknown command.')
