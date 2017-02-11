#TartanHacks 2017 pyserial implementation and
#LED light methods and 
#Pygame Music player implementation

import serial
import colorsys
from time import sleep
import pygame

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
#			brightness - a float from 0 to 100
#			port - Serial port to send out the color data 
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
#			brightness - a float from 0 to 100
#			port - Serial port to send out the color data 
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


if __name__ == '__main__':
	'''port = serial.Serial()
	initializePort(port)
	turnOn(port)
	print 'turned on'
	for i in range(0, 360, 5):
		changeColor(i, 50, port)
		sleep(0.05)
	print 'spectrum complete'
	turnOff(0, 100, port)
	print 'turned off'''

	initMusic()
	playSong('Lil Wayne - New Slaves.mp3')

