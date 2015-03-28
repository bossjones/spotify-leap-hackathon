from audioserver import *
from audioserver import *
from sound import *
import sys

server = AudioServer()
m = server.getMic()
s = Sound(m)
s.play()

while 1:
  try:
    n = random.uniform(.5, 3)
    s.transpose(n)
  except KeyboardInterrupt:
    # threads = threading.enumerate()
    # for t in threads:
    #   t.stop()
    s.kill()
    exit()

# s.transpose(1.5)


# repos; cd spotify-leap-hackathon/;
