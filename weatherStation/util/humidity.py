#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import pandas as pd

# Get the system specific configuration which are set up
# individual from the system user.
from weatherStation.config import configs

# Gas constante of vapor 461.51 [J/(kg*K)]
RD = 461.51

def e_sat_w(temperature):
    """
    Calculate equilibrium vapor pressure 
    according Magnus
    @param temperature - temperature of the air [K]
    @return - equilibrium vapor pressure [Pa]
    """
    return 611.2 * math.exp(17.62 * (temperature-273.15) / (243.12 + (temperature-273.15)))

def e(phi, e_sat_w):
    """
    @param phi - relative humidity [1]
    @param e_sat_w - equilibrium vapor pressure [Pa]
    @return - partial pressure of water vapor [Pa]
    """ 
    return phi * e_sat_w

def relative_humidity(e, T):
    """
    Relative humidity of air
    Unit : [1]
    @param e - partial pressure of water vapor [Pa]
    @param T - air temperature [K]
    @return - relative humidity
    """
    return e/e_sat_w(temperature)

def absolute_humidity(phi, T):
    """
    Calculate the absolute humidity according the relative
    humidity and the air temperature.
    @param phi - relative humidity [1]
    @param T - air temperature [K]
    @return - absolute humidity [g/m^3]
    """
    return (e(phi,e_sat_w(T)))/(RD * T)*1000

def absolute_humidity_df(df):
    """
    Calculate the absolute humidity according the relative
    humidity and the air temperature.

    Parameters
    ----------
    df - panda dataframe
    """
    df[configs.HUMIDITY_ABS] = df.apply(lambda x : absolute_humidity(x[configs.HUMIDITY], x[configs.TEMPERATURE]+273.15), axis=1)
    return df


if __name__ == '__main__':
    temperature = 25.97 + 273.15
    print(e_sat_w(temperature))
    print(absolute_humidity(0.5175,temperature))
    print(absolute_humidity(0.431,25.7+273.15))

    df = pd.DataFrame({configs.HUMIDITY:[0.5,0.43, 0.9], configs.TEMPERATURE:[20, 15, 10]})
    absolute_humidity_df(df)
    print(df)