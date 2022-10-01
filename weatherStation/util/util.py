#!usr/bin/python
# -*- coding : utf-8 -*-

import time
import os
from weatherStation.util import logDHT22
from weatherStation.config import configs
import numpy as np
import pandas as pd
from scipy import stats

MILD_OUTLIER = 'mild'
EXTREME_OUTLIER = 'extreme'

def find_outlier(values, outlier_type = MILD_OUTLIER) -> object:
	"""
	Identify mild or extreme ouliers in the set of data.
	@param values set of values to check, type Numpy array
	@param outlier_type identifier whether to identify mild or extrem outliers
	Returns
	-------
	A filter array with true if the value is a outlier otherwise false
	"""
	# first quartile
	q1 = np.quantile(values, 0.25)
	# third quartile
	q3 = np.quantile(values, 0.75)

	# inter quartiles range
	iqr = q3-q1
	if outlier_type == EXTREME_OUTLIER:
		factor = 3
	else:
		factor = 1.5

	bottom_range = q1 - factor * iqr
	upper_range = q3 + factor * iqr

	return (values <= bottom_range) | (values >= upper_range)

def correct_value(x, y):
	"""

	Parameters
	----------
	x -
	y

	Returns
	-------

	"""
	# valid values
	#valid_y = y[[not x for x in find_outlier(y)]]

	#slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(values)), values)


# ~ #print q1, q3, min_range, max_range
# ~ #print 'dht22_data[\'temperature\'][i]= ',dht22_data[i,2]

# ~ if dht22_data[i,2] < min_range or dht22_data[i,2] > max_range:
# ~ #print False
# ~ select.append(True)
# ~ slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(values),values))
# ~ dht22_data[i,2] = intercept + slope * j
# ~ else:
# ~ #print True
# ~ select.append(True)

if __name__ == '__main__':
	values = np.array([4.491,4.462,4.407,4.550,4.438,4.74,4.48,5.67,4.651,4.722,4.752,4.699])
	print(values)
	print(find_outlier(values))
	print(values[[not x for x in find_outlier(values)]])

# ~ for i in range(dht22_data_lenght):
	# ~ num_values = 15
	# ~ idx_min = int(max(0,i-num_values/2.))
	# ~ idx_max = int(min(idx_min + num_values,dht22_data_lenght))

	# ~ if idx_max - idx_min != num_values:
		# ~ idx_min = int(max(0,idx_max-num_values))

	# ~ if i-num_values/2. >= 0 and i+num_values/2 <= dht22_data_lenght:
		# ~ j = 7
	# ~ elif i-num_values/2. < 0:
		# ~ j = i
	# ~ else:
		# ~ j = num_values - (dht22_data_lenght-i)

	# ~ num_values = idx_max - idx_min
	# ~ values = np.sort(dht22_data[idx_min:idx_max,2])
	# ~ #print 'values= ',values

	# ~ q1 = np.quantile(values,0.25)
	# ~ q3 = np.quantile(values,0.75)

	# ~ #print 'q1:', q1, np.quantile(values,0.25)
	# ~ #print 'q3:', q3, np.quantile(values,0.75)

	# ~ min_range = q1 - 1.5 * (q3-q1)
	# ~ max_range = q3 + 1.5 * (q3-q1)

	# ~ slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(values)),values)

	# ~ #print q1, q3, min_range, max_range
	# ~ #print 'dht22_data[\'temperature\'][i]= ',dht22_data[i,2]

	# ~ if dht22_data[i,2] < min_range or dht22_data[i,2] > max_range:
		# ~ #print False
		# ~ select.append(True)
		# ~ slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(values),values))
		# ~ dht22_data[i,2] = intercept + slope * j
	# ~ else:
		# ~ #print True
		# ~ select.append(True)
