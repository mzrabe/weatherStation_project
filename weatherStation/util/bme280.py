#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script is only to generate dummy data
for the logBME280.py script.
"""
from datetime import datetime

def readBME280All():
    houre = datetime.now().strftime("%H")
    minute = datetime.now().strftime("%M")
    second = datetime.now().strftime("%S")

    return float(houre),float(minute),float(second)