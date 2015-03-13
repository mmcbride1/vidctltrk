#!/usr/bin/python

import os
import sys
import time
import logging
import datetime
import subprocess
from subprocess import PIPE
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
   df = {} #########
   #################

   """
   Constructor for
   the ImageHandler

   """

   def __init__(self):

      self.cf = self.getParams();

      self.main()

   """
   Main function
   Executes the 
   series of remote
   processes

   """

   def main(self):

      cf = self.cf

      for host in cf[0:2] :

         if self.proc(host) == 0 :

            self.asgrmcnt(host)

            self.scp(host)

            self.trydel(host)

      return

   """
   For the delete 
   function, attempt
   5 times in case 
   of disconnect   

   """

   def trydel(self, host):

      self.host = host

      for x in range(0, 5) :

         res = self.delete(host)

         if res != '' :

            time.sleep(5)

         else :

            break

      return

   """
   Get the list 
   that contains the
   remote file names at
   the execution of this
   program

   """

   def getrmlst(self):

      return self.df

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
   Get the machine IP,
   or get the hostname
   for the full host
   address

   """

   def getHNIP(self, host, part):

      self.host = host

      self.part = part

      host = host.split(':')[0]

      return host.split('@')[part]

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
   Carry out ping 
   function to ensure 
   connectivity and 
   log any issues in
   the process

   """

   def proc(self, host):

      cf = self.cf

      self.host = host

      ip = self.getHNIP(host, 1)

      code = self.ping(ip)

      if code != 0 :

         self.logger(cf[9] + " " + str(code))

      return code

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

      lst = con.replace('\n', ' ')

      return lst.rstrip()

   """
   Assign remote 
   content. First take
   a snapshot of the 
   files in the scp
   directory and assign
   them to a list

   """

   def asgrmcnt(self, host):

      cf = self.cf

      self.host = host

      p = host.split(':')

      n = p[1].split(os.sep)

      self.df[n[2]] = self.check(p[0], p[1])

      return 

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

   def scp(self, host):

      cf = self.cf

      self.host = host

      cmd = self.scpcmd(host)

      ip = self.getHNIP(host, 1)

      proc = subprocess.Popen(cmd, shell=True)

      proc.wait()

      return

   """
   General SSH access
   to the remote hosts
   for selective 
   purposes

   """

   def ssh(self, host, cmd):

      cf = self.cf

      cmd_str = cf[7] % (cf[4], host, cmd)

      p = subprocess.Popen(cmd_str, shell=True, stderr=PIPE)

      return p.communicate()[1]

   """
   Prior to purging
   the remote image
   files, attempt
   to confirm that
   the copy was 
   successful

   """

   def flocal(self, lst):

      self.lst = lst

      cf = self.cf

      pth = cf[5] + '/images/'

      lst = lst.split(' ')

      for f in lst :

         if os.path.isfile(pth + f) == False :

            return False

      return True
      
   """
   Build the command
   that will purge
   the image files 
   from the remote 
   system 

   """

   def delcmd(self, inpt):

      self.inpt = inpt

      name = inpt[0].split('@')[0]

      flst = self.getrmlst()

      ext = self.flocal(flst[name])

      if (flst[name] != '') & (ext) :

         cmd = "cd %s; sudo rm %s"

         return cmd % (inpt[1], flst[name])

      else :

         return 0

   """
   Following the file
   copy, purge the 
   image files from 
   the remote system 

   """

   def delete(self, dirc):

      cf = self.cf

      self.dirc = dirc

      path = dirc.split(':')

      cmd = self.delcmd(path)
         
      if cmd != 0 :

         p = self.ssh(path[0], '"%s"' % cmd)

         return p

