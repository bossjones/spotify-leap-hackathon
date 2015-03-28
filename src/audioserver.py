from pyo import *

class AudioServer:

  def __init__(self):
    self.connection = Server().boot()
    self.connection.start()

  def stop(self):
    self.connection.stop()

  def getMic(self):
    return Input(chnl=1, mul=2)
