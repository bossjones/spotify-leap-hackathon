from pyo import *

class AudioServer(object):

  def __init__(self):
    self.connection = Server(sr=44100, nchnls=2, duplex=0).boot()
    self.connection.start()

  def stop(self):
    self.connection.stop()

  def getMic(self):
    return Input(chnl=1, mul=2)
