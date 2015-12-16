"""
Dumb little pong game written in Python using Pygame. Pretty bad code.
It kind of works, though.
Written by Katherine Martinez and Jan Martinez (no relation) for 65-150
"""

import pygame, random
from controller import *

##WIDTH  = 1920
##HEIGHT = 1080
WIDTH = 890
HEIGHT = 500
THRESH = 5

WHITE = [255, 255, 255]
BLACK = [ 0, 0, 0]

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shitty Pong")

        self.collided = False

        ## Ball (moves at random velocity)
        self.ball_img = pygame.image.load("basketball_50.bmp")
        self.ball = self.ball_img.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.dirx = random.choice([-2, -1, 1, 2])
        self.diry = random.choice([-2, -1, 1, 2])
        self.gravity = 1

        ## Right is player, Left is computer
        self.velx = 0
        self.vely = 0
        self.left_img = pygame.image.load("left_man_100.bmp")
        self.right_img = pygame.image.load("right_man_100.bmp")
        self.left = self.left_img.get_rect(center = (THRESH, HEIGHT / 2))
        self.right = self.right_img.get_rect(center = (WIDTH - THRESH,
                                                       HEIGHT / 2))
        ## Stuff that handles the score
        self.font = 70
        self.face = pygame.font.match_font("cutecartoon")
        self.scoreC = pygame.font.Font(self.face, self.font)
        self.scoreP = pygame.font.Font(self.face, self.font)
        self.scoreC_val = 0
        self.scoreP_val = 0
        self.scoreC_img = self.scoreC.render(str(self.scoreC_val),
                                             True, WHITE)
        self.scoreP_img = self.scoreP.render(str(self.scoreP_val),
                                             True, WHITE)

        ## CONTROLLERS
        self.controllers = XboxControllers()
        if (self.controllers.count == 0):
            print "** Error: Oops! Plug in some controllers to run."
            exit()
        if (self.controllers.count == 1):
            print "** Error: Oops! you need to plug in another controller to run."
            exit()
        if (self.controllers.count > 2):
            print "** Error: Oops! You have too many controllers plugged in. Just use two!"

        self.controllerLeft = self.controllers.joysticks[0]
        self.controllerRight = self.controllers.joysticks[1]

        ## Screen changes & leaderboard stuff
        self.leaders = [] # (initials, score)
        self.state = 'start'  ## start, play, entry, scoreboard
        self.winner = 0
        self.winner_score = 0

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit()

            if (self.state == 'start'):
                self.drawStart()
            elif (self.state == 'play'):
                self.updateGame()
            elif (self.state == 'entry'):
                self.drawEntry()
            elif (self.state == 'scoreboard'):
                self.drawScoreboard()
            else:
                print " ????? how did you get here"

    def updateGame(self):
       ## Method that updates the game
        clock = pygame.time.Clock()
        startTime = clock.get_time()
        while (self.state == 'play'):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    # Quit game
                    pygame.display.quit()
                    pygame.font.quit()
                    pygame.quit()
                    return
                elif (event.type == pygame.JOYAXISMOTION):
                    # Move right player with mouse
                    self.updatePlayers()

            # play goes for a minute - can be extended?
            if (clock.get_time() - startTime >= 60000):
                # figure out who won or if there was a tie
                if self.scoreR > self.scoreL:
                    self.winner = 2
                    self.winner_score = self.scoreR
                elif self.scoreR < self.scoreL:
                    self.winner = 1
                    self.winner_score = self.scoreL
                else:
                    # tie
                    self.winner = 0
                    self.winner_score = self.scoreR

                # check if the score was good enough to get on the leaderboard
                if (self.winner > 0):
                    if self.winner_score > self.leaderboard[-1][1]:
                        self.state = 'entry'
                # otherwise just show high scores
                else:
                    self.state = 'scoreboard'
                return
                    
            ## Update the things
            self.updateBall()
            self.screen.fill([0,0,0])
            self.screen.blit(self.screen, (0,0))
            self.screen.blit(self.left_img, self.left)
            self.screen.blit(self.right_img, self.right)
            self.screen.blit(self.scoreL_img, (self.font / 2,
                                               HEIGHT - self.font))
            self.screen.blit(self.scoreR_img, (WIDTH - (self.font / 2),
                                               HEIGHT - self.font))
            self.screen.blit(self.ball_img, self.ball)
            pygame.display.flip()

    def move(self):
        (dX_a, dY_a) = (self.controllerLeft.getdX_right(), self.controllerLeft.getdY_right())
        (dX_b, dY_b) = (self.controllerRight.getDx_right(), self.controllerRight.getdY_right())
        (moveX_a, moveY_a) = (dX_a * 20, dY_a * 20)
        (moveX_b, moveY_b) = (dX_b * 20, dY_b * 20)
        self.right.move_ip(moveX_b, moveY_b)
        self.left.move_ip(moveX_a, moveY_a)        

    def updateBall(self):
        ## Moves the ball... yep, that's it
        if (self.hitPaddle()):
            pass
        elif (self.ball.left <= THRESH):
            # Right dude scores
            self.dirx = -self.dirx
            self.scoreR_val += 1
            self.scoreR_img = self.scoreR.render(str(self.scoreR_val),
                                                 True, [255,255,255])
        elif (self.ball.right >= WIDTH - THRESH):
            # Left dude scores
            self.dirx = -self.dirx
            self.scoreL_val += 1
            self.scoreL_img = self.scoreL.render(str(self.scoreL_val),
                                                 True, [255,255,255])
        elif (self.ball.top <= THRESH):
            # Bounce at top
            self.diry = abs(self.diry)
        elif (self.ball.bottom >= HEIGHT - THRESH):
            # Bounce at bottom
            self.diry = -1 * abs(self.diry)
            self.gravity = 0
        #self.diry += self.gravity ## WHY YOU NO WORK!?!?!?
        self.gravity += .1
        self.ball.move_ip(self.dirx, self.diry)


    def hitPaddle(self):
        ## Handles hits/collisions
        if (self.collided):
            self.collided = (self.ball.colliderect(self.left) or
                             self.ball.colliderect(self.right))
            return True
        if (self.ball.colliderect(self.left)):
            self.dirx = -1 * self.dirx
            self.diry = -1 * self.diry
            self.collided = True
            return True
        if (self.ball.colliderect(self.right)):
            if (self.rightx != 0): self.dirx = -1 * self.dirx
            if (self.righty != 0): self.diry = -1 * self.diry
            self.collided = True
            return True
        return False

    def reset(self):
        ## Reset the game
        return

    def handlePlayerEntry(self, players):
        print players
        if players == (1,1):
            # no need to handle player entry - shouldnt be called here anyways
            return players
        playerLeft = players[0]
        playerRight = players[1]
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_RETURN):
                    return (1,1)
            if (self.controllerLeft.getAButton()):
                return (1, playerRight)
            if (self.controllerRight.getAButton()):
                return (playerLeft, 1)
            return players

    def drawNoPlayersEntered(self):
        self.screen.fill([0,0,0])
        self.screen.blit(self.screen, (0,0))
        # draw "hey you"
        print "hey you"
        pygame.display.flip()

        pygame.time.wait(1000)
        # draw "wanna play a game"

        print "wanna play a game"
        pygame.time.wait(1000)
        # loop resets

    def drawOnePlayerEntered(self):
        self.screen.fill([0,0,0])
        self.screen.blit(self.screen, (0,0))
        # draw "grab a friend!"
        print "grab a friend"
        pygame.display.flip()

    def drawStart(self):
        # player entry
        players = (0,0)
        while (self.state == 'start'):
            players = self.handlePlayerEntry(players)
            if (players == (0,0)):
                self.drawNoPlayersEntered()
            elif (players == (0, 1) or players == (1,0)):
                self.drawOnePlayerEntered()
            else:
                self.state = 'play'

    def drawInitialEntry(self):
        # name selection ????
        # restrict editing to winner
        if (self.winner == 1):
            controller = self.controllerLeft
        if (self.winner == 2):
            controller = self.controllerRight
        if (not controller):
            print "**  Error: ya hecked it up"
            exit()

        name = 'AAA'
        cursor = 0
        while (self.state == 'entry'):
            # events - manipulating string
            if (controller.isUp()):
                ordinal = ord(name[cursor]) + 1
                if (ordinal > 90):
                    ordinal = 65
                name[cursor] = chr(ordinal)
            if (controller.isDown()):
                ordinal = ord(name[cursor]) - 1
                if (ordinal < 65):
                    ordinal = 90
                name[cursor] = chr(ordinal)
            if (controller.getAButton()):
                cursor += 1
                if cursor == 4:
                    self.leaders.append((name, self.winner_score))
                    sort(self.leaders, key=lambda x: x[1])
                    self.state = 'scoreboard'
            if (controller.getBButton()):
                if cursor != 0:
                    cursor -= 1

            # actual drawing
            self.screen.fill([0,0,0])
            self.screen.blit(self.screen, (0,0))
            message = self.face.render(name, WHITE)
            self.screen.blit(message, (500,500))
            pygame.display.flip()

    def drawLeaderBoard(self):
        # display top scores
        while (self.state == 'scoreboard'):
            title = "HIGH SCORES"
            title_obj = self.face.render(title, WHITE)
            self.screen.blit(title_obj, (500, 20))
            offset = 40
            for player in self.leaderboard:
                text = player[0] + ' ** ' + str(player[1])
                font_text = self.face.render(text, WHITE)
                self.screen.blit(font_text, (500, offset))
                offset += 20
            pygame.display.flip()

            pygame.time.wait(5000)
            self.state = 'start'

game = Game()
