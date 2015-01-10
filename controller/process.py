#!/usr/bin/python

import os
import sys
import subprocess
from img import ImageHandler
from vid import VideoStager

"""
Ping the sensor 
machine. if not 
reachable, no 
need to execute 

"""

def checksys():

   host = "192.168.1.101"

   cmd = "ping -c 1 %s" % (host)

   stat = subprocess.call(cmd, shell=True)

   return stat

## execute ##

if checksys() == 0 :

   img = ImageHandler()

   vid = VideoStager()

   vid.run()

else :

   sys.exit()
