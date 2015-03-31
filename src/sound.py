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

    # WORKING
    # self.m = Input(chnl=1, mul=2)
    # pva = PVAnal(m, size=1024)
    # pvt = PVTranspose(pva, transpo=1.5)
    # pvs = PVSynth(pvt).out()
    # dry = Delay(m, delay=1024./s.getSamplingRate(), mul=.7).out(1)

    self._freq  = freq
    self._mul   = mul
    self._add   = add
    self._pva = PVAnal(input, size=int(size))
    self._pvt = PVTranspose(self._pva, transpo=float(freq))
    #self._base_objs = self._pvas.getBaseObjects()

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

  @trace
  def transpose(self):
    self._pvt = PVTranspose( self._pva, transpo=float(self._freq) )

  # @trace
  # def play(self):
  #   p = PVAddSynth(self.input, pitch=1)
  #   t = threading.Thread( target=self.playBack, args=(p,) )
  #   t.start()
  #   self.threads.append(t)

  def getPVT(self):
    return self._pvt

  @trace
  def play(self):
      self._pvas  = PVAddSynth(self._pvt).out()


  # @trace
  # def play(self):
  #   #PVTranspose(self._input, transpo=self.freq)
  #   #p = PVAddSynth(self.input, pitch=1)
  #   p = self._pvas
  #   t = threading.Thread( target=self.playBack, args=(p,) )
  #   t.start()
  #   self.threads.append(t)

  # @trace
  # def playBack(self,p):
  #   p.out()
  #   while 1:
  #     if self.kill_flag == 1:
  #       print('kill')
  #       exit()

  # @trace
  # def kill(self):
  #   self.kill_flag = 1





