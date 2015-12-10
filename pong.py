"""
Dumb little pong game written in Python using Tkinter. Pretty bad code.
It kind of works, though.
Written by Katherine Martinez and Jan Martinez (no relation) for 65-150
"""

from Tkinter import *
import random

HEIGHT = 500
WIDTH  = 500
THRESH = 10

class Game:
    def __init__(self, master):
        ## Set Canvas
        #global WIDTH
        #global HEIGHT
        #self.tk = Tk()
        self.canvas = Canvas(master, width = WIDTH, height = HEIGHT)
        self.canvas.pack()

        ## Start/Restart button
        self.button = Button(master, text = "Play?", command = self.start)
        self.button.pack()

        ## Set labels that display scores
        self.scoreP = 0     # player score
        self.scoreC = 0     # computer score
        ## Variables and instances that change the scores within the canvas
        self.scoreP_var = IntVar()
        self.scoreC_var = IntVar()
        self.scoreP_var.set(self.scoreP)
        self.scoreC_var.set(self.scoreC)
        self.scoreP_txt = Label(master, textvariable = self.scoreP_var,
                                font=("Arial", 20))
        self.scoreC_txt = Label(master, textvariable = self.scoreC_var,
                                font=("Arial", 20))
        self.scoreC_txt.pack(side = LEFT)
        self.scoreP_txt.pack(side = RIGHT)
        
        ## Parameters
        self.size = 20      # diameter of ball
        self.padWid = 20    # width of paddles
        self.padLen  = 60   # length of paddle
        
        ## Draw ball and paddles and a border or something
        self.ball = self.canvas.create_oval(WIDTH / 2, HEIGHT / 2,
                                            (WIDTH / 2) + self.size,
                                            (HEIGHT / 2) + self.size,
                                            fill = "red")
        self.player = self.canvas.create_rectangle(WIDTH - THRESH - self.padWid,
                                                   HEIGHT / 2,
                                                   WIDTH - THRESH,
                                                   (HEIGHT / 2) + self.padLen,
                                                   fill = "black")
        self.comp = self.canvas.create_rectangle(THRESH, HEIGHT / 2,
                                                 THRESH + self.padWid,
                                                 (HEIGHT / 2) + self.padLen,
                                                 fill = "black")
        self.border = self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT,
                                                   fill = '', outline = "green",
                                                   width = THRESH)

    def updateGame(self):
        ## Method that updates the game

        ## Variables that hold coordinates of all objects
        self.player_coords = self.canvas.coords(self.player)
        self.comp_coords = self.canvas.coords(self.comp)
        self.ball_coords = self.canvas.coords(self.ball)
        
        self.scored()
        self.updateBall()
        self.compAI()
        self.hitPaddle()
        ## Calls itself after 50msec
        root.after(50, self.updateGame)

    def start(self):
        self.canvas.bind("<Motion>", self.move)
        self.reset()
        self.updateGame()

    def move(self, event):
        self.x, self.y = event.x, event.y
        self.player_coords[0] = self.x - (self.padWid / 2)
        self.player_coords[1] = self.y - (self.padLen / 2)
        self.player_coords[2] = self.x + (self.padWid / 2)
        self.player_coords[3] = self.y + (self.padLen / 2)
        self.canvas.coords(self.player, self.player_coords[0],
                           self.player_coords[1], self.player_coords[2],
                           self.player_coords[3])

    def compAI(self):
        ## Just moves the computer paddle a bit towards the ball
        if (self.comp_coords[1] > self.ball_coords[3] and
            self.comp_coords[1] > 0):
            self.canvas.move(self.comp, 0, -10)
        elif (self.comp_coords[3] < self.ball_coords[1] and
              self.comp_coords[3] < HEIGHT):
            self.canvas.move(self.comp, 0, 10)

    def updateBall(self):
        ## Moves the ball... yep, that's it
        self.isOutOfBounds()
        self.canvas.move(self.ball, self.dirx, self.diry)

    def isOutOfBounds(self):
        ## Bounces on top and bottom
        if (self.canvas.coords(self.ball)[1] <= THRESH or
            self.canvas.coords(self.ball)[3] >= HEIGHT - THRESH):
            self.diry = -1 * self.diry

    def hitPaddle(self):
        ## Bounces back when it hits the paddles
        ## This is weird-looking code
        ## Basically bounce when ball and paddles have same coordinates
        if ((self.comp_coords[1] < self.ball_coords[3] and
             self.comp_coords[3] > self.ball_coords[1] and
             self.comp_coords[2] >= self.ball_coords[0]) or
            (self.player_coords[1] < self.player_coords[3] and
             self.player_coords[3] > self.ball_coords[1] and
             self.player_coords[0] <= self.ball_coords[2])):
            self.dirx = -1 * self.dirx

    def scored(self):
        ## Updates score if ball reaches a side and resets ball
        if (self.ball_coords[0] < THRESH):
            self.scoreP += 1
            self.scoreP_var.set(self.scoreP)
            self.reset()
        elif (self.ball_coords[2] > WIDTH - THRESH):
            self.scoreC += 1
            self.scoreC_var.set(self.scoreC)
            self.reset()

    def reset(self):
        ## Reset ball in the middle
        self.canvas.coords(self.ball, WIDTH / 2, HEIGHT / 2,
                           (WIDTH / 2) + self.size,
                           (HEIGHT / 2) + self.size)
        ## Pick a random velocity
        self.dirx = random.randint(5, 15)
        self.diry = random.randint(5, 15)
        self.dirx += (2 * self.dirx) * random.randint(-1, 0)
        self.diry += (2 * self.diry) * random.randint(-1, 0)

    def run(self):
        mainloop()

root = Tk()
game = Game(root)
root.mainloop()
