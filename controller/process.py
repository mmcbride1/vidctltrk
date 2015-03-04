#!/usr/bin/python

import os
import sys
import time
import subprocess
from xtra import purgetool
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

# __init()__ #

while True :

   if checksys() == 0 :

      img = ImageHandler()

      vid = VideoStager()

      vid.run()

      purgetool.ridfile()

   time.sleep(60)
