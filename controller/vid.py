#!/usr/bin/python

import os
import re
import uuid
import datetime
import subprocess

#
# *
# * VideoStager
# *
#

class VideoStager:

   """
   Get the configuration
   for the image and video 
   locations 
   
   """

   def config(self):
   
      file = '/etc/impt.conf'
   
      conf = open(file)
      
      stngs = conf.readlines()
      
      conf.close()
      
      stngs = [s.strip() for s in stngs]
      
      return stngs
      
   """
   Select the specific 
   configuration setting
   needed
   
   """
   
   def getConf(self, c):
   
      self.c = c
      
      return self.config()[c]

   """
   Produce a unique
   name for each import
   video file
   
   """
   
   def genID(self, file):
   
      self.file = file
      
      file = file.replace(":", "")
      
      id = uuid.uuid4()
      
      return "%s-%s" % (file, id)
      
   """
   Give the imported 
   file a name that is 
   appropriate for the
   vid conversion program
   
   """
   
   def rename(self, file):
   
      self.file = file
      
      return os.rename(file, self.genID(file))
      
   """
   Generate a unique 
   identifier for
   each converted video
   file
   
   """
   
   def vidname(self):
   
      now = datetime.datetime.now()
   
      sufx = str(now)
      
      sufx = re.sub(r'\W+', '', sufx)
      
      return "file%s.mp4" % (sufx)
      
   """
   Execute the video 
   conversion via 
   MP4Box and note the
   return code for later
   logging use
   
   """
   
   def MP4Box(self, file):
   
      self.file = file
      
      mp4 = 'MP4Box -add'
      
      vid = self.getConf(0) 
      
      vname = vid + self.vidname()
      
      cmd = "%s %s %s" % (mp4, file, vname)
      
      x = subprocess.call(cmd, shell=True)
      
      return x
      
   """
   Apply the given 
   function to each 
   file in the specified
   directory
   
   """
   
   def stage(self, root, func):
   
      self.root = root
      
      for subdir, dirs, files in os.walk(root):
      
         for file in files:
         
            func(os.path.join(subdir, file)) 
            
   """
   Purge the import 
   directory of all
   video files following
   conversion 
   
   """
   
   def purge(self, dir):
   
      self.dir = dir
      
      cmd = "sudo rm %s/*" % (dir)
      
      os.system(cmd)
      
      return 
      
   """
   Execute the staging
   functions 
   
   """
   
   def run(self):
   
      img = self.getConf(1)
      
      self.stage(img, self.rename)
      self.stage(img, self.MP4Box)
      
      self.purge(img)
      
      return 
         
