from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as KController
from pynput.keyboard import Key
import time
import os
import random
from PIL import ImageOps, ImageGrab
from numpy import *
import math
import cv2
import numpy as np
from neuralNetwork import Neural_Network, Node
import copy

mouse = Controller()
keyboard = KController()
# cookedFish = [16100, 16900]
# rawFish = [14000, 14550]

ballColor = [(137, 25, 16, 255)]
boardColor = [(0, 150, 0, 255)]

scrWOffset = 10
scrHOffset = 275

ballRadius = 25

scrWidth = 1200
scrHeight = 1425

score_pos = (2*587-scrWOffset, 2*269-scrHOffset)

in_game_pos = (2*33-scrWOffset, 2*266-scrHOffset)

start_button_pos = (308, 192)
start_cursor_pos = (300, 500)


mousex = 350
mousey = 500

def screenGrab():
	box = (0, 0, 2880, 1800)
	im = ImageGrab.grab(box)
	im.save('full_snap_' + str(int(time.time())) + '.png', 'PNG')
	return im

def leftClick():
	mouse.press(Button.left)
	time.sleep(.1)
	mouse.release(Button.left)

def leftClick(cord):
	mousePos(cord)
	time.sleep(.1)
	mouse.press(Button.left)
	time.sleep(.1)
	mouse.release(Button.left)

def leftDown():
	mouse.press(Button.left)
	time.sleep(.1)
		 
def leftUp():
	mouse.release(Button.left)
	time.sleep(.1)

def rightClick():
	mouse.press(Button.right)
	time.sleep(.1)
	mouse.release(Button.right)

def rightDown():
	mouse.press(Button.right)
	time.sleep(.1)
		 
def rightUp():
	mouse.release(Button.right)
	time.sleep(.1)
	print("left release")

def mousePos(cord):
	mouse.position = (cord[0], cord[1])

def get_cords():
	x,y = mouse.position
	print(x,y)
	return (x, y)

def isRed(tupl):
	if tupl[0] >= 120 and tupl[1] < 50 and tupl[2] < 50:
		return True
	return False

def isGreen(tupl):
	if tupl[1] >= 120 and tupl[0] < 70 and tupl[2] < 70:
		return True
	return False

def isBlue(tupl):
	if tupl[2] >= 120 and tupl[0] < 70 and tupl[1] < 70:
		return True
	return False

def get_image():
	box = (scrWOffset, scrHOffset, scrWidth + scrWOffset, scrHeight + scrHOffset)
	im = ImageGrab.grab(box)
	return im

def analyzeImage():
	im = get_image()
	# im.save('screen.png', 'PNG')
	red_xvals = []
	red_yvals = []

	blue_xvals = []
	blue_yvals = []

	in_game = False
	score = 0

	if isGreen(im.getpixel(in_game_pos)):
		in_game = True

	score = im.getpixel(score_pos)[0]*30

	for i in range(0, im.size[0], 5): 
		for j in range(0, im.size[1], 5): 
			pixelColor = im.getpixel((i, j))
			if isRed(pixelColor):
				red_xvals.append(i)
				red_yvals.append(j)
			if isBlue(pixelColor):
				blue_xvals.append(i)
				blue_yvals.append(j)				

	ri = (min(red_xvals) + max(red_xvals))/2
	rj = max(red_yvals)

	bi = (min(blue_xvals) + max(blue_xvals))/2
	bj = max(blue_yvals)

	# box = (scrWOffset + bi - ballRadius, scrHOffset + bj - ballRadius, scrWOffset + bi + ballRadius, scrHOffset + bj + ballRadius,)
	# im = ImageGrab.grab(box)
	# im.save('blueball.png', 'PNG')  

	# box = (scrWOffset + ri - ballRadius, scrHOffset + rj - ballRadius, scrWOffset + ri + ballRadius, scrHOffset + rj + ballRadius,)
	# im = ImageGrab.grab(box)
	# im.save('redball.png', 'PNG') 	 

	return [[ri/600, rj/600, bi/600, bj/600], score, in_game]

def playAGame(neur):
	if not isGreen(get_image().getpixel(in_game_pos)):
		leftClick(start_button_pos)
		mousePos(start_cursor_pos)

	im = get_image()
	im.save("screen.png", "PNG")

	while not isGreen(get_image().getpixel(in_game_pos)):
		time.sleep(.01)

	while isGreen(get_image().getpixel(in_game_pos)):
		print("in while loop")
		vals = analyzeImage()[0]
		vals.append(get_cords()[0]/600)
		neur.evaluate(vals)
		print("finished evaluating")

	print("exited whilee loop")

	print("score is: ", get_image().getpixel(score_pos)[0]*30)
	return analyzeImage()[2]


def main():
	bx = Node(0)
	by = Node(0)
	rx = Node(0)
	ry = Node(0)
	mx = Node(0)

	ml = Node(0)
	mr = Node(0)

	inputs_test = [bx, by, rx, ry, mx]
	outputs_test = [ml, mr]


	def move_right():
		coords = get_cords()
		mousePos((coords[0] + 50,coords[1]))
		print("move_right: ", get_cords())

	def move_left():
		coords = get_cords()
		mousePos((coords[0] - 50,coords[1]))
		print("move_left", get_cords())

	output_funcs = [move_left, move_right]


	nns = []
	for _ in range(3):
		nns.append(Neural_Network(copy.deepcopy(inputs_test), copy.deepcopy(outputs_test), output_funcs, [3, 3]))
	# nn = Neural_Network(inputs_test, outputs_test, output_funcs, [3, 3])

	# print(nn)
	time.sleep(3)
	scores = []
	while(True):
		for n in nns:
			scores.append(playAGame(n))
		print(scores)
		ord_scores = np.argsort(scores)
		next_gen = []
		for i in ord_scores[0:5]:
			next_gen.append(nns[i])
		temp = []
		for a in next_gen:
			for b in next_gen:
				temp.append(Neural_Network.breed(a,b))
		nns = temp
	

if __name__ == "__main__":
	main()
