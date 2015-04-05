#!/usr/bin/env python

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

import Leap, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# import PYO stuff
from pyo import *

import sys

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

def callback(arg):
    s.freq = arg

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        super(SampleListener, self).__init__()
        # NOTE: How to trigger function on value change
        # source: http://stackoverflow.com/questions/6190468/how-to-trigger-function-on-value-change
        self._roll_degrees = 0.0
        self._observers = []

    @trace
    def get_roll(self):
        print "GET_ROLL: %f" % self._roll_degrees
        return self._roll_degrees

    @trace
    def set_roll(self, value):
        self._roll_degrees = self.compute_factor(value * Leap.RAD_TO_DEG)
        print "set_roll: %f" % (self._roll_degrees)

    @trace
    def on_init(self, controller):
        print "Initialized"

    @trace
    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    @trace
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    @trace
    def on_exit(self, controller):
        print "Exited"

    @trace
    def compute_factor(self, a_float):
       if a_float > 0:
         # positive
         # IF ITS POSITIVE: Factor = 1.25
         return float((a_float/100.00) + 10.00)
       else:
         # negative
         # IF ITS NEGATIVE: Factor = 0.25
         return float((abs(a_float)/100.00))
    @trace
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # NOTE: Trigger callback
            self.set_roll(normal.roll)

            # Get arm bone
            arm = hand.arm

            # Get fingers
            for finger in hand.fingers:

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""
    @trace
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

if __name__ == "__main__":

    # NOTE: Good example
    # Source: https://gist.github.com/jordanorelli/4569165

    server = Server().boot()
    server.start()


    # gets instance of mic object for INPUT
    m   = Input(chnl=1, mul=2)
    pva = PVAnal(m, size=1024)
    pvt = PVTranspose(pva, transpo=1.5)
    pvs = PVSynth(pvt).out()
    dry = Delay(m, delay=1024./server.getSamplingRate(), mul=.7).out(1)

    time.sleep(1)

    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    server.gui(locals())

    _transpo = listener.get_roll()
    pvt.setTranspo(_transpo)

    sys.stdin.readline()
    controller.remove_listener(listener)
