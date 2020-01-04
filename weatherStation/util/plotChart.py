#!/usr/bin/python
#-*- coding: utf-8 -*-

# IMPORTS
import pandas as pd
import time
import matplotlib.pyplot as plt

from weatherStation.config import configs
from weatherStation.util import aneometer

INNER_TEMPERATURE = 'inner temperature'
OUTER_TEMPERATURE = 'outer temperature'
INNER_HUMIDITY = 'inner humidity'
OUTER_HUMIDITY = 'outer humidity'
PRESSURE = 'pressure'
# name of configuration file
CONFIG_FILE_NAME = 'configs'

def plot_temperature_chart(inner_temperature, outer_temperature, figsize=configs.fig_size, title=None, file_name='temperature.png'):
    fig, ax = plt.subplots(figsize=figsize)

    # plot the data
    p1, = ax.plot(inner_temperature[configs.TIMESTAMP], inner_temperature[configs.TEMPERATURE], '-', label=INNER_TEMPERATURE, linewidth=1)
    p2, = ax.plot(outer_temperature[configs.TIMESTAMP], outer_temperature[configs.TEMPERATURE], '--', label=OUTER_TEMPERATURE, linewidth=1)

    # set labels
    ax.set_xlabel("time")
    ax.set_ylabel(u'temperature [°C]')

    # text size of the axes
    tkw = dict(size=4, width=1.5)
    # colors of the axes
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)

    # set the ticks of the x axis for each 6th value (full hour)
    plt.xticks(inner_temperature[configs.TIMESTAMP][::6], inner_temperature[configs.TIME].map(lambda x: x[:-3])[::6], rotation=45)
    plt.grid(linestyle='dashed', color='lightgray')
    plt.legend()

    # get the mean date of the time values for the name of the file
    print 'savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name

    plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
    plt.close()

def plot_humidity_chart(inner_humidity, outer_humidity, figsize=configs.fig_size, title=None, file_name='humidity.png'):
    fig, ax = plt.subplots(figsize=figsize)

    # plot the data
    p1, = ax.plot(inner_humidity[configs.TIMESTAMP], inner_humidity[configs.HUMIDITY], '-', label=INNER_HUMIDITY, linewidth=1)
    p2, = ax.plot(outer_humidity[configs.TIMESTAMP], outer_humidity[configs.HUMIDITY], '--', label=OUTER_HUMIDITY, linewidth=1)

    # set labels
    ax.set_xlabel("time")
    ax.set_ylabel(u'humidity [%]')

    # text size of the axes
    tkw = dict(size=4, width=1.5)
    # colors of the axes
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)

    # set the ticks of the x axis for each 6th value (full hour)
    plt.xticks(inner_humidity[configs.TIMESTAMP][::6], inner_humidity[configs.TIME].map(lambda x: x[:-3])[::6], rotation=45)
    plt.grid(linestyle='dashed', color='lightgray')
    plt.legend()

    # get the mean date of the time values for the name of the file
    print 'savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name

    plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
    plt.close()

def plot_pressure_chart(pressure, figsize=configs.fig_size, title=None, file_name='pressure.png'):
    fig, ax = plt.subplots(figsize=figsize)

    # plot the data
    p1, = ax.plot(pressure[configs.TIMESTAMP], pressure[configs.PRESSURE], '-', label=PRESSURE, linewidth=1)
    #p2, = ax.plot(outer_temperature[configs.TIMESTAMP], outer_temperature[configs.TEMPERATURE], '--', label=OUTER_TEMPERATURE, linewidth=1)

    # set labels
    ax.set_xlabel("time")
    ax.set_ylabel(u'pressure [hPa]')

    # text size of the axes
    tkw = dict(size=4, width=1.5)
    # colors of the axes
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)

    # set the ticks of the x axis for each 6th value (full hour)
    plt.xticks(pressure[configs.TIMESTAMP][::6], pressure[configs.TIME].map(lambda x: x[:-3])[::6], rotation=45)
    plt.grid(linestyle='dashed', color='lightgray')
    plt.legend()

    # get the mean date of the time values for the name of the file
    print 'savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name

    plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
    plt.close()

