__all__ = ["Bot", "draw_text_sat", "Enemy_proj", "enemyProjs"]

import pygame
pygame.mixer.init()
from fall2020game.players import *
import random
import math
from fall2020game.Images import sprites
import sys

white = (255, 255, 255)
black = (0,0,0)
yellow = (255, 255, 0)
red = (255,0,0)
green =  (0,255,0)
lightblue = (0,188,255)
gold = (255,215,0)
font_name = pygame.font.match_font('arial')
bot = sprites["Enemy Ship.png"]
bot = pygame.transform.scale(bot, (30,30))

from os import path
here = path.dirname(path.abspath(__file__))
Damage = pygame.mixer.Sound(path.join(here,"../Sounds/Damage.wav"))

def damage():
    pygame.mixer.Sound.play(Damage)
    pygame.mixer.music.stop()

def draw_text_sat(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, (x,y))


class Bot:
    def __init__(self):
        self.height = 30.0
        self.width = 30.0
        self.x = 0
        self.y = 0
        #gravity, friction, slope, upwards velocity, x velocity
        self.velx = 0
        self.vely = 0
        self.max_hp = 500
        self.hp = 500
        self.nickName = "Nickname"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 2
        self.timer = 0
        self.StaggerTimer = 0
        self.damage = 10


    def tick(self, win, player, BotPlay):
        #Hp Drawing
        #draw_text_sat(win, str(self.hp), 18 ,self.x-3, self.y-32)
        pygame.draw.rect(win, red, (self.x - 13, self.y - 20, 50, 10))
        pygame.draw.rect(win, green, (self.x - 13, self.y - 20, self.hp / 10, 10))

        win.blit(bot, self.rect)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(bot, self.rect)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for bot1 in BotPlay:
            if bot1.rect.colliderect(self.rect) and bot1.rect != self.rect:
                self.x +=  random.randint(0, 10)
                self.y += random.randint(0, 10)
        #Jittery movement
        #self.vely = player.vely + random.randint(-10, 10)
        #self.velx = player.velx + random.randint(-10, 10)

        #Works but is a little weird when on top of player
        if self.x > player.x:
            self.velx = -self.speed+1
        else:
            self.velx = self.speed-1

        if self.y < player.y:
            self.vely = self.speed - 1
        else:
            self.vely = -self.speed + 1
        self.y += self.vely
        self.x += self.velx
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.timer >= 5:
            projectilEn = Enemy_proj(player,self,self.x, self.y)
            enemyProjs.append(projectilEn)
            self.timer = 0

        self.timer += 1
        self.StaggerTimer +=1

enemyProjs = []

class Enemy_proj:
    def __init__(self,annihilator, bot, x, y):
        self.x = x + 16.5
        self.y = y + 17
        self.height = 10.0
        self.width = 10.0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # friction, slope, upwards velocity, x velocity
        self.velMultiply = 1.5
        self.damage = bot.damage

        if self.x > annihilator.x:
            self.velx = -8
        else:
            self.velx = 8

        if self.y < annihilator.y:
            self.vely = 8
        else:
            self.vely = -8


        if abs(self.x-annihilator.x) > abs(self.y-annihilator.y):
            if self.x - annihilator.x>0:
                self.velx=-3
                self.vely=0
            else:
                self.velx = 3
                self.vely = 0
        else:
            if self.y - annihilator.y>0:
                self.vely=-3
                self.velx=0
            else:
                self.vely = 3
                self.velx = 0

    def tick(self, win, annihilator, sheild, projectiles, windowwidth, windowheight):
        if self.rect.colliderect(annihilator.rect) and annihilator.hp > 0:
            annihilator.hp -= self.damage
            damage()
            enemyProjs.remove(self)
            newsurface = pygame.Surface ((windowwidth, windowheight), pygame.SRCALPHA )
            newsurface.fill ( (255, 0, 0, 55))
            win.blit (newsurface, (0, 0))
        elif self.rect.colliderect(sheild.rect) and sheild.hp > 0:
            sheild.hp -= self.damage
            damage()
            enemyProjs.remove(self)
            sheild.nonHitTime=0
        else:
            for i in projectiles:
                if self.rect.colliderect (i.rect):
                    enemyProjs.remove(self)
                    projectiles.remove(i)
                    break
        self.y += self.vely
        self.x += self.velx
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(win, lightblue, self.rect)




