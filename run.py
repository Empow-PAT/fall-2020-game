import sys
import pygame
from fall2020game.players import *


def main():
    pygame.init()

    windowwidth = 400
    windowheight = 400
    win = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption("Starter")
    black = (0, 0, 0)
    white = (255, 255, 255)

    myfont = pygame.font.SysFont('Impact', 30)  # change the 30 for a different text size


run = True
def main():
    global run
    pygame.init()

    windowwidth = 1024
    windowheight = 768
    win = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption("Starter")
    black = (0, 0, 0)
    white = (255, 255, 255)

    myfont = pygame.font.SysFont('Impact', 30)  # change the 30 for a different text size
    bot = Bot()
    player = PlayerWaving()
    time = 0
    while run:

        pygame.time.delay(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        win.fill(black)
        bot.tick(win, player)
        player.tick(time, keys, windowwidth, windowheight)
        time += 1


        #textsurface = myfont.render("Welcome to PyGame", False, white)
        #win.blit(textsurface, (0, 0))  # change the coordinates to put it in a different place

        pygame.display.update()


if __name__ == '__main__':
    main()






