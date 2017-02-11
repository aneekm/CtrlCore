'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame, os
import serial
import colorsys
from time import sleep

class PygameGame(object):

    def init(self):
        self.MENU = 0
        self.LIGHTS = 1
        self.MUSIC = 2
        self.TEMP = 3
        self.SECURITY = 4 
        self.mode = self.MENU
        self.colors=dict()
        self.colors[0] = (244,241,222)
        self.colors[1] = (224,122,95)
        self.colors[2] = (146,220,229)
        self.colors[3] = (129,178,154)
        self.colors[4] = (242,204,143)
        self.colors[5] = (82, 73, 72)
        self.lightsOn = False
        self.TL = 4 if self.lightsOn == False else 5
        self.TR = 0
        self.BL = 6
        self.BR = 2
        self.offset = self.width/2
        self.quadrant1 = False;
        self.quadrant2 = False;
        self.quadrant3 = False;
        self.quadrant4 = False;
        self.brightness = self.Slider(self.width * 5/6, self.height * 1/6, self.width * 3/24, self.height * 2/3, self.screen, self.colors[1], self.colors[5], True, value = 50, maxVal = 100)
        self.color = self.Slider(self.width/2, self.height * 1/6, self.width * 1/5, self.height * 2/3, self.screen, self.colors[1], self.colors[5], True, value = 0, maxVal = 360, image = 'spectrum.png')
        self.port = serial.Serial()
        initializePort(self.port)
        self.LED = False;
        self.musicState = 11
        self.secState = 13

    class Slider(object):

        def __init__(self, x, y, width, height, screen, slideColor, backColor, vertical = True, value = 0, maxVal = 100, image = None):
            self.x = x
            self.y = y
            self.sliderw = width
            self.sliderh = height
            self.screen = screen
            self.vertical = vertical
            self.value = value
            self.maxVal = maxVal
            self.slideColor = slideColor
            self.backColor = backColor
            self.slideW = .9 * self.sliderw
            self.slideH = .1 * self.sliderh
            self.slideX = self.x + 0.05 * self.sliderw
            self.slideY = (((self.value) * (self.sliderh)) / (self.maxVal)) + self.y - .5*self.slideH
            if not image == None:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                rel_path = "resources\images"
                full_images_dir_path = os.path.join(script_dir, rel_path)
                self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join(full_images_dir_path, image)).convert_alpha(),90), (self.sliderw,self.sliderh))
            else:
                self.image = None

        def getVal(self):
            return self.value

        def setVal(self, val):
            self.value = val
            print 'val: ' + str(val)
            self.slideY = (((self.value) * (self.sliderh)) / (self.maxVal)) + self.y - .5*self.slideH

        def checkSliderConstraints(self, x, y):
            if x > self.x and x < self.x + self.sliderw:
                if y > self.y and y < self.y + self.sliderh:
                    print 'inside slider'
                    return True
                else:
                    return False
            else: 
                return False

        def drawSlider(self):
            if self.image == None:
                pygame.draw.rect(self.screen, self.backColor, (self.x, self.y, self.sliderw, self.sliderh))
            else:
                self.screen.blit(self.image, (self.x, self.y, self.sliderw, self.sliderh))
            pygame.draw.rect(self.screen, self.slideColor, (self.slideX, self.slideY, self.slideW, self.slideH))



    def mousePressed(self, x, y):
        if self.mode == self.MENU:
            if (x < self.width/2 and x > 0):
                if (y < self.height/2 and y > 0):
                    self.lightsPressed()
                elif(y < self.height and y > self.height/2):
                    self.tempPressed()
            elif (x > self.width/2 and x < self.width):
                if (y < self.height/2 and y > 0):
                    self.musicPressed()
                elif(y > 0 and y > self.height/2):
                    self.securityPressed()
        if self.mode == self.LIGHTS:
            if self.brightness.checkSliderConstraints(x, y):
                i = ((y-self.brightness.y) * self.brightness.maxVal) / self.brightness.sliderh
                self.brightness.setVal(i)
                changeColor(self.color.getVal(), self.brightness.getVal(), self.port)
            elif self.color.checkSliderConstraints(x, y):
                i = ((y-self.color.y) * self.color.maxVal) / self.color.sliderh
                self.color.setVal(i)
                changeColor(self.color.getVal(), self.brightness.getVal(), self.port)
            elif x < self.width/2 and x > 0:
                if self.LED:
                    turnOff(self.color.getVal(), self.brightness.getVal(), self.port)
                    self.LED = not self.LED
                else: 
                    turnOn(self.port)
                    self.LED = not self.LED
        if self.mode == self.MUSIC:
            if self.musicState <= 11:
                self.musicState += 1
            elif self.musicState == 12:
                self.musicState = 13
                self.mode = self.MENU
        if self.mode == self.MUSIC:
            if self.musicState < 16:
                self.musicState+=1
            else:
                self.musicState = 13
                self.mode = self.MENU
        if self.mode == self.TEMP:
            self.mode = self.MENU

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        if (self.mode == self.MENU):
            if (x <=1 or x >= self.width-1 or y <= 1 or y >= self.height-1):
                self.quadrant1, self.quadrant2, self.quadrant3, self.quadrant4 = False, False, False, False
            elif (x < self.width/2 and x > 0):
                if (y < self.height/2 and y > 0):
                    self.quadrant2 = True;
                    self.quadrant1, self.quadrant3, self.quadrant4 = False, False, False
                elif(y > 0 and y > self.height/2):
                    self.quadrant3 = True;
                    self.quadrant1, self.quadrant2, self.quadrant4 = False, False, False
            elif (x > self.width/2 and x < self.width):
                if (y < self.height/2 and y > 0):
                    self.quadrant1 = True;
                    self.quadrant2, self.quadrant3, self.quadrant4 = False, False, False
                elif(y > 0 and y > self.height/2):
                    self.quadrant4 = True;
                    self.quadrant1, self.quadrant3, self.quadrant2 = False, False, False

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def lightsPressed(self):
        self.mode = self.LIGHTS

    def musicPressed(self):
        self.mode = self.SECURITY

    def tempPressed(self):
        pass
        self.mode = self.TEMP

    def securityPressed(self):
        pass
        self.mode = self.MUSIC

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if self.offset > 0:
            self.offset-=5

    def redrawAll(self):
        #if on the main menu
        if self.mode == self.MENU:
            if (not self.quadrant2):
                pygame.draw.rect(self.screen, self.colors[1], (self.width*0-self.offset, self.height*7/16,self.width/2, self.height/20))
            else:
                pygame.draw.rect(self.screen, self.colors[1], (0-self.offset, 0, self.width/2, self.height/2))
            if (not self.quadrant1):
                pygame.draw.rect(self.screen, self.colors[2], (self.width/2+self.offset, self.height*7/16,self.width/2, self.height/20))
            else:
                pygame.draw.rect(self.screen, self.colors[2], (self.width/2+self.offset, 0, self.width/2, self.height/2))
            if (not self.quadrant3):
                pygame.draw.rect(self.screen, self.colors[3], (self.width*0-self.offset, self.height*15/16,self.width/2, self.height/20))
            else: 
                pygame.draw.rect(self.screen, self.colors[3], (0-self.offset, self.height/2, self.width/2, self.height))
            if (not self.quadrant4):
                pygame.draw.rect(self.screen, self.colors[4], (self.width/2+self.offset, self.height*15/16,self.width/2, self.height/20))
            else:
                pygame.draw.rect(self.screen, self.colors[4], (self.width/2+self.offset, self.height/2, self.width/2, self.height))
            self.screen.blit(self.textures[self.TL],(self.width*1/4 - self.iconSize/2-self.offset, self.height*1/4 - self.iconSize/2))
            self.screen.blit(self.textures[self.TR],(self.width*3/4 - self.iconSize/2+self.offset, self.height*1/4 - self.iconSize/2))
            self.screen.blit(self.textures[self.BL],(self.width*1/4 - self.iconSize/2-self.offset, self.height*3/4 - self.iconSize/2))
            self.screen.blit(self.textures[self.BR],(self.width*3/4 - self.iconSize/2+self.offset, self.height*3/4 - self.iconSize/2))
        elif self.mode == self.LIGHTS:
            self.brightness.drawSlider()
            self.color.drawSlider()
            self.screen.blit(self.textures[self.TL],(self.width*1/4 - self.iconSize/2-self.offset, self.height/2 - self.iconSize/2))
        elif self.mode == self.SECURITY:
            self.screen.fill(self.bgColor)
            self.screen.blit(self.textures[self.secState],(0,0))
        elif self.mode == self.MUSIC:
            self.screen.fill(self.bgColor)
            self.screen.blit(self.textures[self.musicState],(0,0))
        elif self.mode == self.TEMP:
            self.screen.fill(self.bgColor)
            self.screen.blit(self.textures[10],(0,0))

    def initImages(self):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "resources\images"
        full_images_dir_path = os.path.join(script_dir, rel_path)
        self.textures = dict ()
        self.iconSize = 200
        self.textures[0] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "volume_on.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[1] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "volume_off.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[2] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "lock.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[3] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "lock_open.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[4] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "light_on.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[5] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "light_off.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[6] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "cloud.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[7] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "snow.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[8] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "rain.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[9] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "warm.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[10] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "temp.png")).convert_alpha(), (self.width,self.height))
        self.textures[11] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "music.png")).convert_alpha(), (self.width,self.height))
        self.textures[12] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "musicPlaying.png")).convert_alpha(), (self.width,self.height))
        self.textures[13] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "sec.png")).convert_alpha(), (self.width,self.height))
        self.textures[14] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "sec_armed.png")).convert_alpha(), (self.width,self.height))
        self.textures[15] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "sec_armed_locked.png")).convert_alpha(), (self.width,self.height))
        self.textures[16] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "sec_armed_locked_on.png")).convert_alpha(), (self.width,self.height))

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1280/2, height=960/2, fps=60, title="Slider Test"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (244,241,222)
        
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.initImages()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.screen.fill(self.bgColor)
            self.redrawAll()
            pygame.display.flip()

        pygame.quit()

