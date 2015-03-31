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
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

# Create full path to lib + proj dir
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
proj_dir = os.path.abspath(os.path.join(src_dir, '../src'))

# Insert lib_dir and proj_dir before continuing forward
sys.path.insert(0, lib_dir)
sys.path.insert(0, proj_dir)

# import PYO stuff
from pyo import *
from audioserver import AudioServer
from sound import Sound

import sys
import time
# will use this to trace when functions begin and end
# see details from: http://stackoverflow.com/questions/308999/what-does-functools-wraps-do
import textwrap
from functools import wraps

server = AudioServer()

# gets instance of mic object for INPUT
m = Input(chnl=1, mul=2)

print "%r" % m
print m.__dir__()

# pass INPUT object mic to Sound object
s = Sound(m,freq=1,size=1024,overlaps=4,wintype=1,mul=1, add=0)

# call play function to OUTPUT sound
s.play()

while 1:
  try:
    n = random.uniform(.5, 5)
    s.setFreq(n)
  except KeyboardInterrupt:
    s.kill()
    exit()


# s = Server(sr=44100, nchnls=2, duplex=0).boot()

# a = SfPlayer('../snds/baseballmajeur_m.aif', loop=True)
# b = PinkNoise(.1)

# voc = MyVocoder(in1=a, in2=b, base=70, spread=[1.49,1.5], q=10, num=8).out()
# voc.ctrl()

# s.gui(locals())
