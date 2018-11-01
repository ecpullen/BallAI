import datetime
import random
import tkinter as tk
import numpy as np
from neuralNetwork import Node, Neural_Network
import time
from copy import deepcopy


class Ballio:

    def __init__(self):
        self.root = tk.Tk()
        self.width = 600
        self.height = 600
        self.balls = []
        self.paddles = []
        self.root.title("Ball.io")
        self.root.geometry("%dx%d+50+30" % (self.width, self.height))
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.root.lift()
        '''self.balls = []
        self.balls.append(Ball(600*random.random(),300 + 300*random.random(),10*random.random() - 5,0,50,'red',self.canvas))
        self.balls.append(
            Ball(600 * random.random(), 300 + 300 * random.random(), 10 * random.random() - 5, 0, 20, 'blue',
                 self.canvas))'''

        self.posX = [0, 20,2,2,2]

        self.paddles = []
        for x in self.posX:
            self.paddles.append(self.canvas.create_rectangle(x-75,500,x+75,505))

        
        '''self.canvas.bind('<Motion>', self.update_mouse)
        #create networks
        scores = [0 for _ in self.posX]
        time.sleep(1)
        while min(scores) > 0:
            self.root.update_idletasks()
            self.root.update()
            for b in self.balls:
                scores = b.update(self.posX,scores)
            self.move_paddles()
            print(scores)'''

        self.inputs = [Node(0) for _ in range(5)]
        self.outputs = [Node(0) for _ in range(2)]
        self.posX = []
        for _ in range(5):
            self.posX.append(300)
        nns = []#add neural networks       
        for x in range(5):
            nns.append(Neural_Network(self.inputs,self.outputs,[lambda : self.move(x,-10),lambda : self.move(x,10)],[3,3]))
        self.init()
        print(self.game(nns))

        for nn in nns:
            nn.fire_test()
        '''while True:
            print("top")
            time.sleep(1)
            self.init()
            scores = self.game(nns)
            ord = np.argsort(scores*-1)
            print(scores)
            print(len(nns))
            next_gen = [nns[x] for x in ord[0:2]]
            for _ in range(3):
                next_gen.append(Neural_Network(self.inputs,self.outputs,[],[3,3]))
            for i in range(len(next_gen)):
                next_gen[i].output_funcs = [lambda : self.move(i,-10),lambda : self.move(i,10)]'''
        '''
            Breed/repopulate nns
        '''
            #nns = next_gen

    def init(self):
        for ball in self.balls:
            self.canvas.delete(ball.circ)
        self.balls = []
        self.balls.append(
            Ball(600 * random.random(), 300 + 300 * random.random(), 10 * random.random() - 5, 0, 50, 'red',
                 self.canvas))
        self.balls.append(
            Ball(600 * random.random(), 300 + 300 * random.random(), 10 * random.random() - 5, 0, 20, 'blue',
                 self.canvas))
        self.move_paddles()

    def game(self,nns=[]):
        i = 0
        [bx,by] = self.balls[0].get()
        [rx,ry] = self.balls[1].get()
        for nn in nns:
            nn.evaluate([bx,by,rx,ry,self.posX[i]])
            i+=1
        scores = [0 for _ in self.posX]
        while max(scores) >= 0:
            self.root.update_idletasks()
            self.root.update()
            #update all nns
            for b in self.balls:
                scores = b.update(self.posX,scores)
            self.move_paddles()
            #print(scores)
        return scores;



    def update_mouse(self, event):
        self.posX[0] = max(0,min(600,event.x))

    def move_paddles(self):
        #print(len(self.paddles))
        for i in range(len(self.paddles)):
            self.canvas.coords(self.paddles[i],self.posX[i]-75,500,self.posX[i]+75,505)
        return

    def move(self, idx, delX):
        print("moving: ",idx, " by: ", delX, " to: ",self.posX[idx] + delX)
        self.posX[idx] += delX
        self.move_paddles()

class Ball:

    def __init__(self,x,y,xvel,yvel,rad, col, canvas):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.rad = rad
        self.canvas = canvas
        self.circ = self.canvas.create_oval(self.x-self.rad/2, 600 - (self.y-self.rad/2), self.x + self.rad/2, 600-(self.y + self.rad/2), fill = col)
        self.last_time = datetime.datetime.now()

    def update(self, posX, scores):
        #print(datetime.datetime.now() - self.last_time, " ", datetime.timedelta(milliseconds=10), "", (datetime.datetime.now() - self.last_time) > datetime.timedelta(milliseconds=10))
        if(datetime.datetime.now() - self.last_time) < datetime.timedelta(milliseconds=10):
            #print("skipping")
            return scores
        #print("updating: ", scores)
        self.last_time = datetime.datetime.now()
        self.x += self.xvel
        self.y += self.yvel
        self.yvel -= .1

        if self.x > 600 - self.rad/2 or self.x < self.rad/2:
            self.xvel *= -1

        if self.y > 600 - self.rad/2:
            self.yvel *= -1
            self.y = 600 - self.rad/2

        self.canvas.coords(self.circ, self.x-self.rad/2, 600 - (self.y-self.rad/2), self.x + self.rad/2, 600-(self.y + self.rad/2))


        if self.y < 100 + self.rad/2:
            for i in range(len(posX)):
                if scores[i] >= 0:
                    if abs(posX[i] - self.x) < 75:
                        print("bounced")
                        scores[i] += 100
                    else:
                        print("lose")
                        scores[i] = -scores[i] - 1
            print("turning")
            self.yvel *= -1
            self.y = 100 + self.rad/2
        return scores

    def get(self):
        return self.x,self.y


def main():
    Ballio()
    return


if __name__ == "__main__":
    main()