#Arguments: port - a Serial object that has already been initialized
#Result: Initializes port to 57600 baudrate through COM4 on Windows and returns True if successful, False if not
def initializePort(port):
    port.baudrate = 57600;
    port.port = 'COM4'
    port.open()
    if (port.isOpen()):
        return True
    else:
        return False

#Arguments: colorString - a string representation of an int that represents a 0-255 color value
#Result: Makes it the complete 3-digit length for the serial port
def fixColorString(colorString):
    while(len(colorString) < 3):
        colorString = '0' + colorString
    return colorString

#Arguments: degree - a float from 0 to 360 
#           brightness - a float from 0 to 100
#           port - Serial port to send out the color data 
#Result: changes the color sent to the serial port to the values given
def changeColor(degree, brightness, port):
    h = degree/360.0
    l = brightness/100.0
    (r, g, b) = colorsys.hls_to_rgb(h, l, 1)
    R, G, B = int(255 * r), int(255 * g), int(255 * b)
    port.write(fixColorString(str(R))+fixColorString(str(G))+fixColorString(str(B))+'\n')


#Arguments: port - Serial port to send out color data
#Goal: turns on the LEDs on initiation and fades up to solid bright white
def turnOn(port):
    for i in range(0, 256, 10):
        port.write(fixColorString(str(i))+fixColorString(str(i))+fixColorString(str(i))+'\n')
        sleep(0.1)

