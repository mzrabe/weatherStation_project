#-*- coding: utf-8 -*-
"""
This script is only to generate dummy data
for the logBME280.py script.
"""
from datetime import datetime
import random

def readBME280All():
    houre = datetime.now().strftime("%H")
    minute = datetime.now().strftime("%M")
    second = datetime.now().strftime("%S")

    return (float(houre)*random.randint(1,100)/100.),float(minute)*random.randint(1,100)/100.,float(second)*random.randint(1,100)/100.