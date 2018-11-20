import pygame
import gamebox
import urllib.request
import random
from pygame import Color

camera = gamebox.Camera(800, 600)       #sets camera/window
screen = pygame.display.set_mode((800, 600))
ball_velocity = 5
game_on = False

ticker = 0
translation = 0
clear = Color("Black")

walls = [gamebox.from_color(400, 600, "black", 1000, 10),       #sets bounds
    gamebox.from_color(400, 0, clear, 1000, 0),]

top_pipe = gamebox.from_color(800, 59, "Black", 25, 600)        #sets top and bottom pipe gameboxes
bot_pipe = gamebox.from_color(800, 759, "Black", 25, 600)
bird = gamebox.from_color(400, 300, "green", 20, 20)
bird.yspeed = ball_velocity
top_pipe.xspeed = -5
bot_pipe.xspeed = -5
img = urllib.request.urlretrieve("https://www.desktopbackground.org/download/800x600/2014/07/26/799251_flappy-bird-charizard-edition-on-scratch_1920x1080_h.png")
bg = pygame.image.load('background.png')
score = 0

def tick(keys):

    global game_on
    global ticker
    global translation
    global score

    if not game_on:         #start game argument
        camera.draw(gamebox.from_text(400, 350, 'Press up to start: ', 60, "Black", True))
    camera.display()

    if game_on:         #if game running, add 1 to score for every pipe the player makes it through
        if top_pipe.x and bot_pipe.x == bird.x:
            score += 1

    if game_on:
        ticker += (1/30)

    translation += (1/30)       #tbh not sure what this does
    if translation*15 > 2000:
        translation= 0
    screen.blit(bg, (-translation*15, 0))

    if game_on:             #sets movement of player and pipes
        bird.move_speed()
        top_pipe.move_speed()
        bot_pipe.move_speed()
        bird.yspeed += 0.35

    if top_pipe.x == 0:         #reset function for the pipes
        pipe_gap = random.randint(65,100)
        top_displacement = random.randint(-250, 250)
        top_on_screen = 250 + top_displacement
        bot = 600 - top_on_screen - pipe_gap
        bot_displacement = 250 + 600 - bot
        top_pipe.move(800, 0)
        bot_pipe.move(800, 0)
        top_pipe.center = [800, bot_displacement]
        bot_pipe.center = [800, top_displacement]

    if pygame.K_UP in keys:
        game_on = True

    if pygame.K_SPACE in keys:          #player input argument
        bird.yspeed += -7
        keys.clear()

    if game_on:             #draw argument
        camera.draw(gamebox.from_text(300, 50, str(score), 50, "Black", bold=True))
        for wall in walls:
            camera.draw(wall)
        camera.draw(top_pipe)
        camera.draw(bot_pipe)
        camera.draw(bird)

    if top_pipe.touches(bird) or bot_pipe.touches(bird) or bird.touches(walls[0]) or bird.touches(walls[1]):
        camera.clear("black")       #game over argument
        bird.center = [200, 100]
        camera.draw(gamebox.from_text(400, 300, str("You made it through: "), 50, "White", bold=True))
        camera.draw(gamebox.from_text(400, 400, str(score), 50, "White", bold=True))
        camera.draw(gamebox.from_text(400, 500, str("pipes!"), 50, "White", bold=True))
        gamebox.pause()


gamebox.timer_loop(30, tick)

'''things to do: get rid of black bar at bottom, make sure pipes are always going to be on screen/able to pass through'''