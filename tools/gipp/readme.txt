================================================
GIPP-Geospatial Information Parallel Processor.
Copyright www.supermap.com 
Author: wangerqi@supermap.com
Rev.0.0.1,2014-06-13.
-------------------------------------------------

This version using:
python 2.7
simplejson
geojson
MQTT client for python
mosquitto,MQTT broker

How to install to ubuntu:
1 python
  sudo apt-get install python
  sudo apt-get install python-pip
  sudo pip install simplejson

2 mosquitto
  If you want using local MQTT broker:
  sudo apt-get install mosquitto
  
3 MQTT client for python
   please visit: http://git.eclipse.org/c/paho
   mkdir mqttc_python
   cd mqttc_python
   git clone git://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git
   cd org.eclipse.paho.mqtt.python
   sudo python setup.py install
   
That's OK.   