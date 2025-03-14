# Written by Tom Maltby, (c)Tom Maltby 2025, credits follow
# www.maltby.org
# 
# Currently 3276 lines
# Original game: 1521 lines, 1 weekend of coding + 6 hrs resource housekeeping & trim
# 
# Originally based off Jon Fincher's 120 line tutorial py_tut_with_images.py
# py_tut_with_images on github: https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py
# Jon's blog: https://realpython.com/pygame-a-primer/
#
# Additional sounds from  http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
# # Arcade font from https://www.dafont.com/arcade-ya.font , by Yuji Adachi, listed as 100% free
#
# Barring 2 hours last summer, this is my first Python coding, and my first significant coding in any language
# in the last 15 years.  I'm sure it could be more elegant, but I'm having fun.
#
# Thanks to Jon Fincher, and the creators of the great sounds and music
# Graphics except jet, missile, and white cloud are by me, using Corel and Gimp
#
# Joystick handling imported under MIT license:
#  Copyright (c) 2017 Jon Cooper
#
#  pygame-xbox360controller.
#  Documentation, related files, and licensing can be found at
#
#      <https://github.com/joncoop/pygame-xbox360controller>.
#  Thanks to Jon Cooper, simpler than reinventing the wheel
 

# Import the pygame module
# Import random for random numbers
# Import os for file handling
# Import tkinter for root graphic context
# Import math for reasons
# Import glob for image preload
# Import controller driver

import random
import pygame
import tkinter
import os
import os.path
import math
import glob
import xbox360_controller




# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    K_ESCAPE, #Quit
    K_DOWN,   #Steering
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_SPACE,  #MG
    K_x,  #Flamer
    K_c,  #shock shield
    K_v,  #pulsar
    K_b,  #bio blaster
    K_RETURN,  #Start game
    K_q,
    K_p,  #pause
    K_F1, #help
    KEYDOWN,
    QUIT,
    RLEACCEL,
    K_F5,
)



# Define Colors
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")

# Define constants for the screen width and height
root = tkinter.Tk()
SCREEN_WIDTH = root.winfo_screenwidth() - 50
SCREEN_HEIGHT = root.winfo_screenheight() - 100
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100

