#!/usr/bin/env python
# encoding: utf-8
"""
Main script using hand-written Audo Obj (defined in lib/sound.py).

"""

import os, sys, inspect

# drops you down into pdb if exception is thrown
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=True, ostream=sys.__stdout__)

# Get dir from which python script was called
# src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

# # Create full path to lib + proj dir
# lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
# proj_dir = os.path.abspath(os.path.join(src_dir, '../src'))

# # Insert lib_dir and proj_dir before continuing forward
# sys.path.insert(0, lib_dir)
# sys.path.insert(0, proj_dir)

# import PYO stuff
from pyo import *
#from audioserver import AudioServer
#from sound import Sound

#import sys
import time
# will use this to trace when functions begin and end
# see details from: http://stackoverflow.com/questions/308999/what-does-functools-wraps-do
import textwrap
from functools import wraps

# Disabled # server = AudioServer()

# server = Server().boot()
# server.start()

# # gets instance of mic object for INPUT
# m = Input(chnl=1, mul=2)

### Disabled # m = server.getMic()

# pass INPUT object mic to Sound object
# DISABLED # s = Sound(m)

# call play function to OUTPUT sound
# s.play()
##### DISABLED # pvt  = s.getPVT()
##### DISABLED # pvas = PVAddSynth(pvt).out()
##### DISABLED # dry  = Delay(m, delay=1024./server.getConnection().getSamplingRate(), mul=.7).out(1)
##### DISABLED # pva = PVAnal(input, size=int(size))
##### DISABLED # pvt = PVTranspose(self._pva, transpo=float(freq))

def main():

  server = Server().boot()
  server.start()

  # gets instance of mic object for INPUT
  m   = Input(chnl=1, mul=2)
  pva = PVAnal(m, size=1024)
  pvt = PVTranspose(pva, transpo=1.5)
  pvs = PVSynth(pvt).out()
  dry = Delay(m, delay=1024./server.getSamplingRate(), mul=.7).out(1)


# while 1:
#   try:
#     n = random.uniform(.5, 5)
#     s.setFreq(n)
#     s.transpose()
#   except KeyboardInterrupt:
#     server.stop()
#     s.kill()
#     exit()
  while 1:
    try:
      #s.transpose(0.5)
      sys.stdin.readline()
    except KeyboardInterrupt:
      pass
    finally:
      print "cleaning up threads"
      sys.exit(0)
      # Remove the sample listener when done

# s = Server(sr=44100, nchnls=2, duplex=0).boot()

# a = SfPlayer('../snds/baseballmajeur_m.aif', loop=True)
# b = PinkNoise(.1)

# voc = MyVocoder(in1=a, in2=b, base=70, spread=[1.49,1.5], q=10, num=8).out()
# voc.ctrl()

# s.gui(locals())

if __name__ == "__main__":
    main()
