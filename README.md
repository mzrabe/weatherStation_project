# weatherStation_project
This source code was developed to log the inner and outer 
temperature, humidity and the ambient pressure. Additionally to 
log the velocity of the wind via a cup anemometer. The code is
written to run on a raspberry pi 2 with Python3.4. 

This project includes also a Flask base website with published 
the current measured values.

### Add library to PYTHONPATH
To use this library comfortable in your project it necessary to add the
path to the PYTHONPATH environment variable.

export PYTHONPATH=\<path to the folder weatherStation_project\>

### Used libaries

- Flask
- numpy
- matplotlib
- appdirs

### Configuration on the raspberry pi

The python script use the packeage appdirs. See [appdirs package][1].
To define the location of the logfiles you have to create the following files.
For linux the config file has to create at this location ~/.config/weatherStation.

1. website
2. dht22
3. confings
4. bme280
5. anemometer

#### website
- host=\<On which IP is the website reachable.\>
- port=\<On which port is the website reachable.\>
- debug=\<Should the debuging enable or not\>

>###### The following pattern is required
>- host pattern = r'^host=((\d{1,3}\.){3}(\d{1,3}))'
>- port pattern = r'^port=(\d{1,5})'
>- debug pattern = r'^debug=(true|false)?'

#### dht22
Write in the first line the location to save the logging files.
It should have this formate e.g ~/weatherStation/dht22/

#### bme280
Write in the first line the location to save the logging files.
It should have this formate e.g ~/weatherStation/bme280/

#### configs
?

#### anemometer
Write in the first line the location to save the logging files.
It should have this formate e.g ~/weatherStation/anemometer/

[1]: <https://pypi.org/project/appdirs/#files> "Hobbit lifestyles"