#Arguments: degree - a float from 0 to 360 
#           brightness - a float from 0 to 100
#           port - Serial port to send out the color data 
#Result: turns off the LED strip by slowling fading to black 
def turnOff(degree, brightness, port):
    h = degree/360.0
    l = brightness/100.0
    (r, g, b) = colorsys.hls_to_rgb(h, l, 1)
    R, G, B = int(255 * r), int(255 * g), int(255 * b)
    r_sub, g_sub, b_sub = R/20.0, G/20.0, B/20.0
    for i in range(1, 21):
        port.write(fixColorString(str(int(R-(r_sub * i))))+fixColorString(str(int(G-(g_sub * i))))+fixColorString(str(int(B-(b_sub* i)))+'\n'))
        sleep(0.15)

#Result: initialized Pygame's sound mixer so music can be played. Uses default settings
def initMusic():
    pygame.mixer.init()
    if (pygame.mixer.get_init() != None):
        return True
    else: 
        return False

#Arguments: filename - path to music file being played
#Result: file is loaded into music mixer and played.
def playSong(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

#The following 4 methods set up play/pause, stop, and volume
def stopSong():
    pygame.mixer.music.stop()

def pauseSong():
    pygame.mixer.music.pause()

def unpauseSong():
    pygame.mixer.music.unpause()

def setVolume(vol):
    vol = vol/100.0
    pygame.mixer.music.set_volume(vol)



def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
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
self.self.screen.blit(projected, (offsetX, offsetY))"""