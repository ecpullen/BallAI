import datetime
import random
import tkinter as tk
import numpy as np
from neuralnet import Node, Neural_Network
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

        self.posX = [0]

        
        #nn = Neural_Network([5,3,2,2])
        #print(nn)
        '''
        nn.network[1][0].weights = [1,-1,0,0,0]
        nn.network[1][1].weights = [0,0,1,-1,0]
        nn.network[1][2].weights = [0,0,0,-1,1]
        nn.network[1][0].bias = 0
        nn.network[1][1].bias = 0
        nn.network[1][2].bias = 0

        nn.network[2][0].weights = [1,1,0]
        nn.network[2][1].weights = [-1,0,-1]
        nn.network[2][0].bias = -2
        nn.network[2][1].bias = 0

        nn.network[3][0].weights = [1,1]
        nn.network[3][1].weights = [-1,-1]
        nn.network[3][0].bias = -1
        nn.network[3][1].bias = 0
        
        self.init()
        self.game([nn])
        '''

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

        '''self.inputs = [Node(0) for _ in range(5)]
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
            pass'''
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
        nns = [Neural_Network([2,2]) for _ in range(20)]


        nn = Neural_Network([2,2])
        #print(nn)
        
        nn.network[1][0].weights = [-1,1]
        nn.network[1][1].weights = [1,1]
        nn.network[1][0].bias = 0
        nn.network[1][1].bias = 0

        self.posX = [300 for _ in nns]
        #print("len",len(self.posX))
        nns[0] = nn.get_copy()
        self.paddles = []
        for x in self.posX:
            self.paddles.append(self.canvas.create_rectangle(x-75,500,x+75,505, fill = 'grey'))
        self.init()
        self.game(nns)

    def init(self):
        for ball in self.balls:
            self.canvas.delete(ball.circ)
        self.balls = []
        self.balls.append(
            Ball(600 * random.random(), 300 + 300 * random.random(), 10 * random.random() - 5, 0, 50, 'red',
                 self.canvas))
        '''self.balls.append(
            Ball(600 * random.random(), 300 + 300 * random.random(), 10 * random.random() - 5, 0, 20, 'blue',
                 self.canvas))'''
        self.move_paddles()

    def game(self,nns=[]):
        i = 0
        scores = [0 for _ in nns]
        while max(scores) >= 0:
            self.root.update_idletasks()
            self.root.update()
            self.update_nn(nns)
            for b in self.balls:
                b.update(self.posX,nns)
            self.move_paddles()
            #print(scores)
        return scores;

    def update_nn(self, nns):
        [bx,by] = self.balls[0].get()
        #[rx,ry] = self.balls[1].get()
        #print("len",len(self.posX))
        for i in range(len(nns)):
            #print(self.posX[i])
            outs = nns[i].evaluate([bx,self.posX[i]])
            # outs = nns[i].evaluate([by,ry,bx,self.posX[i],rx])
            if outs[0] == 1:
                self.move(i,-10)
            if outs[1] == 1:
                self.move(i,10)

    def update_mouse(self, event):
        self.posX[0] = max(0,min(600,event.x))

    def move_paddles(self):
        #print(len(self.paddles))
        for i in range(len(self.paddles)):
            self.canvas.coords(self.paddles[i],self.posX[i]-75,500+i/5,self.posX[i]+75,505+2*i/5)
        return

    def move(self, idx, delX):
        print("moving: ",idx, " by: ", delX, " to: ",self.posX[idx] + delX)
        self.posX[idx] = min(600,max(0,self.posX[idx]+delX))
        #self.move_paddles()

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

    def update(self, posX, nns):
        #print(datetime.datetime.now() - self.last_time, " ", datetime.timedelta(milliseconds=10), "", (datetime.datetime.now() - self.last_time) > datetime.timedelta(milliseconds=10))
        if(datetime.datetime.now() - self.last_time) < datetime.timedelta(milliseconds=10):
            return
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
        #print(self.x, ", ",self.y)

        if self.y < 100 + self.rad/2:
            for i in range(len(posX)):
                if abs(posX[i] - self.x) < 75:
                    pass
                else:
                    nns[i] = Neural_Network.breed(random.choice(nns),random.choice(nns),2)
            #print("turning")
            self.yvel *= -1
            self.y = 100 + self.rad/2
        return
    def get(self):
        return [self.x,self.y]


def main():
    Ballio()
    return


if __name__ == "__main__":
    main()