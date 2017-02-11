
#import Leap, sys, thread, time 
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x86'#'../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, '/Josh\Hackathons\TartanHacks\LeapDeveloperKit_3.2.0+45899_win\LeapDeveloperKit_3.2.0+45899_win\LeapSDK\lib/x86')

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import pygame

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):

        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            for pointable in hand.pointables:

                print '      X: %d, Y: %d, Z: %d' % (
                    pointable.tip_position.x,
                    pointable.tip_position.y,
                    pointable.tip_position.z)


        if not frame.hands.is_empty:
            print ""


class Runtime(object):

    def __init__(self):

        pygame.init()

        # leap inits
        self.listener = SampleListener()
        self.controller = Leap.Controller()

        self.screenWidth = 200 # 1280
        self.screenHeight = 200 # 960
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight)) # FULLSCREEN
        
        self.frameSurface = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
        self.bgColor = (0,0,0)

        # self.gameMode = 

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.joints = [] # stores .x .y .z values

        self.done = False

        self.hoveringColor = (150,0,250)
        self.touchingColor = (0,255,0)

    def updateFingerData(self):
        frame = self.controller.frame()
        self.joints = frame.hands

    def timerFired(self):
        self.updateFingerData()


    def fingerTouchingSurface(self):
        for hand in self.joints:
            for finger in hand.pointables:
                if finger.tip_position.y > 800:
                    print finger
                    return True
        return False

    def fingerHoveringSurface(self):
        for hand in self.joints:
            for finger in hand.pointables:
                if finger.tip_position.y > 700:
                    print finger
                    return True
        return False


    def keyPressed(self,key):
        if key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE:
            self.done = True
        elif key == pygame.K_SPACE:
            print 'getting data'
            for hand in self.joints:
                for finger in hand.pointables:
                    tip = finger.tip_position
                    print 'X: %d, Y: %d, Z: %d' % (
                        tip.x, tip.y, tip.z)


    def redrawAll(self):
        if self.fingerTouchingSurface():
            pygame.draw.circle(self.screen,self.touchingColor,(self.screenWidth//2,self.screenHeight//2),self.screenHeight//2)
        elif self.fingerHoveringSurface():
            pygame.draw.circle(self.screen,self.hoveringColor,(self.screenWidth//2,self.screenHeight//2),self.screenHeight//2)

    def run(self):

        while not self.done:

            self.clock.tick(self.fps)
            self.timerFired()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event.key)

            self.screen.fill(self.bgColor)
            self.redrawAll()
            pygame.display.flip()

        pygame.quit()



def main():
    
    project = Runtime()
    project.run()
    

if __name__ == "__main__":
    main()

"""
#init functions
    self.CALIBRATE = 0
    self.MENU = 1
    self.LIGHTS = 2
    self.MUSIC = 3
    self.DATA = 4
    #all of the other modes here
def calibrate(self):
    if self.mode == self.CALIBRATE:
        x1,y1 = (...)
        x2,y2 = (...)
        x3,y3 = (...)
        x4,y4 = (...)
        self.scaledW = ((x2-x1)+(x4-x3))/2
        self.scaledH = ((y3-y1)+(y4-y2))/2
        self.offsetX = (x1+x3)/2
        self.offsetY = (y1+y2)/2
        self.projected = pygame.Surface(scaledW, scaledH)
        self.projected.fill(0,255,0)

#put this in redraw all
self.screen.blit(projected, (offsetX, offsetY))
"""