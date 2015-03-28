#!/usr/bin/env python

import os, sys, inspect

# drops you down into pdb if exception is thrown
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=True, ostream=sys.__stdout__)

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)
import Leap
