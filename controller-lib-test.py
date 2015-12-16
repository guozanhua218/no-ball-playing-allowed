# A useful testing file for the controller library. Lets you push
# around a ball and that's pretty much it, but it'll tell you if the 
# joystick isn't working for any reason.

import pygame
from controller import *

##HEIGHT = 1080
WIDTH = 890
HEIGHT = 500
THRESH = 5

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [890, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
controllers = XboxControllers()

(x, y) = (250.0, 350.0)
object_img = pygame.image.load("basketball_50.bmp")
obj = object_img.get_rect(center = (x,y))

while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    for i in xrange(controllers.count):
        (dX, dY) = (controllers.joysticks[i].getdX_right(), controllers.joysticks[i].getdY_right())
        moveX = dX*20
        moveY = dY*20
        obj.move_ip(moveX, moveY)

    screen.fill([0,0,0])
    screen.blit(screen, (0,0))
    screen.blit(object_img, obj)
    if (controllers.joysticks[0].getAButton()):
        screen.fill([255,255,255])
        screen.blit(screen, (0,0))

    pygame.display.flip()

pygame.quit()

