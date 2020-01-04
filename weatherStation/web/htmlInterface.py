#!/usr/bin/python
# -*- coding : utf-8 -*-

from flask import Flask, url_for, request, render_template
import time as time
import numpy as np
import os
import re

from weatherStation.util import beaufort as btf, logBME280, logDHT22, aneometer
from weatherStation.config import configs

# raspberry pi wind log file name pattern
fileNamePattern = aneometer.filePattern
# bme280 file pattern
bmeFilePattern = logBME280.file_name_pattern
# DHT22 file pattern
dht22FilePattern = logDHT22.file_name_pattern

# Dateipfad in dem sich die Logdateinen befinden
windlogsDir = configs.getLogDirPath(aneometer.CONFIG_FILE_NAME)
bme280Dir = configs.getLogDirPath(logBME280.CONFIG_FILE_NAME)
dht22Dir = configs.getLogDirPath(logDHT22.CONFIG_FILE_NAME)

CONFIG_FILE_NAME = 'website'

app = Flask(__name__)

def load_config_parameter():
    configs.get_config_parameter(CONFIG_FILE_NAME)
    host_pattern = r'^host=((\d{1,3}\.){3}(\d{1,3}))'
    port_pattern = r'^port=(\d{1,5})'
    debug_pattern =r'^debug=(true|false)?'

    parameter = dict(host='127.0.0.1', port=4242, debug=False)

    for l in configs.get_config_parameter(CONFIG_FILE_NAME):
        match = re.search(host_pattern, l)
        if match is not None:
            parameter['host'] = match.group(1)
            continue

        match = re.search(port_pattern, l)
        if match:
            parameter['port'] = match.group(1)
            continue

        match = re.search(debug_pattern, l)
        if match:
            if match.group(1) == 'true':
                parameter['debug'] = True
            else:
                parameter['debug'] = False
            continue
    return parameter





def calcVelocity(fname, start, stop):
    error = ''
    try:
        data = np.array([float(x) for x in open(windlogsDir + '/' + fname, 'r').readlines()], dtype=float)
    except ValueError:
        error = 'ValueError'
        lineNumber = 1
        for x in open(windlogsDir + '/' + fname, 'r').readlines():
            try:
                xfloat = float(x)
                lineNumber = lineNumber + 1
            except ValueError:
                # print 'ValueError in file',fname
                error = error + 'ValueError in file' + fname
                # print x,'in line',lineNumber+1,'cannot convert in a float!'
                error = error + str(x) + 'in line' + str(lineNumber + 1) + 'cannot convert in a float!'
                break
        return (error, '', '')

    dataInHoure = data[(data > start * 1000) & (data <= stop * 1000)]
    if dataInHoure.size < 2:
        return ('0.0', '0.0', '0.0')

    timeDiff = dataInHoure[1:-1] - dataInHoure[0:-2]
    vAvg = aneometer.v(timeDiff) * 3.6
    mean = round(np.sum(vAvg) / vAvg.size, 1)

    return (str(mean), str(round(max(vAvg), 1)), str(round(min(vAvg))))


def fetchLastBME280Data(fName):
    """
    Fetch the last logged data of the BME280 sensor as String.
    If no data of the current day are avalible
    only '-' for each value will return.
    """
    if os.path.isfile(fName) == False:
        return "-", "-", "-"

    # get the data from the file, skip the first line (header)
    data = [x.strip('\n').split(',') for x in open(fName, 'r').readlines()[1:]]
    # temperatur, pressure, humidity
    return data[-1][2], data[-1][3], data[-1][4]


def fetchLastDHT22Data(fName):
    """
    Fetch the last logged data of the DHT22 sensor as String.
    If no data of the current da are avalible
    only '-' for each value will return.
    """
    if os.path.isfile(fName) == False:
        return "-", "-"

    # get the data from the file, skip the first line (header)
    data = [x.strip('\n').split(',') for x in open(fName, 'r').readlines()[1:]]
    # temperature, , humidity
    if len(data) == 0:
        return '-', '-'

    temperature = '-'
    if data[-1][2] is not None:
        temperature = data[-1][2]
    humidity = '-'
    if data[-1][4] is not None:
        humidity = data[-1][4]

    return temperature, humidity


@app.route("/")
def index():
    timeSpan = 10  # [min]
    timeNow = time.mktime(time.localtime())  # [s]
    fileName = time.strftime(fileNamePattern, time.localtime(timeNow))
    bme280FileName = time.strftime(bmeFilePattern, time.localtime(timeNow))
    dht22FileName = time.strftime(dht22FilePattern, time.localtime(timeNow))

    if os.path.isfile(windlogsDir + '/' + fileName) == False:
        velocity, maxVelocity, minVelocity = '-', '-', '-'
        beaufort_scale = [0, 0, '-', '-', '-']
    else:
        pastTime = timeNow - 60 * timeSpan  # [s]
        velocity, maxVelocity, minVelocity = calcVelocity(fileName, pastTime, timeNow)
        beaufort_scale = btf.BEAUFORT_SCALAR[btf.fetchIndex(float(velocity) / 3.6)]

    temperature, pressure, humidity = fetchLastBME280Data(bme280Dir + '/' + bme280FileName)
    temperatureDHT22, humidityDHT22 = fetchLastDHT22Data(dht22Dir + '/' + dht22FileName)



    date = time.strftime('%d. %B %Y', time.localtime(timeNow))
    timeRange = time.strftime('%H:%M', time.localtime(timeNow))

    return render_template('index.html', temperature=temperature, pressure=pressure, humidity=humidity,
                           temperatureDHT22=temperatureDHT22, humidityDHT22=humidityDHT22,
                           velocity=velocity, beaufort=str(beaufort_scale[btf.BTF_NUMBER]),
                           beaufort_desc=beaufort_scale[btf.DESCRIPTION],
                           beaufort_desc_land=beaufort_scale[btf.VIS_EFFECT_LAND], maxVelocity=maxVelocity,
                           minVelocity=minVelocity, date=date, time=timeRange, range=timeSpan)

def run_website():
    app.run(**load_config_parameter())

if __name__ == '__main__':
    run_website()