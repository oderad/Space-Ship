import pygame
import random
import math
from pygame import mixer

# initialized pygame
pygame.init()

# creates screen
#800 is width 600 is height
DISPLAYSURF = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('/media/pi/PHILIPS UFD/surfaces/space.jpg')
background = pygame.transform.scale(background,(800,600))

# displays on taskbar
pygame.display.set_caption("Asteroid Invasion")
icon = pygame.image.load('/media/pi/PHILIPS UFD/surfaces/ufo.png')
pygame.display.set_icon(icon)

#player
playerIMG = pygame.image.load('/media/pi/PHILIPS UFD/surfaces/ship.png')
playerX = 470
playerY = 480
playerX_change = 0

#Enemy
# the [] creates a list which enables the different amounts
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('/media/pi/PHILIPS UFD/surfaces/asteroid.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

#Missle
# ready means bullet can't be seen
# fire means bullet
missileIMG = pygame.image.load('/media/pi/PHILIPS UFD/surfaces/missile.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 10
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    DISPLAYSURF.blit(over_text, (200, 250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    DISPLAYSURF.blit(score, (x, y))

def player(x,y):
    DISPLAYSURF.blit(playerIMG, (x, y))

def enemy(x,y,i):
    DISPLAYSURF.blit(enemyIMG[i], (x, y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    DISPLAYSURF.blit(missileIMG, (x+16, y+10))
    
def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX,2)) + (math.pow(enemyY - missileY,2)))
    if distance < 27:
        return True
    else:
        return False

# this is our game loop
running = True
while running: # main game loop
    # RGB - Red, Green, Blue
    DISPLAYSURF.fill((0, 0, 0))
    # Background image
    DISPLAYSURF.blit(background, (0, 0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke pressed check if left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    # this gets current x coordinate of ship then stores in missileX
                    missileX = playerX
                    fire_missile(playerX, missileY)
        
        
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    
    playerX += playerX_change
    
    # Code for the boundaries and borders
    if playerX <= 0:
        playerX = 0
    #The reason we did 736 and not 800 is because image is 64 pixels so 800-64=736
    elif playerX >= 736:
        playerX = 736
    
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        
        enemyX[i] += enemyX_change[i]
        # Code for the boundaries and borders
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
    #The reason we did 736 and not 800 is because image is 64 pixels so 800-64=736
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]
        
      # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            missileY = 480
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
        
    # Bullet movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"
        
        
    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change
  
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()