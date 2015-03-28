from pyo import *
import threading

class Sound(object):
  kill_flag = 0
  threads = []

  def __init__(self, input):
    self.input = PVAnal(input, size=1024, overlaps=4, wintype=1)

  def transpose(self, freq):
    PVTranspose( self.input, transpo=freq )

  def play(self):
    p = PVAddSynth(self.input, pitch=1)
    t = threading.Thread( target=self.playBack, args=(p,) )
    t.start()
    self.threads.append(t)

  def playBack(self,p):
    p.out()
    while 1:
      if self.kill_flag == 1:
        print('kill')
        exit()

  def kill(self):
    self.kill_flag = 1
      # t.stop()

  # while 1:
  #   # print('test')






