
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

        self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.minSwipeLength = 500
        self.minSwipeVelocity = 1000
        self.controller.config.set("Gesture.Swipe.MinLength", self.minSwipeLength)
        self.controller.config.set("Gesture.Swipe.MinVelocity", self.minSwipeVelocity)
        self.controller.config.save()

        self.screenWidth = 600 # 1280
        self.screenHeight = 600 # 960
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight)) # FULLSCREEN
        
        self.frameSurface = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
        self.bgColor = (0,0,0)

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.joints = [] # stores .x .y .z values

        self.doneRunning = False

        self.tableDepth = 0
        self.hoverBuffer = 100

        self.hoveringColor = (150,0,250)
        self.touchingColor = (0,255,0)

        self.offsetX,self.offsetY,self.projectionWidth,self.projectionHeight = self.runCalibration()

    def invertPoints(self,x,y):
        nx = self.screenWidth - x
        ny = self.screenHeight - y
        return nx,ny

    def spacialToPixel(self,x,y):
        nx = x - self.offsetX
        ny = y - self.offsetY
        ny = -ny
        self.projectionWidth = abs(self.projectionWidth)
        self.projectionHeight = abs(self.projectionHeight)
        nx = abs(nx*self.screenWidth/self.projectionWidth)
        ny = abs(ny*self.screenHeight/self.projectionHeight)
        return nx,ny

    def runCalibration(self):
        calibrated = False

        coords = []

        while not calibrated:


            self.screen.fill(self.bgColor)
            self.drawCalib()

            frame = self.controller.frame()
            self.updateFingerData(frame)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(self.joints) > 0:
                    coords.append((self.joints[0],self.joints[2]))
                    self.tableDepth += self.joints[1]
                    if len(coords) == 2:
                        calibrated = True
                        break

        x0,y0 = coords[0] 
        x1,y1 = coords[1]
        width = abs(x1 - x0)
        height = abs(y1 - y0)
        self.tableDepth = self.tableDepth/2
        return x0,y0,width,height
                        
    def drawCalib(self):
        color = (0,255,0) if len(self.joints) > 0 else (150,0,250)
        pygame.draw.rect(self.screen,color,(0,0,self.screenWidth,self.screenHeight))
        pygame.display.flip()

    def isTouchingSurface(self):
        return self.joints[1] > self.tableDepth

    def isHoveringSurface(self):
        return self.joints[1] > self.tableDepth - self.hoverBuffer

    def updateFingerData(self,frame):
        self.joints = []
        if len(frame.hands) > 0:
            finger = frame.hands[0].fingers.frontmost
            self.joints = [finger.tip_position.x,finger.tip_position.y,finger.tip_position.z]

    def timerFired(self):
        frame = self.controller.frame()
        self.updateFingerData(frame)

    def fingerTouchingSurface(self):
        return len(self.joints) > 0 and self.isTouchingSurface()
    

    def fingerHoveringSurface(self):
        return len(self.joints) > 0 and self.isHoveringSurface()


    def keyPressed(self,key):
        if key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE:
            self.doneRunning = True
        elif key == pygame.K_SPACE:
            print 'getting data'
            if len(self.joints) > 0:
                print 'X: %d, Y: %d, Z: %d' % (
                        self.joints[0], self.joints[1], self.joints[2])

    def drawCirclesOnFingertip(self):
        if len(self.joints) > 0:
            if self.isTouchingSurface():
                color = self.touchingColor
            elif self.isHoveringSurface():
                color = self.hoveringColor
            else:
                color = self.bgColor
            cx,cy = self.joints[0],self.joints[2]
            nx,ny = self.spacialToPixel(cx,cy)
            x,y = self.invertPoints(nx,ny)
            pygame.draw.circle(self.screen,color,(int(x),int(y)),20)


    def redrawAll(self):
        if len(self.joints) > 0:
            pygame.draw.rect(self.screen,(255,255,255),(0,0,20,20))
            self.drawCirclesOnFingertip()
        '''
        if self.fingerTouchingSurface():
            pygame.draw.circle(self.screen,self.touchingColor,(self.screenWidth//2,self.screenHeight//2),self.screenHeight//4)
        elif self.fingerHoveringSurface():
            pygame.draw.circle(self.screen,self.hoveringColor,(self.screenWidth//2,self.screenHeight//2),self.screenHeight//4)
'''

    def run(self):

        while not self.doneRunning:

            self.clock.tick(self.fps)
            self.timerFired()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doneRunning = True
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