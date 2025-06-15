import pygame
import math
import random
import time
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (800, 600))

gameOverBackground = pygame.image.load('spaceBg.jpg')
gameOverBackground = pygame.transform.scale(gameOverBackground, (800, 600))

mixer.music.load('bgm.mp3')
mixer.music.play(-1)
# mixer.music.set_volume(0.1)

aliveHeartImage = pygame.image.load('aliveHeart.png')
aliveHeartImage = pygame.transform.scale(aliveHeartImage, (35, 35))

deadHeartImage = pygame.image.load('deadHeart.png')
deadHeartImage = pygame.transform.scale(deadHeartImage, (35, 35))

bunker1Image = pygame.image.load('bunker1.png')
bunker1Image = pygame.transform.scale(bunker1Image, (75, 75))

bunker2Image = pygame.image.load('bunker2.png')
bunker2Image = pygame.transform.scale(bunker2Image, (75, 75))

bunker3Image = pygame.image.load('bunker3.png')
bunker3Image = pygame.transform.scale(bunker3Image, (75, 75))

playerImage = pygame.image.load('spaceship (1).png')
playerImage = pygame.transform.scale(playerImage, (55, 55))
playerX = 375
playerY = 500

playerX_change = 0
playerY_change = 0

bulletImage = pygame.image.load('bullet.png');
bulletImage = pygame.transform.scale(bulletImage, (15, 15))
bullet_state = False
bulletX = 0
bulletY = 0

enemyBulletImage = pygame.image.load('bulletEnemy.png');
enemyBulletImage = pygame.transform.scale(enemyBulletImage, (15, 15))
enemy_bullets = []

enemy1Image = pygame.image.load('alien1.png')
enemy1Image = pygame.transform.scale(enemy1Image, (50, 50))

enemy2Image = pygame.image.load('alien2.png')
enemy2Image = pygame.transform.scale(enemy2Image, (50, 50))

enemy3Image = pygame.image.load('alien3.png')
enemy3Image = pygame.transform.scale(enemy3Image, (50, 50))

enemy4Image = pygame.image.load('ufo.png')
enemy4Image = pygame.transform.scale(enemy4Image, (50, 50))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy1(x, y):
    screen.blit(enemy1Image, (x, y))


def enemy2(x, y):
    screen.blit(enemy2Image, (x, y))


def enemy3(x, y):
    screen.blit(enemy3Image, (x, y))


def enemy4(x, y):
    screen.blit(enemy4Image, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImage, (x, y))


def enemy_fire_bullet(x, y):
    enemy_bullets.append({'x': x, 'y': y})


enemyPos = [
    [0, 0, 1, 3, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0]
]

enemyAliveLocations = [[0 for _ in range(7)] for _ in range(5)]

enemyInfo = []
enemyAliveLocations[0][5] = 1

start_x = 120
start_y = 10

enemy_x_spacing = 80
enemy_y_spacing = 60

for row_index, row in enumerate(enemyPos):
    for col_index, value in enumerate(row):
        if value:
            x_coordinate = start_x + col_index * enemy_x_spacing
            y_coordinate = start_y + row_index * enemy_y_spacing

            if row_index in [0, 4]:
                etype = 1
            elif row_index in [1, 3]:
                etype = 2
            else:
                etype = 3

            if (value == 3):
                etype = 4

            enemyInfo.append(
                {'x': x_coordinate, 'y': y_coordinate, 'x_pos': row_index, 'y_pos': col_index, 'type': etype,
                 'alive': True, 'lives': value})
            enemyAliveLocations[row_index][col_index] = 1


def isCollision(bulletX, bulletY):
    bullet_rect = pygame.Rect(bulletX, bulletY, bulletImage.get_width(), bulletImage.get_height())
    for enemy in enemyInfo:
        if enemy['alive']:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy1Image.get_width(), enemy1Image.get_height())
            if bullet_rect.colliderect(enemy_rect):
                return enemy
    return None


bunkerInfo = []

for i in range(3):
    bunkerInfo.append({'x': 145 + 200 * i, 'y': 400, 'health': 3})


def bunker1(x, y):
    screen.blit(bunker1Image, (x, y))

def bunker2(x, y):
    screen.blit(bunker2Image, (x, y))

def bunker3(x, y):
    screen.blit(bunker3Image, (x, y))


def isBunkerHit(bulletX, bulletY):
    bullet_rect = pygame.Rect(bulletX, bulletY, bulletImage.get_width(), bulletImage.get_height())
    for bunker in bunkerInfo:
        if bunker['health'] > 0:
            bunker_rect = pygame.Rect(bunker['x'], bunker['y'], bunker1Image.get_width(), bunker1Image.get_height())
            if bullet_rect.colliderect(bunker_rect):
                return bunker
    return None


noOfLives = 3


