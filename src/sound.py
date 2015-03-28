from pyo import *
import threading
# will use this to trace when functions begin and end
# see details from: http://stackoverflow.com/questions/308999/what-does-functools-wraps-do
import textwrap
from functools import wraps

# trace decorator
def trace(func):
    """Tracing wrapper to log when function enter/exit happens.
    :param func: Function to wrap
    :type func: callable
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Start {!r}'. format(func.__name__))
        result = func(*args, **kwargs)
        print('End {!r}'. format(func.__name__))
        return result
    return wrapper


class Sound(object):
  kill_flag = 0
  threads = []

  @trace
  def __init__(self, input):
    self.input = PVAnal(input, size=1024, overlaps=4, wintype=1)

  @trace
  def transpose(self, freq):
    PVTranspose( self.input, transpo=freq )

  @trace
  def play(self):
    p = PVAddSynth(self.input, pitch=1)
    t = threading.Thread( target=self.playBack, args=(p,) )
    t.start()
    self.threads.append(t)

  @trace
  def playBack(self,p):
    p.out()
    while 1:
      if self.kill_flag == 1:
        print('kill')
        exit()

  @trace
  def kill(self):
    self.kill_flag = 1





