#!/usr/bin/python
#-*- coding: utf-8 -*-

import math

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
    @return - absolute humidity [kg/m^3]
    """
    return (e(phi,e_sat_w(T)))/(RD * T)


if __name__ == '__main__':
    temperature = 25.97 + 273.15
    print e_sat_w(temperature)
    print absoluteHumidity(0.5175,temperature)
    print absoluteHumidity(0.431,25.7+273.15)