def plot_group_chart(inner, outer, figsize=configs.fig_size_group, title=None, file_name='groupChart.png'):
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=figsize, sharex=True, gridspec_kw={'hspace': 0})

    # plot the data
    ax1.plot(inner[configs.TIMESTAMP], inner[configs.TEMPERATURE], 'r-', label=INNER_TEMPERATURE, linewidth=1)
    ax1.plot(outer[configs.TIMESTAMP], outer[configs.TEMPERATURE], 'r--', label=OUTER_TEMPERATURE, linewidth=1)

    ax2.plot(inner[configs.TIMESTAMP], inner[configs.HUMIDITY], 'g-', label=INNER_HUMIDITY, linewidth=1)
    ax2.plot(outer[configs.TIMESTAMP], outer[configs.HUMIDITY], 'g--', label=OUTER_HUMIDITY, linewidth=1)

    ax3.plot(inner[configs.TIMESTAMP], inner[configs.PRESSURE], 'b-', label=PRESSURE, linewidth=1)

    # set labels
    plt.xlabel('time')
    ax1.set_ylabel(u'temperature [°C]')
    ax2.set_ylabel(u'humidity [%]')
    ax3.set_ylabel(u'pressure [hPa]')

    # text size of the axes
    tkw = dict(size=4, width=1.5)
    # colors of the axes
    ax1.tick_params(axis='y', colors='black', **tkw)
    ax2.tick_params(axis='y', colors='black', **tkw)
    ax3.tick_params(axis='y', colors='black', **tkw)

    # set the ticks of the x axis for each 6th value (full hour)
    plt.xticks(inner[configs.TIMESTAMP][::6], inner[configs.TIME].map(lambda x: x[:-3])[::6], rotation=45)
    ax1.grid(linestyle='dashed', color='lightgray')
    ax2.grid(linestyle='dashed', color='lightgray')
    ax3.grid(linestyle='dashed', color='lightgray')

    ax1.legend()
    ax2.legend()
    ax3.legend()

    # get the mean date of the time values for the name of the file
    print 'savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + file_name

    plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + file_name, format='png', bbox_inches='tight')
    plt.close()


def plot_hour_wind_log_chart(data, fileName=None, figsize=configs.fig_size, title=None):
    """
    Make a plot of the given wind log data. Before plotting the values averaging
    before for each time interval.

    @param data - hours and wind velocity values

    Parameters
    ----------
    data : hours and wind velocity values, data[0] - time in milliseconds, data[1] - wind velocity as hour average [km/h]
    fileName : file name of the chart to save
    figsize : size of the chart in inches
    title : title of the chart
    """

    # generate labels
    labels = [[], []]
    for x in data[0]:
        # get full hour time before xValue[-1]
        x_label_time = round(x / 3600000. - 0.5) * 3600000
        # add xticks label coordinate (time value on x axis)
        labels[0].append(x_label_time)
        # add the corresponding time as string
        labels[1].append(time.strftime('%H:%M', time.localtime(x_label_time / 1000.)))

    # get full hour time after xValue[-1]
    x_label_time = round(data[0][-1]/3600000.+0.5)*3600000
    labels[0].append(x_label_time)
    labels[1].append(time.strftime('%H:%M', time.localtime(x_label_time / 1000.)))

    # todo Den Part noch auslagern !!! In dieser Methode besser nur die Daten generieren.
    # print 'Start plotting ...'
    # Plot the wind velocity chart
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111)

    if title != None:
        plt.title(title)

    plt.xlabel('time')
    plt.ylabel('wind velocity [km/h]')

    ax.plot(data[0], data[1], '-', label='hourly average', linewidth=1)

    # generate the x axis labels
    timeinterval = data[0][1] - data[0][0]
    plt.xticks(labels[0], labels[1], rotation=45)
    # print 'legend'
    # plt.legend()
    plt.ylim(ymin=0)
    plt.xlim(labels[0][0] - timeinterval / 2.0, labels[0][-1] + 3 * timeinterval / 2.0)
    plt.grid(linestyle='dashed', color='lightgray')

    # get the mean date of the time values for the name of the file
    if fileName == None:
        fileName = 'hourValues_windlogs_' + time.strftime(aneometer.datePattern, time.localtime(
            data[0][int(len(data[0]) / 2)] / 1000.)) + '.png'

    print 'savefig', configs.getLogDirPath(CONFIG_FILE_NAME) + fileName

    plt.savefig(configs.getLogDirPath(CONFIG_FILE_NAME) + fileName, format='png', bbox_inches='tight')
    plt.close()