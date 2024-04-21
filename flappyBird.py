#moduls we need for a game
import pygame
from pygame.locals import *
import random

pygame.init() # initialize pygame

clock = pygame.time.Clock()
fps = 60


# game resoloutin 
screenWidth = 764
screenLength = 836

screen = pygame.display.set_mode((screenWidth, screenLength))
pygame.display.set_caption("Flappy bird")

#define font
font = pygame.font.SysFont("Bauhaus 93", 60)

# define colour
white = (255,255,255)


#game variable
groundScroll = 0
scrollSpeed = 4 # speed in pixels
flying = False
gameOver = False
pipeGap = 150
pipeFrequency = 1200 ##In miliseconds
lastPipe = pygame.time.get_ticks() - pipeFrequency
score = 0
passPipe = False


#load game background and grass images
backgroundImage = pygame.image.load("FlappyBird/bg.png") 
groundImage = pygame.image.load("FlappyBird/ground.png")
buttonImage = pygame.image.load("FlappyBird/restart.png")


def draw_text(text, font, textColour, x, y):
    img = font.render(text, True, textColour)
    screen.blit(img, (x,y))

def resetGame():
    pipeGroup.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screenLength / 2)
    flappy.index = 2
    score = 0
    return score


class Bird(pygame.sprite.Sprite): ## a bird(main sprite) class with bird's current coordinates
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0 ## to change images to imitate animations
        self.counter = 0 ## speed of the animations
        for num in range (1, 4):
            img =  pygame.image.load(f"FlappyBird/bird{num}.png") ## a python way of format string
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() ## a rectangle, by changing recftagle we change a place of our bird sprite
        self.rect.center = (x, y)
        self.velocity = 0
        self.clicked = False ## chechking if buttom is clicked
    
    def update(self): ## handles with animations


        #gravity
        if flying == True: ## this if statement make it possible to game to start only after first click
            self.velocity += 0.5 ## bird's velocity goes up every frame by 0.5
            if self.velocity > 8:
                self.velocity = 8 ## limiting velocity to 8
            if self.rect.bottom < 668 :
                self.rect.y += int(self.velocity)

        if gameOver == False:
            ## jumpimg
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False            

            self.counter += 1
            flapCooldown = 5
            if self.counter > flapCooldown:
                self.counter = 0 ## if counter reaches more then length of the images array it resets
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0 ## if index reaches more then length of the images array it resets
                
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], -2 * self.velocity) ## by deafault this function is counterclockwise so velocity should be negetive
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) ## bird is dead so it rotates and looks into the ground(press f)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappybird/pipe.png")
        self.rect = self.image.get_rect()
        #postion 1 if pipe is on top and positio = -1 if on bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x , y - int(pipeGap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipeGap / 2)]
    def update(self):
        self.rect.x -= scrollSpeed ##making pipes move
        if self.rect.x < -100: # destroying piepes after we no longer see them
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #get mouse position
        mousePosition = pygame.mouse.get_pos()

        # check if mouse is over the buttin
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action



birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()


flappy = Bird(100, int(screenLength / 2))

birdGroup.add(flappy)

#restart button instance
button = Button(screenWidth // 2 - 50, screenLength // 2 - 100, buttonImage)

## Main game loop
run = True
while run:
    
    clock.tick(fps)

    #draw background
    screen.blit(backgroundImage, (0,0))


    birdGroup.draw(screen)
    birdGroup.update()

    pipeGroup.draw(screen)


    #draw ground
    screen.blit(groundImage, (groundScroll,668))

    ## chech the score
    if len(pipeGroup) > 0:
        if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.left\
        and birdGroup.sprites()[0].rect.right < pipeGroup.sprites()[0].rect.right\
        and passPipe == False:
            passPipe = True
        if passPipe == True:
            if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.right:
                score += 1
                passPipe = False
    draw_text(str(score), font, white, int(screenWidth / 2), 20)


    ## check if bird has hitten the ground
    if flappy.rect.bottom >= 668:
        gameOver = True
        flying = False

    # Look for colllision
    if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False) or flappy.rect.top <= 0: #If we set one of falses to true one of the groups would be deleted
        gameOver = True

    

    #scroll groud
    if gameOver == False and flying == True: ##scroll only if game is on

        #generate pipes
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > pipeFrequency:
            pipeHeight = random.randint(-100, 100)
            bottomPipe = Pipe(screenWidth,  int(screenLength / 2) + pipeHeight, -1)
            topPipe = Pipe(screenWidth, int(screenLength / 2) + pipeHeight, 1)
            pipeGroup.add(bottomPipe)
            pipeGroup.add(topPipe)
            lastPipe = timeNow

        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35: #ground image has 34 frames, so after reaching those frames image goes back to the original coordinates, so it looks like it is infinite
            groundScroll = 0

        pipeGroup.update()

    # check for gameover and reset
    if gameOver == True:
        if button.draw() == True:
            gameOver = False
            score = resetGame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True

    pygame.display.update()




pygame.quit()