#!/usr/bin/python

"""
# PurgeTool

This module will be
used to manage all 
artifacts generated
from the videotruck
process. This module
will also be extended 
to handle logging and 
service check tasks

"""

import os

SIZE = 1024.0 * 1024.0

"""
Make the file name
and the size limit
configurable

"""

def loadconf():

   config = {}

   vid = '/home/vidctl/vidctltrk/controller'

   vid = vid + "/xtra/purge.conf"

   execfile(vid, config)

   return config

"""
Determine the current
size of the param file.
Convert to MB

"""

def logsize(inpt):

   bytez = os.path.getsize(inpt)

   return (bytez / SIZE)

"""
Open the log
file and empty
the contents

"""

def mkfile(inpt):

   file = open(inpt, 'w')

   file.close()

   return

"""
If the current param
file is larger than
set limit, delete 
the file

"""

def ridfile():

   cf = loadconf()

   limit = cf['limit']

   if (os.path.isfile(cf['file'])) :

      if (logsize(cf['file']) > float(limit)) :

         mkfile(cf['file'])

   return
