#!/usr/bin/python
#-*- coding: utf-8 -*-

# IMPORTS
import os
import appdirs

# size of the figure for the wind velocity and the pressure, humidity and temperature chart
fig_size = (12, 4)
fig_size_group = (12, 8)

## CSV - field names
DATE = 'date'
TIME = 'time'
DATE_TIME = 'date_time'
TIMESTAMP = 'timestamp'
TEMPERATURE = 'temperature'
PRESSURE = 'pressure'
HUMIDITY = 'humidity'

def getLogDirPath(name):
    """
    Get the path of directory at which the log files should store.
    On MacOS:           ~/Library/Application Support/<AppName>
    on Windows (XP):    C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>
        or possibly:
                        C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>
    on Linux:
    
    @param name - name of sensor which data should log

    Returns
    -------
    object

    """
    # get path to log directory
    configPath = os.path.join(appdirs.user_config_dir('weatherStation'),name)
    
    if os.path.isfile(configPath):
        configFile = open(configPath,'r')
        # Read the first line of the configuration file
        # which specified the path where the log files
        # should store.
        return configFile.readline()
    else:
        print('Please define the path where the log files should stored in the config-file :',configPath)
        return ''


def get_config_parameter(name):
    """
    Get the path of directory at which the log files should store.
    On MacOS:           ~/Library/Application Support/<AppName>
    on Windows (XP):    C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>
        or possibly:
                        C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>
    on Linux:

    @param name - name of sensor which data should log

    Returns
    -------
    object

    """
    # get path to log directory
    configPath = os.path.join(appdirs.user_config_dir('weatherStation'), name)

    if os.path.isfile(configPath):
        configFile = open(configPath, 'r')
        # Read the first line of the configuration file
        # which specified the path where the log files
        # should store.
        return configFile.readlines()
    else:
        print('Please define the path where the log files should stored in the config-file :', configPath)
        return ''