# Define the Sun and Moon object
class SunMoon(pygame.sprite.Sprite):
    def __init__(self, wavenum):
        super(SunMoon, self).__init__()
        # Start with Sun loaded
        self.surf = get_image("sun1.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        # Place randomly
        self.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)

    def update(self, wavenum):

        if wavenum < 3:
            # Keep sun until wave 3
            self.surf = get_image("sun1.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if wavenum > 2 and wavenum < 4:
            # Then replace it with moon
            self.surf = get_image("moon1.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, firebullet):
        super(Player, self).__init__()
        self.surf = get_image("jet.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        # Start jet in middle of left edge
        self.rect.top = SCREEN_HEIGHT_NOBOX / 2
        self.rect.left = 30
        self.firebullet = 0
        self.hp = 100
        self.armor = 50

    # Move the sprite based on joystick
    #def updatestk(self, )
 
    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if redflash == False and greenflash == False:
            
            # handle joysticks
            left_x, left_y = controller.get_left_stick()
             # player move   
            self.rect.move_ip(int(left_x * 5), 0)
            self.rect.move_ip(0, int(left_y * 5))
            triggers = controller.get_triggers()
            buttons = controller.get_buttons()
            if triggers > 0.3:
                self.firebullet = 3
            if buttons[0] == 1:
                self.firebullet = 4
            if buttons[2] == 1:
                self.firebullet = 5
            if buttons[1] == 1:
                self.firebullet = 6
            if buttons[3] == 1:
                self.firebullet = 7
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
                move_down_sound.play()
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
            if pressed_keys[K_SPACE]:
                #machine gun
                #shoot_sound.play()
                self.firebullet = 3
            if pressed_keys[K_x]:
                #flamer
                self.firebullet = 4
            if pressed_keys[K_c]:
                #lightning shield
                self.firebullet = 5
            if pressed_keys[K_b]:
                #bioweapon
                self.firebullet = 6
            if pressed_keys[K_v]:
                #pulse
                self.firebullet = 7
            # Keep player on the screen if not on flash       
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT_NOBOX:
                self.rect.bottom = SCREEN_HEIGHT_NOBOX
        return(self)                

# Define the mountain object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        super(Mountain, self).__init__()
        if wave < 3:
            self.mountnum = str(random.randint(1,2))
        elif wave < 5:
            self.mountnum = str(random.randint(1,4))
        else:
            self.mountnum = str(random.randint(1,6))
        self.surf = get_image("mountain" + self.mountnum + ".png")
        
        self.name = "mountain" + "mountain" + self.mountnum + ".png"
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # Starts on the bottom, off the screen to the right
        self.rect = self.surf.get_rect(bottomleft=(SCREEN_WIDTH + 30, SCREEN_HEIGHT_NOBOX),)
        if (random.randint(1,100) + (wave * wave)) > 90: 
                # Spawn gun on rock, more likely in later waves
                new_enemy = Enemy(7,14,1,self)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # Move the mountain based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        # if off left edge, kill
        if self.rect.right < 0:
            self.kill()


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):

    def __init__(self, etype, boomcounter, hp, launcher):
        super(Enemy, self).__init__()
        self.name = "enemy" + enemydict[etype]["imgname"]
        self.surf = get_image(enemydict[etype]["imgname"])
        self.surf.set_colorkey(enemydict[etype]["mask"], RLEACCEL) 
        # Random speed, climb/dive               
        if enemydict[etype]["randspeed"]:
            self.speed = random.randint(*enemydict[etype]["speed"])
        else:
            self.speed = enemydict[etype]["speed"]
        if enemydict[etype]["randcenter"]:
            self.rect = self.surf.get_rect(center = (random.randint(*enemydict[etype]["centerwidth"]), random.randint(*enemydict[etype]["centerheight"])))
        else:
            if enemydict[etype]["islauncher"]:
                randadd = 0
                # Let boss shoot at multiple levels
                if hasattr(launcher, "etype"):
                    if enemydict[launcher.etype]["boss"] == 1:
                        randadd = random.randint(-100,100)
                        self.rect = self.surf.get_rect(center=(launcher.rect.left + enemydict[etype]["centerwidth"], launcher.rect.top + randadd + enemydict[etype]["centerheight"]))
                    else:
                        self.rect = self.surf.get_rect(center=(launcher.rect.left + enemydict[etype]["centerwidth"], launcher.rect.top + enemydict[etype]["centerheight"]))    
                else:
                    self.rect = self.surf.get_rect(center=(launcher.rect.left + enemydict[etype]["centerwidth"], launcher.rect.top + enemydict[etype]["centerheight"]))
            else:
                self.rect = self.surf.get_rect(center = (enemydict[etype]["centerwidth"], enemydict[etype]["centerheight"]))               
        if enemydict[etype]["randclimb"]:
            if enemydict[etype]["ishoming"]:
                climbmod = random.randint(*enemydict[etype]["climb"])
                if self.rect.top > player.rect.top:
                    self.climb = - climbmod
                else:
                    self.climb = climbmod
            else:
                self.climb = random.randint(*enemydict[etype]["climb"])
        else:
            self.climb = enemydict[etype]["climb"]
        if enemydict[etype]["isanimated"]:
            self.ticks = enemydict[etype]["ticks"]
        self.fired = enemydict[etype]["fired"]
        self.hp = enemydict[etype]["hp"]

        
        self.etype = etype
        # set blowup time to enemy as passed
        self.boomcounter = boomcounter

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        if random.randint(1,10)>5:
            # 50% modify climb if applicable
            if enemydict[self.etype]["randclimb"]:
                # get mod/turn as tuple of random parameters
                climbmod = random.randint(*enemydict[self.etype]["climb"])
                if enemydict[self.etype]["ishoming"]:
                    if self.rect.top > player.rect.top:
                        self.climb = self.climb - climbmod
                    else:
                        self.climb = self.climb + climbmod 
                else:
                    self.climb = self.climb + climbmod
                if enemydict[self.etype]["climbmin"] > self.climb:
                    self.climb = enemydict[self.etype]["climbmin"] 
                if enemydict[self.etype]["climbmax"] < self.climb:
                    self.climb = enemydict[self.etype]["climbmax"]
        if enemydict[self.etype]["isanimated"]:
            # animate through dictionary checks
            framecheck = 0
            gotframe = False
            self.ticks = self.ticks -1
            if self.ticks < 1:
                self.ticks = self.ticks = enemydict[self.etype]["ticks"]
            while gotframe == False:
                if self.ticks > enemydict[self.etype]["aniframetimers"][framecheck]:
                    self.surf = get_image(enemydict[self.etype]["aniframes"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            if self.ticks < 0:
                self.ticks = self.ticks = enemydict[self.etype]["ticks"]
            self.surf.set_colorkey(enemydict[self.etype]["mask"], RLEACCEL)

        # Move the enemy
        if enemydict[self.etype]["advancedmovement"] == True:
            isdone = amove(self)   
        if hasattr(self, "rect"):
            if hasattr(self.rect, "move_ip"):
                self.rect.move_ip(-self.speed, self.climb)
                # Kill it if offscreen
                if self.rect.right < 0:
                    self.kill()
                if self.rect.left > SCREEN_WIDTH + 100:
                    self.kill()
                # Make top & bottom permeable to powerups; other enemies must stay in screen
                if self.rect.bottom > SCREEN_HEIGHT_NOBOX:
                    # ENEMY GROUND COLLISIONS
                    if enemydict[self.etype]["ispowerup"] == False:
                        if enemydict[self.etype]["isground"] == False: # Missile Launcher should be on ground
                            # Otherwise Don't leave
                            self.rect.bottom = SCREEN_HEIGHT_NOBOX - 50
                            # Bounce
                            self.climb = self.climb * - 1 # * self.climb
                        if enemydict[self.etype]["damground"] > 0:
                            self.hp = self.hp - int(100 * (enemydict[self.etype]["damground"]/100))
                            if self.hp < 0:
                                # Explode missiles, blimps
                                if enemydict[self.etype]["isexplodable"]:
                                    self.etype = enemydict[self.etype]["isexplodable"]
                                else:
                                    if enemydict[self.etype]["isexploded"] == False:
                                        self.kill()
                if self.rect.top < 0:
                    if enemydict[self.etype]["ispowerup"] == False:
                        # Don't leave
                        self.top = 5
                        # Bounce
                        self.climb = 3
                    elif self.rect.bottom < 0: # But don't let them disappear up without cleanup
                        self.kill()
        if enemydict[self.etype]["isshooter"] == True:   
            # Functional blimp or missile launcher or cannon, potentialy etc
            if redflash == False:
                if random.randint(1,100) + wave * 2 > 90 and self.fired == 0:
                    # Shoot designated ammotype
                    new_enemy = Enemy(enemydict[self.etype]["ammotype"],14,1,self)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                    self.fired = enemydict[self.etype]["fired"]
                elif self.fired > 0:
                    self.fired = self.fired - 1
        if enemydict[self.etype]["isexploded"]:          
            self.hp = 1
            # Exploding animation            
            self.boomcounter = self.boomcounter - 1
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()
            framecheck = 0
            gotframe = False
            while gotframe == False and self.boomcounter > 0:
                if self.boomcounter > enemydict[self.etype]["expframetimers"][framecheck]:
                    self.surf = get_image(enemydict[self.etype]["expframes"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            self.surf.set_colorkey(enemydict[self.etype]["mask"], RLEACCEL)
        
        if enemydict[self.etype]["skyburst"]:  #self.etype == 81: # Cannon shell
            # Don't let off screen
            if self.rect.right < 0:
                self.kill
            if random.randint(1,10) == 10:
                # Slow climb gradually but randomly
                self.climb = self.climb + 1
            if self.rect.bottom > SCREEN_HEIGHT_NOBOX or self.rect.top < 0:
                # Kill at top/bottom
                self.kill
            if self.climb > -1:
                # Detonate at peak of arc
                if enemydict[self.etype]["isexplodable"]:
                    self.etype = enemydict[self.etype]["isexplodable"]
                    self.boomcounter = 7 # Abbreviated explosion
                else:
                    self.kill()
        if enemydict[self.etype]["isground"] == True:
            self.rect.bottom = SCREEN_HEIGHT_NOBOX

# Define the bullet object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self,startx,starty,btype,boomcounter):
        super(Bullet, self).__init__()
        self.btype = btype
        self.surf = get_image(bulletdict[self.btype]["imgname"])
        self.name = "bullet" + bulletdict[self.btype]["imgname"]
        self.speed = bulletdict[self.btype]["bspeed"]
        bulletdict[self.btype]["sound"].play()
        self.boomcounter = boomcounter
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # The starting position is the nose of the plane
        self.rect = self.surf.get_rect(
            center=(
                startx,
                starty
            )
        )
        
    # Move the bullet based on speed
    # Remove it when it passes the right edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if bulletdict[self.btype]["isanimated"]:
            self.boomcounter = self.boomcounter - 1
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()
            framecheck = 0
            gotframe = False
            while gotframe == False and self.boomcounter > 0:
                if self.boomcounter > bulletdict[self.btype]["frametimers"][framecheck]:
                    self.surf = get_image(bulletdict[self.btype]["frames"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # Shock Lances from active shock shield
            if bulletdict[self.btype]["shield"] == True:
                self.rect.centerx = player.rect.centerx + random.randint(-3, 3)
                self.rect.centery = player.rect.centery + random.randint(-3, 3)
                # This is a Shock Lance spawner to increase the effect and wow-factor of the shock shield
                pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
                if enemies:
                    # If there aren't already bushels of Shock Lances flying around
                    if len(bullets) < 100:
                        closeenemies = []
                        for e, enem in enumerate(enemies):
                            chkdist = pos.distance_to(pygame.math.Vector2(enem.rect.centerx, enem.rect.centery))
                            if chkdist < 300:
                                # Gather a list of enemies within 300 of player
                                closeenemies.append(enem)
                        # If there are enemies closer than 300
                        if len(closeenemies) > 0:
                            # Throw shock bolts from the shock shield at nearby enemies
                            for e in closeenemies:
                                edist = pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery))
                                if edist < 300:
                                    new_bullet = Bullet(player.rect.centery,player.rect.centerx,6,3)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    yoffset = e.rect.centery - player.rect.centery
                                    xoffset = e.rect.centerx - player.rect.centerx
                                    rotation = math.degrees(math.atan2(yoffset, xoffset))
                                    scalesurf = pygame.transform.scale(new_bullet.surf, (new_bullet.rect.height, edist))
                                    finsurf = pygame.transform.rotate(scalesurf, rotation)
                                    new_bullet.surf = finsurf
                                    new_bullet.rect = new_bullet.surf.get_rect()
                                    if e.rect.centery < player.rect.centery:
                                        new_bullet.rect.bottomleft = player.rect.center
                                    else:
                                        new_bullet.rect.topleft = player.rect.center

            if self.btype == 6:
                # Shock Lance
                self.rect.centerx = player.rect.centerx + random.randint(-3, 3)
                self.rect.centery = player.rect.centery + random.randint(-3, 3)
                pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
                if enemies:
                    closestenemy = min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery)))
                    edist = pos.distance_to(pygame.math.Vector2(closestenemy.rect.centerx, closestenemy.rect.centery))
                    if edist < 300:
                        yoffset = closestenemy.rect.centery - player.rect.centery
                        xoffset = closestenemy.rect.centerx - player.rect.centerx
                        # This extra rotation / scale started as an error, but is just the spectacular touch we needed
                        # The scaling of an already rotated sprite causes spectacular and chaotic 'jumping the gap'
                        rotation = math.degrees(math.atan2(yoffset, xoffset))
                        scalesurf = pygame.transform.scale(self.surf, (self.rect.height, edist))
                        finsurf = pygame.transform.rotate(scalesurf, rotation)
                        self.surf = finsurf
                        self.surf.set_colorkey(WHITE, RLEACCEL)
                        self.rect = self.surf.get_rect()
                        self.rect.center = closestenemy.rect.center
                        
                
        if self:
            center = self.rect.center
            self.rect = self.surf.get_rect()
            self.rect.center = center   

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        if wave < 3:
            # During the day, use light clouds
            self.surf = get_image("cloud.png")
        else:
            # At night, use dark clouds
            self.surf = get_image("cloud2.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT_NOBOX - 200),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        # if off left edge, kill
        if self.rect.right < 0:
            self.kill()   

# Advanced movement function(s)

def amove(thise):
    # For the first case, assume a desire to stay in the vertical center, 150 pixels from the back edge of the screen
    # Initialize locals
    movex = 0
    movey = 0
    # Set base coordinates
    basey = SCREEN_HEIGHT_NOBOX / 2 - thise.rect.height / 2
    basex = SCREEN_WIDTH - 250
    # establish proposed move
    movey = thise.climb + thise.rect.bottom
    if thise.speed > 5:
        movex = thise.speed + thise.rect.left
    else:
        movex = thise.speed + thise.rect.right
    # Adjust towards base on probablility of distance per axis
    if movex > basex:
        percreturn = movex - basex
        if random.randint(1,100) < percreturn:
            thise.speed = thise.speed + 3
    if movex < basex:
        percreturn = (basex - movex) // 5        
        if random.randint(1,100) < percreturn:
            thise.speed = thise.speed - 3
    
    # Update proposed x position
    if thise.speed > 5:
        movex = thise.speed + thise.rect.left
    else:
        movex = thise.speed + thise.rect.right
    if movey > basey:
        percreturn = (movey - basey) // 2
        if random.randint(1,100) < percreturn:
            thise.climb = thise.climb - 3
    if movey < basey:
        percreturn = basey - movey        
        if random.randint(1,100) < percreturn:
            thise.speed = thise.speed + 3
    # Update proposed y position
    movey = thise.climb + thise.rect.bottom
    # Now check that we aren't running into a mountain or the ground
    if movey > SCREEN_HEIGHT_NOBOX:
        movey = SCREEN_HEIGHT_NOBOX - 50
    if len(mountains) > 0:
        for m in mountains:
            if m.rect.collidepoint(movey,movex):
                thise.climb = -5
                thise.speed = 5
    # Don't leave the screen
    if thise.rect.right > SCREEN_WIDTH:
        thise.rect.right = SCREEN_WIDTH - 30
        thise.speed = 6
    if thise.rect.left < 0:
        thise.rect.left = 30
        thise.speed = -6
    if thise.rect.top < 0:
        thise.rect.top = 30
        thise.climb = -3
    if thise.rect.bottom > SCREEN_HEIGHT_NOBOX:
        thise.rect.bottom = SCREEN_HEIGHT_NOBOX - 50
        thise.climb = + 3
    if thise.speed > 15:
        thise.speed = 15
    if thise.speed < -15:
        thise.speed = -15
    if thise.climb > 8:
        thise.climb = 8
    if thise.climb < -8:
        thise.climb = -8
    return(thise)
    


# Define and cache fonts

pygame.font.init()
font15 = pygame.font.Font("fonts/ARCADE_R.ttf", 15)
font16 = pygame.font.Font("fonts/ARCADE_R.ttf", 16)
font20 = pygame.font.Font("fonts/ARCADE_R.ttf", 20)
font30 = pygame.font.Font("fonts/ARCADE_R.ttf", 30)
font50 = pygame.font.Font("fonts/ARCADE_R.ttf", 50)
font60 = pygame.font.Font("fonts/ARCADE_R.ttf", 60)
font75 = pygame.font.Font("fonts/ARCADE_R.ttf", 75)

# Cache repeated text renders
playagametextblack = font30.render("Press Enter To Play - Press Esc to Quit", 1, BLACK)
playagametextred = font30.render("Press Enter To Play - Press Esc to Quit", 1, RED)
pausetext1 = font20.render("Controls:", 1, BLACK)
pausetext2 = font16.render("Flying: Arrow keys - Up, Down, Left, Right", 1, BLACK)
pausetext3 = font16.render("Weapons: Space - Machine Gun, X - Flamer, C - Shock Shield, V - Pulsar, B - Bio Blast", 1, BLACK)
pausetext4 = font16.render("Enter - Play / Pause / Unpause, Escape - Quit ", 1, BLACK)
pausetext5 = font20.render("Press Enter To UnPause - Press Esc to Quit", 1, BLACK)
pausetext1red = font20.render("Controls:", 1, RED)
pausetext2red = font16.render("Flying: Arrow keys - Up, Down, Left, Right", 1, RED)
pausetext3red = font16.render("Weapons: Space - Machine Gun, X - Flamer, C - Shock Shield, V - Pulsar, B - Bio Blast", 1, RED)
pausetext4red = font16.render("Enter - Play / Pause / Unpause, Escape - Quit ", 1, RED)
pausetext5red = font20.render("Press Enter To UnPause - Press Esc to Quit", 1, RED)

def texts(lives, score):
    # gives lives, score, waves, high score
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,0))
    screen.blit(scoretext, (32, SCREEN_HEIGHT - 22))
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,255))
    screen.blit(scoretext, (30, SCREEN_HEIGHT - 20))

