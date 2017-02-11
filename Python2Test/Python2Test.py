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
        self.colors[2] = (61,64,91)
        self.colors[3] = (129,178,154)
        self.colors[4] = (242,204,143)
        self.TL = 4
        self.TR = 0
        self.BL = 6
        self.BR = 11
        self.offset = self.width/2

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def lightsPressed(self):
        self.mode = self.LIGHTS

    def musicPressed(self):
        self.mode = self.LIGHTS

    def tempPressed(self):
        self.mode = self.LIGHTS

    def securityPressed(self):
        self.mode = self.LIGHTS

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if self.offset > 0:
            self.offset-=5

    def redrawAll(self, screen):
        #if on the main menu
        pygame.draw.rect(screen, self.colors[1], (self.width*0-self.offset, self.height*7/16,self.width/2, self.height/20))
        pygame.draw.rect(screen, self.colors[2], (self.width/2+self.offset, self.height*7/16,self.width/2, self.height/20))
        pygame.draw.rect(screen, self.colors[3], (self.width*0-self.offset, self.height*15/16,self.width/2, self.height/20))
        pygame.draw.rect(screen, self.colors[4], (self.width/2+self.offset, self.height*15/16,self.width/2, self.height/20))
        screen.blit(self.textures[self.TL],(self.width*1/4 - self.iconSize/2-self.offset, self.height*1/4 - self.iconSize/2))
        screen.blit(self.textures[self.TR],(self.width*3/4 - self.iconSize/2+self.offset, self.height*1/4 - self.iconSize/2))
        screen.blit(self.textures[self.BL],(self.width*1/4 - self.iconSize/2-self.offset, self.height*3/4 - self.iconSize/2))
        screen.blit(self.textures[self.BR],(self.width*3/4 - self.iconSize/2+self.offset, self.height*3/4 - self.iconSize/2))

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
        self.textures[10] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "cloud.png")).convert_alpha(), (self.iconSize,self.iconSize))
        self.textures[11] = pygame.transform.scale(pygame.image.load(os.path.join(full_images_dir_path, "camera.png")).convert_alpha(), (self.iconSize,self.iconSize))
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
        screen = pygame.display.set_mode((self.width, self.height))
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
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


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
self.screen.blit(projected, (offsetX, offsetY))"""