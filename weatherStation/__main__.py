#!usr/bin/python

import os, sys
import appdirs

from weatherStation.util import logBME280

if __name__ == '__main__':
	logBME280.run()
