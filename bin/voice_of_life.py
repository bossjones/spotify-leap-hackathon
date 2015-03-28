#!/usr/bin/env python

# import os, sys, inspect

# # drops you down into pdb if exception is thrown
# import sys
# from IPython.core import ultratb
# sys.excepthook = ultratb.FormattedTB(mode='Verbose',
#      color_scheme='Linux', call_pdb=True, ostream=sys.__stdout__)

# src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
# sys.path.insert(0, lib_dir)
# import Leap

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

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# import PYO stuff
from audioserver import AudioServer
from sound import Sound

#from audioserver import *
#from sound import *

#import AudioServer
#import Sound
import sys

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def set_sound(self, sound_obj):
        self.sound = sound_obj

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def compute_factor(self, a_float):
       if a_float > 0:
         # positive
         # IF ITS POSITIVE: Factor = 1.25
         return float((a_float/100.00) + 1.00)
         #return float(0.5)
       else:
         # negative
         # IF ITS NEGATIVE: Factor = 0.25
         return float((abs(a_float)/100.00))
         #return float(0.5)

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # print self.compute_factor(normal.roll * Leap.RAD_TO_DEG)
            #self.sound.transpose( self.compute_factor(normal.roll * Leap.RAD_TO_DEG) )

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

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

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

# main thread
def main():

    ### PYO AUDIO SHIT

    # creates audo daemon
    server = AudioServer()

    # gets instance of mic object for INPUT
    m = server.getMic()

    # pass INPUT object mic to Sound object
    s = Sound(m)

    # call play function to OUTPUT sound
    s.transpose(2.5)
    s.play()

    #### LEAP MOTION SHIT

    # Create a sample listener and controller
    listener = SampleListener()
    listener.set_sound( s )
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    ### # Keep this process running until Enter is pressed
    ### print "Press Enter to quit..."
    ### try:
    ###     sys.stdin.readline()
    ### except KeyboardInterrupt:
    ###     pass
    ### finally:
    ###     # Remove the sample listener when done
    ###     s.kill()
    ###     controller.remove_listener(listener)

    while 1:
      try:
        #s.transpose(0.5)
        sys.stdin.readline()
      except KeyboardInterrupt:
        pass
      finally:
        print "cleaning up threads"
        # Remove the sample listener when done
        s.kill()
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