def texts2(flamer, shock, bio, pulse):
    # gives ammo - machinegun has infinite ammo
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): " + str(shock)  + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,0))
    screen.blit(scoretext, (32, SCREEN_HEIGHT - 42))
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): "+str(shock) + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,255))
    screen.blit(scoretext, (30, SCREEN_HEIGHT - 40))

def texts3(highscore):
    # on enter to play screen, gives high score
    
    ptxtoffset = playagametextblack.width / 2
    screen.blit(playagametextblack, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 60))
    screen.blit(playagametextred, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 58))
    playagametext = font60.render("High Score: "+str(highscore), 1, (0,0,0))
    ptxtoffset = playagametext.width / 2
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 100))
    playagametext = font60.render("High Score: "+str(highscore), 1, (255,0,0))
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 102))
    #Control list
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2))
    screen.blit(pausetext1red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 2))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 20))
    screen.blit(pausetext2red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 22))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 40))
    screen.blit(pausetext3red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 42))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 60))
    screen.blit(pausetext4red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 62))

def texts4():
    #Pause screen    
    ptxtoffset = pausetext5.width / 2
    screen.blit(pausetext5, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 30))
    screen.blit(pausetext5red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 28))
    #Control list
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2))
    screen.blit(pausetext1red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 2))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 20))
    screen.blit(pausetext2red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 22))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 40))
    screen.blit(pausetext3red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 42))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 60))
    screen.blit(pausetext4red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 62))

healthhardmax = 400
armorhardmax = 200
healthmax = 200
armormax = 100
bossmode = False
wasbossmode = bossmode
bosshealthblink = 0

def healthbar(left, top, health):
    healthbarborder = pygame.Rect(left + 40, top, healthmax, 30)
    healthbarfilled = pygame.Rect(left + 42, top + 2, int((healthmax - 4) * (health/(healthmax/2))), 26)
    heartimg = get_image("heart.png")
    heartimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(heartimg, (left,top))

    if health > 70:
        healthbarcolor = GREEN
    elif health > 30:
        healthbarcolor = YELLOW
    else:
        healthbarcolor = RED
    pygame.draw.rect(screen, BLACK, healthbarborder, 0, 2)
    pygame.draw.rect(screen, healthbarcolor, healthbarfilled, 0, 2)
    return health

