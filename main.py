# Kurt Bruckbauer

import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# Create the Game Window
screen = pygame.display.set_mode((1000, 800))
background = pygame.image.load("background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)    # -1 value plays ound file on loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("x_wing64.png")
xcor = 470
ycor = 640
xcor_change = 0
ycor_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Bullet:
bullet_img = pygame.image.load("yellow_bullet.png")
bullet_xcor = 0
bullet_ycor = 640
bullet_xcor_change = 0
bullet_ycor_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# GAME_OVER_TEXT
over_font = pygame.font.Font("freesansbold.ttf", 64)

def gameOver_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (400, 500))  # Prints GAME OVER TO screen at x & y coords



# Ready BULLET_STATE - You cant see bullet on screen
# Fire BULLET_STATE - The bullet is visible & moving
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Changes state of the bullet on function call(SPACE_BAR)
    screen.blit(bullet_img, (x + 16, y + 10))  # Places bullet at noise of ship & prints img to the window


# Alien
alien_img = []
alien_xcor = []
alien_ycor = []
alien_xcor_change = []
alien_ycor_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alien_img.append(pygame.image.load("alien.png"))
    alien_xcor.append(random.randint(0, 935))
    alien_ycor.append(random.randint(50, 150))
    alien_xcor_change.append(1)
    alien_ycor_change.append(40)


def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))


# Function to determine collision bt bullet and aliens
def isCollision(alien_xcor, alien_ycor, bullet_xcor, bullet_ycor):
    distance = math.sqrt((alien_xcor - bullet_xcor) ** 2 + (alien_ycor - bullet_ycor) ** 2)
    if distance < 27:
        return True
    else:
        return False


# Game Loop

running = True
while running:

    screen.fill((0, 0, 50))  # RGB value
    # Background Image displays space photo as background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If a keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            xcor_change = -5
        if event.key == pygame.K_RIGHT:
            xcor_change = 5
        if event.key == pygame.K_SPACE:  # Binds SPACE_BAR to shooting bullet
            if bullet_state is "ready":  # Checks if bullet is on the screen or not
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bullet_xcor = xcor  # Gets the current ship location, assigns it to the bullet

                fire_bullet(bullet_xcor, bullet_ycor)  # Attach the fire_bullet function to SPACE_BAR

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            xcor_change = 0

    xcor += xcor_change
    # X-WING border control
    if xcor <= 0:
        xcor = 0
    elif xcor >= 936:
        xcor = 936

    # Bullet movement
    if bullet_ycor <= 0:  # ~~> IF the bullet reaches top of window -->
        bullet_ycor = 600  # --> reset bullet position to bottom of window -->
        bullet_state = "ready"  # --> reset BULLET_STATE to 'ready' which also takes off the screen

    if bullet_state is "fire":  # If the BULLET_STATE = FIRE -->
        fire_bullet(bullet_xcor, bullet_ycor)  # --> then FIRE BULLET -->
        bullet_ycor -= bullet_ycor_change  # --> moves bullet up the YCOR until it reaches the 0 YCOR~~^

    # Alien Movement
    for i in range(num_of_aliens):

        # Game Over
        if alien_ycor[i] > 640:
            for j in range(num_of_aliens):
                alien_ycor[i] = 2000
            gameOver_text()
            break
        alien_xcor[i] += alien_xcor_change[i]
        # Alien border control
        if alien_xcor[i] <= 0:
            alien_xcor_change[i] = 1
            alien_ycor[i] += alien_ycor_change[i]
        elif alien_xcor[i] >= 936:
            alien_xcor_change[i] = -1
            alien_ycor[i] += alien_ycor_change[i]

        # Collision of Bullet & Alien
        collision = isCollision(alien_xcor[i], alien_ycor[i], bullet_xcor, bullet_ycor)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_ycor = 680
            bullet_state = "ready"
            score_value += 1

            alien_xcor[i] = random.randint(0, 935)
            alien_ycor[i] = random.randint(50, 150)

        alien(alien_xcor[i], alien_ycor[i], i)

    player(xcor, ycor)
    show_score(textX, textY)
    pygame.display.update()
