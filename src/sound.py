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
  def __init__(self, input, freq=1,size=1024,overlaps=4,wintype=1,mul=1, add=0):
    # Properly initialize PyoObject's basic attributes
    # PyoObject.__init__(self,size,overlaps,wintype)
    #PyoObject.__init__(self)

    ## DISABLED # self.input = PVAnal(input, size=1024, overlaps=4, wintype=1)
    self._input = input
    self._freq  = freq
    self._mul   = mul
    self._add   = add
    freq,mul,add,lmax = convertArgsToLists(freq,mul,add)
    self._pva = PVAnal(input, size=size, overlaps=overlaps, wintype=wintype)
    self._pvt = PVTranspose(self._pva, transpo=freq)
    self._pvas = PVAddSynth(self._pvt, pitch=1, num=100, first=0, inc=1, mul=mul, add=add)
    self._base_objs = self._pvas.getBaseObjects()

  def __dir__(self):
      return ["freq"]

  @trace
  def setFreq(self, x):
      """
      Replace the `freq` attribute.

      :Args:

          x : float or PyoObject
              New `freq` attribute.

      """
      self._freq = x
      self._pvt.transpo = x

  @property
  def freq(self): return self._freq
  @freq.setter
  def freq(self, x): self.setFreq(x)

  def setInput(self, x):
      """
      Replace the `input` attribute.

      :Args:

          x : float or PyoObject
              New `input` attribute.

      """
      self._input = x
      self._pvt.transpo = x

  @property
  def input(self): return self._input
  @input.setter
  def input(self, x): self.setInput(x)


  # @trace
  # def get_input(self):
  #   return self.input

  # @trace
  # def transpose(self):
  #   PVTranspose( self.input, transpo=self.freq )

  # @trace
  # def play(self):
  #   p = PVAddSynth(self.input, pitch=1)
  #   t = threading.Thread( target=self.playBack, args=(p,) )
  #   t.start()
  #   self.threads.append(t)

  @trace
  def play(self):
    #PVTranspose(self._input, transpo=self.freq)
    #p = PVAddSynth(self.input, pitch=1)
    p = self._pvas
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