def bosshealthbar(left, top, boss, health, bosshealthblink):
 
    bhealthmax = enemydict[boss.etype]["hp"] / 2 * wave
    barsizefactor = bhealthmax / 1000
    healthbarblink = pygame.Rect(left + 35, top-5, int(200 * barsizefactor) + 10, 40)
    healthbarborder = pygame.Rect(left + 40, top, int(200 * barsizefactor), 30)
    healthbarfilled = pygame.Rect(left + 42, top + 2, int((196) * (health/(bhealthmax)) * barsizefactor), 26)

    if int((196) * (health/(bhealthmax))) > 70 * wave / 2:
        healthbarcolor = GREEN
    elif int((196) * (health/(bhealthmax))) > 30 * wave / 2:
        healthbarcolor = YELLOW
    else:
        healthbarcolor = RED

    if bosshealthblink < 10:
        pygame.draw.rect(screen, YELLOW, healthbarblink, 0, 2)
    else:
        pygame.draw.rect(screen, RED, healthbarblink, 0, 2)
    pygame.draw.rect(screen, BLACK, healthbarborder, 0, 2)
    pygame.draw.rect(screen, healthbarcolor, healthbarfilled, 0, 2)
    if bosshealthblink > 20:
        bosshealthblink = 0
    return boss
    

def armorbar(left, top, armor):
    armorbarborder = pygame.Rect(left + 40, top, armormax, 30)
    armorbarfilled = pygame.Rect(left + 42, top +2, int((armormax - 4) * (armor/(armormax/2))), 26)
    shieldimg = get_image("shield.png")
    shieldimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(shieldimg, (left, top))
    pygame.draw.rect(screen, BLACK, armorbarborder, 0, 2)
    pygame.draw.rect(screen, BLUE, armorbarfilled, 0, 2)
    return armor

def fpscounter():    
    fps = str(int(clock.get_fps()))
    fps_t = font20.render("FPS:" + fps, 1, RED)
    screen.blit(fps_t,(10,10))  

def statusdisplay():
    statusbox = pygame.Rect(3, SCREEN_HEIGHT - 94, SCREEN_WIDTH - 3, 94)
    statusboxframe = pygame.Rect(0,SCREEN_HEIGHT - 100,SCREEN_WIDTH,100)
    pygame.draw.rect(screen, BLUE, statusboxframe, 0, 3)
    pygame.draw.rect(screen, GRAY, statusbox, 0, 3)   
    # Draw our game text
    texts(plives, score)
    texts2(flamer,shock,bio,pulse)   
    healthbar(10, SCREEN_HEIGHT - 80, player.hp)
    armorbar((healthmax + 50), SCREEN_HEIGHT - 80, player.armor)
# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# make a controller
controller = xbox360_controller.Controller()

# Create the screen object
# First set the icon
icon = pygame.image.load("Graphics/""icon.png")
icon.set_colorkey(BLACK, RLEACCEL)
pygame.display.set_icon(icon)
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Assault Shark')

# Preload graphics
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("Graphics/" + key).convert()
    return image_cache[key]

image_cache = {}
# Gets a list of all images in the graphics directory
images = glob.glob ("Graphics/*.png")
# Loads all images into the image_cache dictionary
for image in images:
    img_name = os.path.basename(image)
    get_image(img_name)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
