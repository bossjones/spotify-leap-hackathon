# spotify-leap-hackathon
Repo for Synthesis &amp; Samples Music Hackathon.

# brew requirements

```
brew install liblo libsndfile portaudio portmidi
```

*On the Mac, it is very simple to build pyo from source with the Homebrew package mananger:**

```
# source: https://code.google.com/p/pyo/wiki/Installation
brew install python liblo libsndfile portaudio portmidi
cd /tmp
svn checkout http://pyo.googlecode.com/svn/trunk/ pyo
cd pyo
python setup.py install --use-coreaudio --use-double --universal
```


*A short gist explaining how to compile pyo - the powerful Audio/DSP library for Python, on Mac OS X. The instructions are specifically for installing pyo with a brewed Python install - not with Mac OS X system Python.*

```
# source: https://gist.github.com/pwalsh/5691534
# using brew installed Python
 
brew install portaudio portmidi libsndfile liblo jack
 
brew link portaudio portmidi libsndfile liblo
 
cd ~/Sites/tmp
 
svn checkout http://pyo.googlecode.com/svn/trunk/ pyo-read-only
 
cd pyo-read-only
 
python setup.py install --use-coreaudio --use-jack --use-double
 
cd ../
 
sudo rm -r pyo-read-only
```

** Fix for LeapPython.so and using homebrew python **

```
install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python \
/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib \
LeapPython.so
```

```
# Info on static libs installed
Python-pyo (version 0.7.5)

System requirements : OS X 10.6 to 10.10

This package installs all the required components to run pyo inside your current Python installation. Python 2.6 or 2.7 (32/64 bit) must be already installed on your system.

This package is divided into two separate installers. If you do not require one of them, please unselect the package in custom installation mode.

1. pyo extension:
The following components will be installed in the site-packages folder of the current Python Framework:

_pyo.so
_pyo64.so
pyo.py
pyo64.py
pyolib (folder)

2. Support libraries (i386 and x86_64):
This component will install a number of dynamic libraries on which pyo depends. If you already have these, then you can skip this installation.

Warning: this installation will overwrite any previously installed libraries. These are the libraries that will be installed in your /usr/local/lib directory:

liblo.7.dylib
libportaudio.2.dylib
libportmidi.dylib
libsndfile.1.dylib
libFLAC.8.dylib
libvorbisenc.2.dylib
libvorbis.0.dylib
libogg.0.dylib

Olivier Bélanger, 2015
````
