#!/usr/bin/python

import os
import sys
import logging
import datetime
import subprocess
from xml.dom import minidom

#
# *
# * ImageHandler * #
# *
#

class ImageHandler:

   # configuration #
   #################
   cf = [] #########
   #################

   """
   Constructor for
   the ImageHandler

   """

   def __init__(self):

      self.cf = self.getParams();

      self.scp()

      self.delete()

   """
   Retrieve the 
   configuration file
   and store the paramters

   """

   def conf(self, file):

      self.file = file

      args = []

      xml = minidom.parse(file)

      al = xml.getElementsByTagName('item')

      for a in al :

         args.append(a.attributes['name'].value) 

      return args

   """
   Distribute the
   configuration params
   into reusable objects 

   """

   def getParams(self):

      params = self.conf('/etc/img.conf')

      return params

   """
   Get the machine IP
   for the full host
   address

   """

   def getIP(self, host):

      self.host = host

      host = host.split(':')[0]

      return host.split('@')[1]

   """
   Log keeping for
   remote connections
   and others

   """

   def logger(self, mg):

      cf = self.cf
      
      self.mg = mg

      t = datetime.datetime.now()

      t = str(t).split(".")[0]

      ins = " %s: %s" % (t, mg)

      logging.basicConfig(filename=cf[8], level=logging.ERROR)
      
      logging.error(ins)

   """
   Before connecting
   for file operations
   ensure connectivity

   """

   def ping(self, host):

      self.host = host

      cmd = "ping -c 1 %s" % (host) 

      proc = subprocess.call(cmd, shell=True)

      return proc

   """
   Check connectivity
   and attempt to 
   connect a max of
   five times

   """

   def proc(self, host):

      cf = self.cf
      
      self.host = host

      for i in range(5):

         code = self.ping(host)

         if code == 0:

            break

         if i == 4:

            self.logger(cf[9] + " " + str(code))

            sys.exit()

   """
   Build the needed 
   command for the 
   file copy 

   """

   def scpcmd(self, host):

      cf = self.cf
      
      self.host = host

      cmd = cf[6] % (cf[4], host, cf[5])

      return cmd

   """
   Execute the file
   copy for each host
   in the conf list

   """ 

   def scp(self):

      cf = self.cf

      for host in cf[0:2] :

         cmd = self.scpcmd(host)

         ip = self.getIP(host)

         self.proc(ip)

         proc = subprocess.Popen(cmd, shell=True)

         proc.wait()

   """
   General SSH access
   to the remote hosts
   for selective 
   purposes

   """

   def ssh(self, host, cmd):

      cf = self.cf

      cmd_str = cf[7] % (cf[4], host, cmd)

      subprocess.Popen(cmd_str, shell=True)
      
   """
   Quick directory 
   check to evaluate 
   contents
   
   """
   
   def check(self, host, dirc):
   
      cf = self.cf
      
      self.host = host
      self.dirc = dirc
      
      cmd = "ls -A %s" % (dirc)
      
      chk = cf[7] % (cf[4], host, cmd)
      
      con = os.popen(chk).read()
      
      return 0 if (con == "") else 1

   """
   Following the file
   copy, purge the 
   image files from 
   the remote system 

   """

   def delete(self):

      cf = self.cf

      for dirc in cf[0:2] :

         path = dirc.split(':')

         cmd = "sudo rm %s/*" % (path[1])

         ip = self.getIP(dirc)

         self.proc(ip)
         
         if self.check(path[0], path[1]) == 1 :

            self.ssh(path[0], cmd)