# Many new additional sounds sourced from: http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
shoot_sound = pygame.mixer.Sound("sounds/Shoot.ogg")
collision_sound = pygame.mixer.Sound("sounds/Small_explosion.ogg")
bio_sound = pygame.mixer.Sound("sounds/Bio_splat.ogg")
shock_sound = pygame.mixer.Sound("sounds/Shock_sound2.ogg")
flamer_sound = pygame.mixer.Sound("sounds/Flamer_sound.ogg")
powerup_sound = pygame.mixer.Sound("sounds/Power_up.ogg")
wavechange_sound = pygame.mixer.Sound("sounds/Wave_change.ogg")
pulse_sound = pygame.mixer.Sound("sounds/Pulse_sound.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)
shoot_sound.set_volume(0.5)
bio_sound.set_volume(0.5)
shock_sound.set_volume(0.5)
flamer_sound.set_volume(0.5)
powerup_sound.set_volume(0.5)
wavechange_sound.set_volume(0.5)
pulse_sound.set_volume(0.5)

# Fill a nested dictionary of bullets by btype
bulletdict = {
    1: {
        "imgname": "bullet.png",
        "bspeed": 25,
        "sound": shoot_sound,
        "isanimated": False,
        "numframes": 1,
        "frames": ("bullet.png",),
        "frametimers": (0,)
    },
    2: {
        "imgname": "blast1.png",
        "shield": False,
        "bspeed": 20,
        "sound": flamer_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("blast1.png","blast2.png","blast3.png","blast4.png","blast5.png"),
        "frametimers": (22,16,10,5,0)
    },
    3: {
        "imgname": "shock1.png",
        "shield": True,
        "bspeed": 0,
        "sound": shock_sound,
        "isanimated": True,
        "numframes": 4,
        "frames": ("shock1.png","shock2.png","shock3.png","shock4.png"),
        "frametimers": (12,8,4,0)
    },
    4: {
        "imgname": "bio1.png",
        "shield": False,
        "bspeed": 30,
        "sound": bio_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("bio1.png","bio2.png","bio3.png","bio4.png","bio5.png"),
        "frametimers": (22,16,10,5,0)
    },
    5: {
        "imgname": "pulse1.png",
        "shield": False,
        "bspeed": 15,
        "sound": pulse_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("pulse1.png","pulse2.png","pulse3.png","pulse4.png","pulse5.png"),
        "frametimers": (22,18,12,5,0)
    },
    6: {
        "imgname": "shockbolt.png",
        "shield": False,
        "bspeed": 0,
        "sound": shock_sound,
        "isanimated": True,
        "numframes": 2,
        "frames": ("shockbolt2.png", "shockbolt.png"),
        "frametimers": (2,0)
    }
}    

# Fill a nested dictionary of enemies by etype
enemydict = {
    1: {
        # Missile, unguided
        "imgname": "missile1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (5,20),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (-1,1),
        # Limits for climb/dive
        "climbmax": 8,
        "climbmin": -8,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (SCREEN_WIDTH, SCREEN_WIDTH + 20),
        "centerheight": (0,SCREEN_HEIGHT_NOBOX),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 10,
        # Number of animation frames
        "numaniframes": 2,
        # Timing for animation frames
        "aniframetimers": (5,0),    
        # Animation frame names   
        "aniframes": ("missile1.png","missile2.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 62,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage to player if collided
        "damage": (10,20),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    2: {
        # Homing Snek
        "imgname": "snek1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 15, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": (0,1),
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -30,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 10,
        # Number of animation frames
        "numaniframes": 2,
        # Timing for animation frames
        "aniframetimers": (5,0),    
        # Animation frame names   
        "aniframes": ("snek1.png","snek2.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 62,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (15,30),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    3: {
        # Homing Missile
        "imgname": "missile21.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 16, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 9,
        "climbmin": -9,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -20,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 8,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": (5,3,0),    
        # Animation frame names   
        "aniframes": ("missile21.png","missile22.png","missile23.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 62,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (15,30),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    4: {
        # Blue blimp, unarmored
        "imgname": "ship4.png",
        "mask": BLACK, # Blimps are leftover from the VB They Comin, and have black for a mask color
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (5,10),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (-1,1),
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": 2,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (SCREEN_WIDTH, SCREEN_WIDTH + 20),
        "centerheight": (0,SCREEN_HEIGHT_NOBOX),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,             
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 61,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 20,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 4,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (30,45),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    5: {
        # Red blimp, armored
        "imgname": "ship4a.png",
        "mask": BLACK, # Blimps are leftover from the VB They Comin, and have black for a mask color
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (5,10),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (-1,1),
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": 6,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (SCREEN_WIDTH, SCREEN_WIDTH + 20),
        "centerheight": (0,SCREEN_HEIGHT_NOBOX),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 61,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 20,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 5,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (40,60),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    6: {
        # Homing Fish
        "imgname": "fish1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 20, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": -4,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -38,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 2,
        # Timing for animation frames
        "aniframetimers": (6,0),    
        # Animation frame names   
        "aniframes": ("fish1.png","fish2.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 62,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (20,35),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    7: {
        # Cannon
        "imgname": "gun1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": 81,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": +60,
        "centerheight": -20,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,         
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 64,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 25,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 2,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (25,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    8: {
        # Missile Launcher
        "imgname": "gun2.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": 3,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": SCREEN_WIDTH + 30,
        "centerheight": SCREEN_HEIGHT_NOBOX -33,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 63,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 35,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 2,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (25,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    41: {
        # Cuttleboss 1
        "imgname": "shell3.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": True,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": (1,3),
        # Limits for climb/dive
        "climbmax": 5,
        "climbmin": -5,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": 6,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": SCREEN_WIDTH + 30,
        "centerheight": SCREEN_HEIGHT_NOBOX / 2,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": (8,4,0),    
        # Animation frame names   
        "aniframes": ("shell3.png","shell3b.png", "shell3c.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 65,
        # Missiles and shells have one hp; blimps and guns have more, bosses have many
        "hp": 1000,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (100,200),
        # is boss?
        "boss": 1,
        # boomcounter for explosion timing
        "boomcounter": 35,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 0
    },
    61: {
        # Exploded blimp
        "imgname": "ship4xp1.png",
        "mask": BLACK,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": (8,5,0),
        # expframes is a tuple of explosion frames
        "expframes": ("ship4xp1.png","ship4xp2.png","ship4xp3.png"),
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (15,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    62: {
        # Exploded missile or cannon shell
        "imgname": "boom1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": (8,5,0),
        # expframes is a tuple of explosion frames
        "expframes": ("boom.png","boom2.png","boom3.png"),
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (5,10),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    63: {
        # Exploded Missile Launcher
        "imgname": "gun2xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": (8,5,0),
        # expframes is a tuple of explosion frames
        "expframes": ("gun2xp1.png","gun2xp2.png","gun2xp3.png"),
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (5,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    64: {
        # Exploded Cannon
        "imgname": "gun1xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": (8,5,0),
        # expframes is a tuple of explosion frames
        "expframes": ("gun1xp1.png","gun1xp2.png","gun1xp3.png"),
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (5,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    65: {
        # Exploded blimp
        "imgname": "ship4xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 4,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": (18,12,6,0),
        # expframes is a tuple of explosion frames
        "expframes": ("shell3xp1.png","shell3xp2.png","shell3xp3.png","shell3xp4.png"),
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (15,40),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    81: {
        # Cannon Shell
        "imgname": "bullete1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 15, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": -5,
        # Limits for climb/dive
        "climbmax": 2,
        "climbmin": -5,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": True,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -5,
        "centerheight": -5,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,      
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 62,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": (15,25),
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100
    },
    111: {
        # Life Powerup
        "imgname": "extralife.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": (6,3,0),    
        # Animation frame names   
        "aniframes": ("extralife.png","extralife2.png","extralife3.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    112: {
        # Flamer Powerup
        "imgname": "powerupflamer.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    113: {
        # Shock Powerup
        "imgname": "powerupshock.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    114: {
        # Bio Blaster Powerup
        "imgname": "powerupbio.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    115: {
        # Pulsar Powerup
        "imgname": "poweruppulse.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    116: {
        # Health Powerup
        "imgname": "poweruphealth.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    117: {
        # Armor Powerup
        "imgname": "poweruparmor.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    118: {
        # Healthmax Powerup
        "imgname": "poweruphealthmax.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": (6,3,0),    
        # Animation frame names   
        "aniframes": ("poweruphealthmax.png","poweruphealthmax1.png","poweruphealthmax2.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    },
    119: {
        # Armormax Powerup
        "imgname": "poweruparmormax.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": (-1,1),
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": (1,2),
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": (100, SCREEN_WIDTH -100),
        "centerheight": (-10, 0),
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": (6,3,0),    
        # Animation frame names   
        "aniframes": ("poweruparmormax.png","poweruparmormax1.png","poweruparmormax2.png"),
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0
    }
}

# Create sunmoon
wavesunmoon = SunMoon(0)
# Create our 'player'
player = Player(0)

# Create custom events for adding a new enemy and cloud and bullet and moving sun/moon
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDBULLET = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBULLET, 50)
ADDMOUNTAIN = pygame.USEREVENT + 4
pygame.time.set_timer(ADDMOUNTAIN, 2000)
#MOVESUNMOON = pygame.USEREVENT + 4
#pygame.time.set_timer(MOVESUNMOON, 20000)

# Create groups to hold enemy sprites, cloud sprites, bullet sprites, mountain sprites, and all sprites
# - enemies, bullets, and mountains are used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
mountains = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# - wavesunmoon and player are individual sprites
all_sprites.add(wavesunmoon)
all_sprites.add(player)



# Set player lives, score, special weapons, redflash, greenflash, gamerunning variables


plives = 3
score = 0
flamer = 100
shock = 100
bio = 100
pulse = 100
player.hp = 100
player.armor = 50
healthmax = 200
armormax = 100
# For character deaths
redflash = False
# For stage changes
greenflash = False
# For flash timing
redflashticks = 0
greenflashticks = 0
# ingame being false steers to start screen - press enter to play
ingame = False
# pause state control
pause = False
# default if file not found
highscore = 0
# First wave setup
wave = 1
wavecounter = 0
wavegoal = 150
waveendticks = 0


# check for saved highscore
hsfilename = "highscore.txt"
if os.path.isfile(hsfilename) and os.access(hsfilename, os.R_OK):
    with open(hsfilename, "r") as file:
        hsstr =  file.read()
        if hsstr:
            hs = (int(hsstr))
        else:
            hs = 0
        # If larger than 0, update
        if hs > highscore:
            highscore = hs

# Variable to keep our main loop running - false is exit condition
running = True

# Our main loop
while running:
    try:
        if pause == True and ingame == True:
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == xbox360_controller.START:
                        pause = False
                        pygame.mixer.music.play(loops=-1)
                    if event.button == xbox360_controller.BACK:
                        ingame = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        # Press Enter to Play
                        # unpause
                        pause = False
                        pygame.mixer.music.play(loops=-1)
                    elif event.key == K_ESCAPE:
                        # Prepare for exit
                        ingame = False              
                    #pressed_keysq = pygame.key.get_pressed()
                    #if pressed_keysq == K_p:
                    #    pause = False
                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = False
            # Set Background for start screen     
            #screen.fill((135, 206, 250))
            texts4()
            pygame.display.flip()
        else:
            if ingame:
                #pressed_keysq = pygame.key.get_pressed()
                #if pressed_keysq == K_p:
                #    pause = True
                # Look at events relative to pause status
                for event in pygame.event.get():
                # Did the user hit a key or button?
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == xbox360_controller.START:
                            pause = True
                            pygame.mixer.music.stop()
                        if event.button == xbox360_controller.BACK:
                            ingame = False 
                            for i, enemy1 in enumerate(enemies):
                                enemy1.kill()
                            for i, bullet1 in enumerate(bullets):
                                bullet1.kill()
                            for i, cloud1 in enumerate(clouds):
                                cloud1.kill()                
                            for i, mountain1 in enumerate(mountains):
                                mountain1.kill()                              
                    if event.type == KEYDOWN:
                        # Was it the Escape key? If so, stop the loop
                        if event.key == K_ESCAPE:
                            ingame = False        
                            for i, enemy1 in enumerate(enemies):
                                enemy1.kill()
                            for i, bullet1 in enumerate(bullets):
                                bullet1.kill()
                            for i, cloud1 in enumerate(clouds):
                                cloud1.kill()                
                            for i, mountain1 in enumerate(mountains):
                                mountain1.kill()
                        elif event.key == K_RETURN:
                            pause = True
                            pygame.mixer.music.stop()
                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = False

                    # Should we add a new mountain?
                    elif event.type == ADDMOUNTAIN:
                        if redflash == False and greenflash == False:
                            # wave increases chance
                            if random.randint(1,100) < 25 + (2 * wave):
                                # Create the new mountain, and add it to our sprite groups
                                new_mountain = Mountain()
                                mountains.add(new_mountain)
                                all_sprites.add(new_mountain)


                    # Should we add a new enemy?
                    elif event.type == ADDENEMY:
                        if wavecounter < wavegoal:
                            # No new enemies while dead/wave 'Get Ready'
                            # Percentage of wave complete for factoring rate of enemy spawning
                            wavcompleteperc = int(((wavecounter + wave)/wavegoal) * 100)
                            if wavcompleteperc > 50 and waveboss < wave and random.randint(1,100) > 95:
                                new_enemy = Enemy(41,35,hp,0)
                                enemies.add(new_enemy)
                                all_sprites.add(new_enemy)
                                new_enemy.hp = (new_enemy.hp / 2) * wave
                                waveboss = waveboss + 1

                            if random.randint(1,100) < wavcompleteperc + 25 + wave * wave:
                                enemiestocreate = random.randint(1,int(math.sqrt(wave)))
                                for x in range(1, enemiestocreate + 1):
                                    if redflash == False and greenflash == False:
                                        # Create the new enemy, and add it to our sprite groups
                                        hp = 1
                                        powerup = random.randint(1,100)
                                        if powerup < 3 + wave :
                                            # Blimp1
                                            newetype = 4
                                            hp = 10
                                        if powerup > 2 + wave and powerup < 5 + wave * 2:
                                            # Blimp2
                                            newetype = 5
                                            hp = 20
                                        if powerup > 4 + wave * 2 and powerup < 7 + wave * 3:
                                            # Missile Launcher
                                            newetype = 8
                                        if powerup < 88 and powerup > 6 + wave * 3:
                                            # Missile
                                            newetype = 1
                                        elif powerup > 86 and powerup < 89:
                                            # Health
                                            newetype = 116
                                            if healthmax < healthhardmax:
                                                # 1 in 10 of boost to max health
                                                if random.randint(1,10) > 5:
                                                    newetype = 118
                                        elif powerup > 88 and powerup < 91:
                                            # Armor
                                            newetype = 117
                                            if armormax < armorhardmax:
                                                # 1 in 10 of boost to max armor
                                                if random.randint(1,10) > 5:
                                                    newetype = 119
                                        elif powerup > 90 and powerup < 93:
                                            # Extra Life
                                            newetype = 111
                                        elif powerup > 92 and powerup < 95:
                                            # Power Up FLamer
                                            newetype = 112
                                        elif powerup > 94 and powerup < 97:
                                            # Power Up Shock
                                            newetype = 113
                                        elif powerup > 96 and powerup < 99:
                                            # Power Up Bio
                                            newetype = 114
                                        elif powerup > 97:
                                            # Power Up Pulse
                                            newetype = 115
                                        new_enemy = Enemy(newetype,14,hp,0)
                                        enemies.add(new_enemy)
                                        all_sprites.add(new_enemy)
                                        oops = pygame.sprite.spritecollideany(new_enemy, mountains)
                                        if oops:
                                            if new_enemy.etype < 7 or new_enemy.etype > 8:
                                                new_enemy.kill()

                    # Should we add a new cloud?
                    elif event.type == ADDCLOUD:
                        # Create the new cloud, and add it to our sprite groups
                        new_cloud = Cloud()
                        clouds.add(new_cloud)
                        all_sprites.add(new_cloud)

                    # Should we add a new bullet?
                    elif event.type == ADDBULLET:
                        if player.firebullet > 0 and player.firebullet < 4:
                            # Create the new bullet, and add it to our sprite groups
                            new_bullet = Bullet(player.rect.right,player.rect.bottom,1,8)
                            bullets.add(new_bullet)
                            all_sprites.add(new_bullet)
                            player.firebullet = player.firebullet - 1 
                        elif player.firebullet == 4:
                            # Create the blast bullet, and add it to our sprite groups
                            # Decrement armory
                            if flamer > 0:
                                flamer = flamer - 1
                                new_bullet = Bullet(player.rect.right,player.rect.top,2,30)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)    
                            player.firebullet = 0
                            
                        elif player.firebullet == 5:
                            # Create the lightning shield, and add it to our sprite groups
                            # Decrement armory
                            if shock > 0:
                                shock = shock - 1
                                new_bullet = Bullet(player.rect.right - player.rect.width/2, player.rect.top + player.rect.height/2,3,16)      
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0
                        elif player.firebullet == 6:
                            # Create the bioweapon bullet, and add it to our sprite groups
                            # Decrement armory
                            if bio > 0:
                                bio = bio - 1
                                new_bullet = Bullet(player.rect.right,player.rect.top,4,26)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0
                        elif player.firebullet == 7:
                            # Create the pulse bullet and add it to our sprite groups
                            # Decrement armory
                            if pulse > 0:
                                pulse = pulse - 1
                                new_bullet = Bullet(player.rect.right, player.rect.top,5,65)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0                    
                # Get the set of keys pressed and check for user input
                if redflash or greenflash:
                    # Keep player off screen for flash
                    player.rect.right = -300
                else:
                    #unhide player
                    pressed_keys = pygame.key.get_pressed()
                    player.update(pressed_keys)
                    #player.rect.left = 30

                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys)

                # Fill the screen with wave-appropriate sky blue unless redflash or greenflash
                if redflash:
                    screen.fill((RED))
                    if pygame.time.get_ticks() > redflashticks + 3000:
                        redflash = False
                        player.rect.left = 30
                        pygame.mixer.music.play(loops=-1)
                elif greenflash:
                    screen.fill(GREEN)
                    if pygame.time.get_ticks() > greenflashticks + 3000:
                        greenflash = False
                        player.rect.left = 30
                        pygame.mixer.music.play(loops=-1)
                else:
                    if wave < 4:
                        screen.fill((135 / wave, 206 / wave, 250 / wave))
                        # Evening sky
                    elif wave > 3 and wave < 5:
                        screen.fill((0, 0, 25))
                        # Dark sky
                    elif wave > 4:
                        screen.fill((0,0,5))
                        # Late Night Sky

                # Update the position of our enemies, bullets, and clouds
                wavesunmoon.update(wave)
                mountains.update()
                enemies.update()
                bullets.update()
                #player.update(pressed_keys)
                clouds.update()
                
                # Draw all our sprites
                #while True:
                
                screen.blit(wavesunmoon.surf, wavesunmoon.rect)
                screen.blit(player.surf, player.rect)
                for entity in mountains:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in enemies:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in bullets:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in clouds:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                
                #for entity in all_sprites:
                #    screen.blit(entity.surf, entity.rect)
                # Draw our status box, add texts
                bosses = 0
                bossmode = False
                for e in enemies:
                    if enemydict[e.etype]["boss"] == 1:
                        bossmode = True
                        bosses += 1
                        bhealthmax = enemydict[e.etype]["hp"] / 2 * wave
                        barsizefactor = bhealthmax / 1000
                        barwide = 200 * barsizefactor + 10
                        bosshealthbar((SCREEN_WIDTH / 2 - (barwide // 2)), (bosses * 50), e ,e.hp, bosshealthblink)
                        bosshealthblink = bosshealthblink + 1
                        if bosshealthblink > 20:
                            bosshealthblink = 0
                # Score being non zero blocks bonus spawn at game beginning after lost bossfight            
                if bossmode == False and wasbossmode == True and score > 0:
                    pups = wave * 10
                    newe = 0
                    while newe < pups:
                        newtype = random.randint(111,119)
                        new_enemy = Enemy(newtype,35,hp,0)
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        newe += 1
                wasbossmode = bossmode
                statusdisplay()

                if redflash:
                    pygame.mixer.music.stop()
                    #Count down on get ready message - has to occur after sprites
                    counterstr = ""
                    #font = pygame.font.Font("fonts/ARCADE_R.ttf",30)
                    deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLACK)
                    dtxtoffset = deadtext.width / 2
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                    deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLUE)
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                    # Bigger font for the countdown
                    #font = pygame.font.Font("fonts/ARCADE_R.ttf",75) 
                    if pygame.time.get_ticks() > redflashticks + 2500:
                        counterstr = "1"
                    elif pygame.time.get_ticks() > redflashticks + 2000:
                        counterstr = "2"
                    elif pygame.time.get_ticks() > redflashticks + 1500:
                        counterstr = "3"
                    elif pygame.time.get_ticks() > redflashticks + 1000:
                        counterstr = "4"
                    elif pygame.time.get_ticks() > redflashticks + 500:
                        counterstr = "5"           
                    countertext = font75.render("GET READY: " + counterstr, 1, BLACK)
                    ctxtoffset = countertext.width / 2
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset, SCREEN_HEIGHT / 2))          
                    countertext = font75.render("GET READY: " + counterstr, 1, BLUE)
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset + 2, SCREEN_HEIGHT / 2 + 2))  
                elif greenflash:
                    #Count down on get ready message - has to occur after sprites
                    pygame.mixer.music.stop()
                    counterstr = ""
                    #font = pygame.font.Font("fonts/ARCADE_R.ttf",30)
                    deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLACK)
                    dtxtoffset = deadtext.width / 2
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                    deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLUE)
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                    # Bigger font for the countdown
                    #font = pygame.font.Font("fonts/ARCADE_R.ttf",75) 
                    if pygame.time.get_ticks() > greenflashticks + 2500:
                        counterstr = "1"
                    elif pygame.time.get_ticks() > greenflashticks + 2000:
                        counterstr = "2"
                    elif pygame.time.get_ticks() > greenflashticks + 1500:
                        counterstr = "3"
                    elif pygame.time.get_ticks() > greenflashticks + 1000:
                        counterstr = "4"
                    elif pygame.time.get_ticks() > greenflashticks + 500:
                        counterstr = "5"           
                    countertext = font75.render("GET READY: " + counterstr, 1, BLACK)
                    ctxtoffset = countertext.width / 2
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset, SCREEN_HEIGHT / 2))          
                    countertext = font75.render("GET READY: " + counterstr, 1, BLUE)
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset + 2, SCREEN_HEIGHT / 2 + 2))

                # Check if the player has collided with any mountains
                crash = pygame.sprite.spritecollideany(player, mountains)
                if crash:
                    crash.mask = pygame.mask.from_surface(crash.surf)
                    if pygame.sprite.collide_mask(player, crash):
                        # Decrement lives
                        plives = plives - 1
                        redflash = True
                        redflashticks = pygame.time.get_ticks()
                        # Move player position to hide
                        player.rect.left = -300
                        player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                        # Refill health
                        player.hp = 100
                        # Refill armor
                        player.armor = 50
                        # Cause destruction event for any remaining enemies
                        for i, enemy1 in enumerate(enemies):
                            if enemy1.etype < 41 or enemy1.etype > 41:
                                enemy1.boomcounter = 10
                                if enemydict[enemy1.etype]["isexplodable"]:
                                    enemy1.etype = enemydict[enemy1.etype]["isexplodable"]
                                else:
                                    enemy1.kill()
                                score = score + 1
                                wavecounter = wavecounter + 1                                                           
                        # If no lives remain, kill player
                        if plives < 1:
                            for i, enemy1 in enumerate(enemies):
                                enemy1.kill()
                            # Go to start screen
                            ingame = False

                # Check if any enemies have collided with the player
                # PLAYER ENEMY COLLISIONS
                
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()
                crash = pygame.sprite.spritecollideany(player, enemies)
                if crash:
                    if crash.etype < 100:
                        # Missile or blimp, possibly exploding
                        collision_sound.play()
                        # Implement variable damage
                        damage = random.randint(*enemydict[crash.etype]["damage"])
                        # if player has armor left
                        if player.armor > 0:
                            # Damage armor first
                            player.armor = player.armor - damage
                            # If armor exhausted
                            if player.armor < 0:
                                # Remove remainder from health
                                player.hp = + player.hp + player.armor
                                # Set armor to empty
                                player.armor = 0
                        else:
                            player.hp = player.hp - damage
                        if player.hp < 1:
                            # Decrement lives
                            plives = plives - 1
                            redflash = True
                            redflashticks = pygame.time.get_ticks()
                            # Move player position to hide
                            player.rect.left = -300
                            player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                            # Refill health
                            player.hp = 100
                            # Refill armor
                            player.armor = 50
                            # Cause destruction event for any remaining enemies
                            for i, enemy1 in enumerate(enemies):
                                if enemy1.etype < 41 or enemy1.etype > 41:
                                    enemy1.boomcounter = 10
                                    if enemydict[enemy1.etype]["isexplodable"]:
                                        enemy1.etype = enemydict[enemy1.etype]["isexplodable"]
                                    else:
                                        enemy1.kill()
                                    score = score + 1
                                    wavecounter = wavecounter + 1                                                           
                        # If no lives remain, kill player
                        if plives < 1:
                            for i, enemy1 in enumerate(enemies):
                                enemy1.kill()
                            # Go to start screen
                            ingame = False
                    
                    elif crash.etype == 111:
                        # Extra Life
                        plives = plives + 1
                    elif crash.etype == 112:
                        # Power Up Flamer
                        flamer = flamer + 100
                    elif crash.etype == 113:
                        # Power Up Shock
                        shock = shock + 100
                    elif crash.etype == 114:
                        # Power Up Bio
                        bio = bio + 100
                    elif crash.etype == 115:
                        # Power Up Pulsar
                        pulse = pulse + 100
                    elif crash.etype == 116:
                        # Power Up Health
                        player.hp = player.hp + 50
                        if player.hp > healthmax // 2:
                            player.hp = healthmax // 2 
                    elif crash.etype == 117:
                        # Power Up Armor
                        player.armor = player.armor + 25
                        if player.armor > armormax // 2:
                            player.armor = armormax // 2
                    elif crash.etype == 118:
                        # Raise maximum health
                        healthmax = healthmax + 50
                        if healthmax > healthhardmax:
                            healthmax = healthhardmax
                        # Power Up Health
                        player.hp = player.hp + 50
                        if player.hp > healthmax // 2:
                            player.hp = healthmax // 2  
                    elif crash.etype == 119:
                        # Raise maximum armor
                        armormax = armormax + 25
                        if armormax > armorhardmax:
                            armormax = armorhardmax
                        # Power Up Armor
                        player.armor = player.armor + 25
                        if player.armor > armormax // 2:
                            player.armor = armormax // 2

                    # Remove the Enemy if not boss
                    if enemydict[crash.etype]["boss"] == 0:
                        crash.kill()
                    else:
                        # Player bounces off boss
                        if player.rect.centerx < crash.rect.centerx:
                            player.rect.right = crash.rect.left - 50
                            player.speed = crash.speed + 3
                        else:
                            player.rect.left = crash.rect.right + 50
                            player.speed = crash.speed - 3
                        if player.rect.centery < crash.rect.centery:
                            player.rect.bottom = crash.rect.top - 50
                            player.climb = crash.climb - 3
                        else:
                            player.rect.top = crash.rect.bottom + 50
                            player.climb = crash.climb + 3
                    # Stop any moving sounds and play the collision sound
                    move_up_sound.stop()
                    move_down_sound.stop()
                    shoot_sound.stop()
                    bio_sound.stop()
                    shock_sound.stop()
                    flamer_sound.stop()
                    powerup_sound.stop()
                    wavechange_sound.stop()
                    pulse_sound.stop()
                    if enemydict[crash.etype]["ispowerup"] == False:
                        # If hostile
                        collision_sound.play()
                    elif crash.etype > 100:
                        # If powerup
                        score = score + 25
                        wavecounter = wavecounter + 1
                        powerup_sound.play()
                # Check for other collisions, kill colliding enemies and destructable bullets   
                # ENEMY ENEMY COLLISIONS
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()
                for i, enemy1 in enumerate(enemies):
                    enemy2 = pygame.sprite.spritecollideany(enemy1, enemies)
                    # If enemies collide
                    if enemy2 != enemy1: 
                        # Not with themselves
                        # De-collide, move smaller
                        #enemy2.rect = enemy2.surf.get_rect()
                        if enemy2.rect.height * enemy2.rect.width < enemy1.rect.height * enemy1.rect.width:
                            if enemy2.rect.centerx < enemy1.rect.centerx:
                                enemy2.rect.right = enemy1.rect.left -5
                            else:
                                enemy2.rect.left = enemy1.rect.right +5
                        else:
                            if enemy1.rect.centerx < enemy2.rect.centerx:
                                enemy1.rect.right = enemy2.rect.left -5
                            else:
                                enemy1.rect.left = enemy2.rect.right +5
                        
                        # 2 powerups don't hurt eachother
                        if not(enemydict[enemy1.etype]["ispowerup"] and enemydict[enemy2.etype]["ispowerup"]):
                            collision_sound.play()
                            if enemydict[enemy1.etype]["isexploded"] == False:
                                # is enemy immune?
                                if enemydict[enemy1.etype]["damenemies"] > 0:
                                    enemy1.hp = enemy1.hp - 1
                                    if enemy1.hp < 1:
                                        if enemydict[enemy1.etype]["isexplodable"]:
                                            enemy1.etype = enemydict[enemy1.etype]["isexplodable"]
                                        else:
                                            enemy1.kill()
                                        score = score + enemydict[enemy1.etype]["hp"]
                                        wavecounter = wavecounter + 1
                            if enemydict[enemy2.etype]["isexploded"] == False:                           
                                # is enemy immune?
                                if enemydict[enemy2.etype]["damenemies"] > 0:
                                    enemy2.hp = enemy2.hp - 1
                                    if enemy2.hp < 1:
                                        if enemydict[enemy2.etype]["isexplodable"]:
                                            enemy2.etype = enemydict[enemy2.etype]["isexplodable"]
                                        else:
                                            enemy2.kill()
                                        score = score + enemydict[enemy2.etype]["hp"]
                                        wavecounter = wavecounter + 1
                # BULLET ENEMY COLLISIONS  
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()      
                for i, thisenemy in enumerate(enemies):
                    bullethit = pygame.sprite.spritecollideany(thisenemy, bullets)
                    # If bullet hits enemy
                    if bullethit:
                        collision_sound.play()
                        if enemydict[thisenemy.etype]["isexploded"] == False and enemydict[thisenemy.etype]["ispowerup"] == False:
                            thisenemy.hp -= 1
                            if thisenemy.hp < 1:
                                if enemydict[thisenemy.etype]["isexplodable"]:
                                    thisenemy.etype = enemydict[thisenemy.etype]["isexplodable"]
                                else:
                                    thisenemy.kill()
                                score = score + enemydict[thisenemy.etype]["hp"]
                                wavecounter += 1
                            if bullethit.btype == 1:
                                # MG bullets go away on impact
                                bullethit.kill()
                            else:
                                # Large bullets degraded by impacts
                                bullethit.boomcounter -= 1                            
                # BULLET MOUNTAIN COLLISIONS        
                for i, thismountain in enumerate(mountains):
                    bullethit = pygame.sprite.spritecollideany(thismountain, bullets)
                    if bullethit:
                        if bullethit.btype == 1:
                            bullethit.kill()
                        else:
                            # Large bullets seriously degraded by mountains
                            if bullethit.boomcounter > 2:
                                bullethit.boomcounter = 2
                # ENEMY MOUNTAIN COLLISIONS  
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()         
                for i, thismountain in enumerate(mountains):
                    enemyhit = pygame.sprite.spritecollideany(thismountain, enemies)
                    if enemyhit:
                        if enemyhit.etype > 8 or enemyhit.etype < 7: #cannon sit on mountain, missile launchers stay on ground
                            # Move enemy up
                            enemyhit.rect.bottom -= 50
                            enemyhit.climb = -3
                            # Bounce enemy left/right from mountain
                            if enemyhit.rect.centerx < thismountain.rect.centerx:
                                enemyhit.rect.right = thismountain.rect.left - 10
                                enemyhit.speed = 4
                            else:
                                enemyhit.rect.left = thismountain.rect.right + 10
                                enemyhit.speed = 6
                        if enemydict[enemyhit.etype]["isexploded"] == False:
                            if enemyhit.etype > 8 or enemyhit.etype < 7: #cannon sit on mountain 
                                # If enemy takes damage from mountain collisions 
                                if enemydict[enemyhit.etype]["dammountain"] > 0:      
                                    # Calculate partial immunity if applicable                 
                                    enemyhit.hp = enemyhit.hp - int(100 * enemydict[enemyhit.etype]["dammountain"] / 100)
                                    if enemyhit.hp < 0:
                                        if enemydict[enemyhit.etype]["isexplodable"]:
                                            enemyhit.etype = enemydict[enemyhit.etype]["isexplodable"]
                                        else:
                                            if enemydict[enemyhit.etype]["isexploded"] == False:
                                                enemyhit.kill()
                                        score = score + 1
                if wavecounter > wavegoal or wavecounter == wavegoal:
                    if bossmode == False:
                        waveendticks += 1
                    if len(enemies) == 0 or waveendticks > 150:
                        # Set up next wave
                        wave = wave + 1
                        wavegoal = wavegoal + (wave * wave * 10) + 100
                        wavecounter = 0
                        waveendticks = 0
                        # Green flash for wave complete
                        greenflash = True
                        greenflashticks = pygame.time.get_ticks()
                        move_up_sound.stop()
                        move_down_sound.stop()
                        shoot_sound.stop()
                        collision_sound.stop()
                        bio_sound.stop()
                        shock_sound.stop()
                        flamer_sound.stop()
                        powerup_sound.stop()
                        pulse_sound.stop()
                        wavechange_sound.play()
                        # Move player positon to hide
                        player.rect.left = -300
                        player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                        # update sunmoon state & new random position
                        wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                        wavesunmoon.update(wave)
                if score > highscore:
                    highscore = score
                # Flip everything to the display
                pygame.display.flip()
                
                # Ensure we maintain a 30 frames per second rate
                clock.tick(30)
            else:
                # Get rid of any remaining sprites except sunmoon and player
                # Park on start screen
                pygame.mixer.music.stop()
                for i, enemy1 in enumerate(enemies):
                    enemy1.kill()
                for i, bullet1 in enumerate(bullets):
                    bullet1.kill()
                for i, cloud1 in enumerate(clouds):
                    cloud1.kill()       
                for i, mountain1 in enumerate(mountains):
                    mountain1.kill()
                # Update highscore
                if score > highscore:
                    highscore = score
                # Look at every event in the queue
                for event in pygame.event.get():
                    # Did the user hit a key or joystick button?
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == xbox360_controller.START:
                            # Press Enter to Play
                            # Reinitialize gamestate at start
                            ingame = True
                            pause = False
                            plives = 3
                            score = 0
                            flamer = 100
                            shock = 100
                            bio = 100
                            pulse = 100
                            wave = 1
                            redflash = False
                            greenflash = False
                            player.hp = 100
                            player.armor = 50  
                            healthmax = 200
                            armormax = 100
                            wavecounter = 0
                            wavegoal = 150
                            waveboss = 0
                            waveendticks = 0
                            pygame.mixer.music.play(loops=-1)
                            wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                            wavesunmoon.update(wave)
                            player.rect.left = 30
                            player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                        if event.button == xbox360_controller.BACK:
                            # Prepare for exit
                            running = False           
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            # Press Enter to Play
                            # Reinitialize gamestate at start
                            ingame = True
                            pause = False
                            plives = 3
                            score = 0
                            flamer = 100
                            shock = 100
                            bio = 100
                            pulse = 100
                            wave = 1
                            redflash = False
                            greenflash = False
                            player.hp = 100
                            player.armor = 50  
                            healthmax = 200
                            armormax = 100
                            wavecounter = 0
                            wavegoal = 150
                            waveboss = 0
                            waveendticks = 0
                            pygame.mixer.music.play(loops=-1)
                            wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                            wavesunmoon.update(wave)
                            player.rect.left = 30
                            player.rect.top = SCREEN_HEIGHT_NOBOX / 5

                        elif event.key == K_ESCAPE:
                            # Prepare for exit
                            running = False               
                        pressed_keysq = pygame.key.get_pressed()
                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = False
                # Set Background for start screen     
                screen.fill((135, 206, 250))
                # Draw Enter to Play, Esc to Exit, High Score
                texts3(highscore)
                # Flip everything to the display
                pygame.display.flip()
                # Ensure we maintain a 30 frames per second rate
                clock.tick(30)
    except TypeError:
        print(entity.name)
        quit
#Save highscore
with open(hsfilename, "w") as file:
    file.write(str(highscore))
  
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
