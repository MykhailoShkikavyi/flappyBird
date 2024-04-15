#moduls we need for a game
import pygame
from pygame.locals import *
import random

pygame.init() # initialize pygame

clock = pygame.time.Clock()
fps = 60

screenWidth = 864
screenLength = 936

screen = pygame.display.set_mode((screenWidth, screenLength))
pygame.display.set_caption("Flappy bird")

#game variable
groundScroll = 0
scrollSpeed = 4 # speed in pixels


#loadimage
backgroundImage = pygame.image.load("bg.png") 
groundImage = pygame.image.load("ground.png")

run = True
while run:
    
    clock.tick(fps)

    screen.blit(backgroundImage, (0,0))
    #draw ground
    screen.blit(groundImage, (groundScroll,768))
    #scroll groud
    groundScroll -= scrollSpeed
    if abs(groundScroll) > 35:
        groundScroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()



pygame.quit()