import random
import time
from weatherStation.util import logBME280, logDHT22

def read_retry(sensor, pin):
	"""
		Simulate sensor data of the DHT22 sensor for the parameter
		temperature and humidity.
		Returns
		-------
		temperature, humidity as floats,
		units: [°C], [%]
		"""
	last_data = logDHT22.get_24_hours_data(time.time()).iloc[-1]

	if last_data.size == 0:
		temperature = 21.
		humidity = 70.
	else:
		temperature = float(last_data[logDHT22.TEMPERATURE])
		humidity = float(last_data[logDHT22.HUMIDITY])

	temperature = temperature + (-1 + random.random() * 2)
	humidity = humidity + (-10 + random.random() * 20)

	return temperature, humidity


def readBME280All():
	"""
	Simulate sensor data of the BME280 sensor for the parameter
	temperature, pressure and humidity.
	Returns
	-------
	temperature, pressure, humidity as floats,
	units: [°C], [hPa], [%]
	"""
	# get the last value in the log file
	last_data = logBME280.get_24_hours_data(time.time()).iloc[-1]

	if last_data.size == 0:
		temperature = 21.
		pressure = 1000.0
		humidity = 70.
	else:
		temperature = float(last_data[logBME280.TEMPERATURE])
		pressure = float(last_data[logBME280.PRESSURE])
		humidity = float(last_data[logBME280.HUMIDITY])

	temperature = temperature + (-1 + random.random() * 2)
	pressure = pressure + (-10 + random.random() * 20)
	humidity = humidity + (-10 + random.random() * 20)

	return temperature, pressure, humidity