def isPlayerHit(bulletX, bulletY, playerX, playerY):
    bullet_rect = pygame.Rect(bulletX, bulletY, bulletImage.get_width(), bulletImage.get_height())
    player_rect = pygame.Rect(playerX, playerY, playerImage.get_width(), playerImage.get_height())
    return bullet_rect.colliderect(player_rect)


score_value = 0
font = pygame.font.Font('spaceboy.ttf', 18)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (166, 134, 240))
    screen.blit(score, (x, y))


def showHealth(x, y):
    health = font.render("Health ", True, (166, 134, 240))
    screen.blit(health, (x - 2, y))
    totalHearts = 3
    for i in range(totalHearts):
        screen.blit(aliveHeartImage, (x + 30 * i, y + 25))
    for i in range(3 - noOfLives):
        screen.blit(deadHeartImage, (x + 30 * (totalHearts - i - 1), y + 25))


def gameOver(ifWon):
    screen.fill((0, 0, 0))
    screen.blit(gameOverBackground, (0, 0))

    over_font = pygame.font.Font('spaceboy.ttf', 60)
    small_font = pygame.font.Font('spaceboy.ttf', 30)

    game_over_text = over_font.render("GAME OVER", True, (176, 140, 255))
    win_or_lose_text = over_font.render("You Win !" if ifWon else "You Lost !", True, (176, 140, 255))
    score_text = small_font.render(f"Final Score: {score_value}", True, (255, 255, 255))

    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
    screen.blit(win_or_lose_text, (screen.get_width() // 2 - win_or_lose_text.get_width() // 2, 235))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 325))

    button_font = pygame.font.Font('spacebar.ttf', 15)
    play_again_text = button_font.render("Play Again", True, (0, 0, 0))
    quit_text = button_font.render("Quit", True, (0, 0, 0))

    play_again_rect = pygame.Rect(screen.get_width() // 2 - 150, 450, 140, 50)
    quit_rect = pygame.Rect(screen.get_width() // 2 + 10, 450, 100, 50)

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (120, 227, 235) if play_again_rect.collidepoint(mouse_pos) else (140, 247, 255),
                     play_again_rect)
    pygame.draw.rect(screen, (235, 80, 80) if quit_rect.collidepoint(mouse_pos) else (255, 100, 100), quit_rect)

    screen.blit(play_again_text, (play_again_rect.x + 5, play_again_rect.y + 15))
    screen.blit(quit_text, (quit_rect.x + 25, quit_rect.y + 15))

    pygame.display.update()

    pygame.mixer.music.pause()

    if ifWon:
        game_over_sound = mixer.Sound('gameWinBGM.mp3')
    else:
        game_over_sound = mixer.Sound('gameOverBGM.mp3')

    game_over_sound.play()
    time.sleep(game_over_sound.get_length())

    pygame.mixer.music.unpause()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    waiting = False
                    return True
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return False
                    exit()


def allEnemiesDead():
    return all(not enemy['alive'] for enemy in enemyInfo)


enemy_fire_delay = 1000
last_enemy_fire_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

running = True
isGameOver = False
isWon = False
PLAYER_SPEED = 8
BULLET_SPEED = 12

while running:
    clock.tick(60)
    if isGameOver == False:
        if allEnemiesDead():
            isWon = True
            isGameOver = True
        screen.fill((14, 8, 22))  # RGB
        screen.blit(background, (0, 0))

        for bunker in bunkerInfo:
            if bunker['health'] <= 0:
                continue
            if bunker['health'] == 3:
                bunker1(bunker['x'], bunker['y'])
            elif bunker['health'] == 2:
                bunker2(bunker['x'], bunker['y'])
            elif bunker['health'] == 1:
                bunker3(bunker['x'], bunker['y'])

        for enemy in enemyInfo:
            if enemy['alive']:
                if enemy['type'] == 1:
                    enemy1(enemy['x'], enemy['y'])
                elif enemy['type'] == 2:
                    enemy2(enemy['x'], enemy['y'])
                elif enemy['type'] == 3:
                    enemy3(enemy['x'], enemy['y'])
                elif enemy['type'] == 4:
                    enemy4(enemy['x'], enemy['y'])
                    health_text = font.render(f"Boss HP: {enemy['lives']}", True, (255, 0, 0))
                    screen.blit(health_text, (645, 80))

        player_bullets = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    playerX_change += PLAYER_SPEED
                if event.key == pygame.K_UP:
                    playerY_change -= PLAYER_SPEED
                elif event.key == pygame.K_DOWN:
                    playerY_change += PLAYER_SPEED
                if event.key == pygame.K_SPACE:
                    if bullet_state == False:
                        mixer.Sound('laser2.wav').play()
                        player_bullets.append({'x': playerX, 'y': playerY})
                        bulletX = playerX
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerX_change = 0
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change
        if (playerX + playerX_change) < 40:
            playerX = 40
        if (playerX + playerX_change) >= 740:
            playerX = 740
        if (playerY + playerY_change) < 480:
            playerY = 480
        if (playerY + playerY_change) >= 532:
            playerY = 532
        player(playerX - 20, playerY + 10)

        if bulletY <= 0:
            bulletY = playerY
            bullet_state = False

        if bullet_state == True:
            fire_bullet(bulletX, bulletY)
            bulletY -= BULLET_SPEED

            hit_bunker = isBunkerHit(bulletX, bulletY)
            if hit_bunker:
                mixer.Sound('explosion.wav').play()
                hit_bunker['health'] -= 1
                bullet_state = False
                bulletX = playerX
                bulletY = playerY
                continue

            hit_enemy = isCollision(bulletX, bulletY)
            if hit_enemy:
                mixer.Sound('explosionEnemy.mp3').play()
                hit_enemy['lives'] -= 1
                if hit_enemy['lives'] == 0:
                    hit_enemy['alive'] = False
                    enemyAliveLocations[hit_enemy['x_pos']][hit_enemy['y_pos']] = 0
                score_value += 1
                bullet_state = False
                bulletX = playerX
                bulletY = playerY

        # for bullet in player_bullets[:]:
        #     bullet['y'] -= BULLET_SPEED
        #     fire_bullet(bullet['x'], bullet['y'])
        #
        #     hit_bunker = isBunkerHit(bullet['x'], bullet['y'])
        #     if hit_bunker:
        #         print(f"Bunker hit at ({hit_bunker['x']}, {hit_bunker['y']}), health left: {hit_bunker['health']}")
        #         hit_bunker['health'] -= 1
        #         player_bullets.remove(bullet)
        #         continue
        #
        #     hit_enemy = isCollision(bullet['x'], bullet['y'])
        #     if hit_enemy:
        #         mixer.Sound('explosion.wav').play()
        #         hit_enemy['lives'] -= 1
        #         if hit_enemy['lives'] == 0:
        #             hit_enemy['alive'] = False
        #             enemyAliveLocations[hit_enemy['x_pos']][hit_enemy['y_pos']] = 0
        #         score_value += 1
        #         player_bullets.remove(bullet)
        #         continue
        #
        #     if bullet['y'] <= 0:
        #         player_bullets.remove(bullet)

        for bullet in enemy_bullets[:]:
            bullet['y'] += BULLET_SPEED
            screen.blit(enemyBulletImage, (bullet['x'], bullet['y']))

            hit_bunker = isBunkerHit(bullet['x'], bullet['y'])
            if hit_bunker:
                mixer.Sound('explosion.wav').play()
                hit_bunker['health'] -= 1
                enemy_bullets.remove(bullet)

            if isPlayerHit(bullet['x'], bullet['y'], playerX - 20, playerY + 10):
                mixer.Sound('explosionWarning.mp3').play()
                noOfLives -= 1
                enemy_bullets.remove(bullet)
                if noOfLives == 0:
                    isGameOver = True
            if bullet['y'] > 600:
                enemy_bullets.remove(bullet)

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_fire_time > enemy_fire_delay:
            EnemyColStillAlive = []
            for i in range(len(enemyAliveLocations)):
                for j in range(len(enemyAliveLocations[i])):
                    if enemyAliveLocations[i][j] == 1:
                        if j not in EnemyColStillAlive:
                            EnemyColStillAlive.append(j)

            colSelected = random.choice(EnemyColStillAlive)
            enemyFiring = []

            for i in range(len(enemyAliveLocations) - 1, -1, -1):
                if enemyAliveLocations[i][colSelected] == 1:
                    enemyFiring.append([i, colSelected])
                    break

            last_enemy_fire_time = current_time

            for enemyFiringI in enemyFiring:
                enemyRow = enemyFiringI[0]
                enemyCol = enemyFiringI[1]
                for enemy in enemyInfo:
                    if enemy['x_pos'] == enemyRow and enemy['y_pos'] == enemyCol and enemy['alive']:
                        enemy_fire_bullet(enemy['x'] + 18, enemy['y'] + 40)
                        break

        show_score(textX, textY)
        showHealth(675, 10)
        pygame.display.update()

    else:
        restart = gameOver(True if isWon else False)
        if restart:
            isGameOver = False
            running = True
            noOfLives = 3
            score_value = 0
            playerX = 375
            playerY = 500
            playerX_change = 0
            playerY_change = 0
            bullet_state = False
            bulletX = 0
            bulletY = 0
            enemy_bullets.clear()

            for enemy in enemyInfo:
                enemy['lives'] = 1
                enemy['alive'] = True
                enemyAliveLocations[enemy['x_pos']][enemy['y_pos']] = 1
                if enemy['type'] == 4:
                    enemy['lives'] = 3

            bunkerInfo.clear()
            for i in range(3):
                bunkerInfo.append({'x': 145 + 200 * i, 'y': 400, 'health': 3})

        else:
            break
