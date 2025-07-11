def main_game():
    import pygame
    import random
    from pygame import mixer
    import bossFight
    import settings
    import sys

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load(r'resources\images\spaceship.png')
    pygame.display.set_icon(icon)

    background = pygame.image.load(r'resources\images\background.jpg')
    background = pygame.transform.scale(background, (800, 600))

    gameOverBackground = pygame.image.load(r'resources\images\spaceBg.jpg')
    gameOverBackground = pygame.transform.scale(gameOverBackground, (800, 600))

    mixer.music.load(r'resources\sounds\bgm.mp3')
    mixer.music.play(-1)
    # mixer.music.set_volume(0.1)

    aliveHeartImage = pygame.image.load(r'resources\images\aliveHeart.png')
    aliveHeartImage = pygame.transform.scale(aliveHeartImage, (35, 35))

    deadHeartImage = pygame.image.load(r'resources\images\deadHeart.png')
    deadHeartImage = pygame.transform.scale(deadHeartImage, (35, 35))

    bunker1Image = pygame.image.load(r'resources\images\bunker1.png')
    bunker1Image = pygame.transform.scale(bunker1Image, (75, 75))

    bunker2Image = pygame.image.load(r'resources\images\bunker2.png')
    bunker2Image = pygame.transform.scale(bunker2Image, (75, 75))

    bunker3Image = pygame.image.load(r'resources\images\bunker3.png')
    bunker3Image = pygame.transform.scale(bunker3Image, (75, 75))

    playerImage = pygame.image.load(r'resources\images\spaceship (1).png')
    playerImage = pygame.transform.scale(playerImage, (55, 55))
    playerX = 375
    playerY = 500
    playerX_change = 0
    playerY_change = 0
    bulletImage = pygame.image.load(r'resources\images\bullet.png');
    bulletImage = pygame.transform.scale(bulletImage, (15, 15))
    bulletX = 0
    bulletY = 0
    player_bullets = []

    enemyBulletImage = pygame.image.load(r'resources\images\bulletEnemy.png');
    enemyBulletImage = pygame.transform.scale(enemyBulletImage, (15, 15))
    enemy_bullets = []

    enemy1Image = pygame.image.load(r'resources\images\alien1.png')
    enemy1Image = pygame.transform.scale(enemy1Image, (50, 50))

    enemy2Image = pygame.image.load(r'resources\images\alien2.png')
    enemy2Image = pygame.transform.scale(enemy2Image, (50, 50))

    enemy3Image = pygame.image.load(r'resources\images\alien3.png')
    enemy3Image = pygame.transform.scale(enemy3Image, (50, 50))

    enemy4Image = pygame.image.load(r'resources\images\ufo.png')
    enemy4Image = pygame.transform.scale(enemy4Image, (50, 50))

    settings.sfx_enabled = True
    music_enabled = True

    def toggle_mute():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            settings.music_enabled = False
        else:
            pygame.mixer.music.unpause()
            settings.music_enabled = True



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
        player_bullets.append({'x': x, 'y': y + 10})  

    def enemy_fire_bullet(x, y):
        enemy_bullets.append({'x': x, 'y': y})

    def drawBunkers():
        for bunker in bunkerInfo:
            if bunker['health'] <= 0:
                continue
            if bunker['health'] == 3:
                bunker1(bunker['x'], bunker['y'])
            elif bunker['health'] == 2:
                bunker2(bunker['x'], bunker['y'])
            elif bunker['health'] == 1:
                bunker3(bunker['x'], bunker['y'])

    def drawEnemies():
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

    enemyPos = [
        [0, 0, 1, 1, 1, 0, 0],
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

                if value == 3:
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
    font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 18)

    textX = 10
    textY = 10


    def show_score(x, y):
        score = font.render("Kills: " + str(score_value), True, (166, 134, 240))
        screen.blit(score, (x, y))


    def load_high_score():
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(new_high_score):
        with open("highscore.txt", "w") as file:
            file.write(str(new_high_score))


    def showHealth(x, y):
        health = font.render("Health ", True, (250, 22, 22))
        screen.blit(health, (x + 8, y))
        totalHearts = 3
        for i in range(totalHearts):
            screen.blit(aliveHeartImage, (x + 30 * i, y + 25))
        for i in range(3 - noOfLives):
            screen.blit(deadHeartImage, (x + 30 * (totalHearts - i - 1), y + 25))

    def gameOver(ifWon, kills, timeTaken, livesLeft):
        screen.fill((0, 0, 0))
        screen.blit(gameOverBackground, (0, 0))

        end_time = pygame.time.get_ticks()

        if not ifWon:
            timeTaken = 0
            livesLeft = 0

        score_value = int(livesLeft * 50 + kills * 5 + timeTaken * 2)
        high_score = load_high_score()
        if score_value > high_score:
            high_score = score_value
            save_high_score(high_score)

        over_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 60)
        small_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 30)

        game_over_text = over_font.render("GAME OVER", True, (176, 140, 255))
        win_or_lose_text = over_font.render("You Win!" if ifWon else "You Lost!", True, (176, 140, 255))
        score_text = small_font.render(f"Final Score: {score_value}", True, (255, 255, 255))
        high_score_text = small_font.render(f"High Score: {high_score}", True, (255, 255, 255))


        button_font = pygame.font.Font(r'resources/fonts/SPACEBAR.TTF', 15)
        play_again_text = button_font.render("Play Again", True, (0, 0, 0))
        quit_text = button_font.render("Quit", True, (0, 0, 0))

        play_again_rect = pygame.Rect(screen.get_width() // 2 - 150, 450, 140, 50)
        quit_rect = pygame.Rect(screen.get_width() // 2 + 10, 450, 100, 50)

        game_over_sound = None
        sound_played_time = None
        isPaused = False

        if settings.sfx_enabled:
            sound_path = r'resources/sounds/gameWinBGM.mp3' if ifWon else r'resources/sounds/gameOverBGM.mp3'
            game_over_sound = mixer.Sound(sound_path)
            game_over_sound.play()
            sound_played_time = pygame.time.get_ticks()

        waiting = True
        while waiting:
            screen.blit(gameOverBackground, (0, 0))
            screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
            screen.blit(win_or_lose_text, (screen.get_width() // 2 - win_or_lose_text.get_width() // 2, 235))
            screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 330))
            screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 380))


            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, (120, 227, 235) if play_again_rect.collidepoint(mouse_pos) else (140, 247, 255), play_again_rect)
            pygame.draw.rect(screen, (235, 80, 80) if quit_rect.collidepoint(mouse_pos) else (255, 100, 100), quit_rect)
            screen.blit(play_again_text, (play_again_rect.x + 5, play_again_rect.y + 15))
            screen.blit(quit_text, (quit_rect.x + 25, quit_rect.y + 15))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()

                    elif event.key == pygame.K_s:
                        settings.sfx_enabled = not settings.sfx_enabled                         
                        if not settings.sfx_enabled and game_over_sound:
                            game_over_sound.stop()

                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        return True

                    elif event.key == pygame.K_p:
                        isPaused = True
                        while isPaused:
                            screen.blit(gameOverBackground, (0, 0))
                            pause_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 50)
                            pause_text = pause_font.render("Paused", True, (133, 255, 253))
                            inner_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 25)
                            inner_text = inner_font.render("Press P to Unpause", True, (255, 255, 255))
                            screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, 250))
                            screen.blit(inner_text, (screen.get_width() // 2 - inner_text.get_width() // 2, 325))
                            pygame.display.update()

                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif pause_event.type == pygame.KEYDOWN:
                                    if pause_event.key == pygame.K_p:
                                        pausesound = mixer.Sound(r'resources/sounds/pause.wav').play()
                                        isPaused = False
                                        # toggle_mute()
                                    elif pause_event.key == pygame.K_m:
                                        toggle_mute()
                                    elif pause_event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.key == pygame.K_RETURN:
                                        pygame.mixer.music.unpause()
                                        return True

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(mouse_pos):
                        pygame.mixer.music.unpause()
                        return True
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        return False

            if sound_played_time and pygame.time.get_ticks() - sound_played_time >= game_over_sound.get_length() * 1000:
                sound_played_time = None


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

    player_blink = False
    player_blink_start_time = 0
    player_invincible_duration = 1000  
    isPaused = False
    start_timer = pygame.time.get_ticks()
    maxTimeLimit = 120 
    pause_time = 0
    pause_start_time = None
    bullet_state = True

    while running:
        clock.tick(60)
        if not isGameOver:
            if allEnemiesDead():
                isWon = bossFight.main_boss_fight()
                # isWon = True
                isGameOver = True
            screen.fill((14, 8, 22))  # RGB
            screen.blit(background, (0, 0))

            if isPaused:
                if pause_start_time is None:
                    pause_start_time = pygame.time.get_ticks()
                # pause_time += pygame.time.get_ticks() - pause_start_time
                # pause_start_time = pygame.time.get_ticks()
                pause_font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 50)
                pause_text = pause_font.render("Paused", True, (133, 255, 253))
                pause_font_inner = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 25)
                pause_text_inner = pause_font_inner.render("Press P to Unpause", True, (255, 255, 255))
                
                screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
                screen.blit(pause_text_inner, (screen.get_width() // 2 - pause_text_inner.get_width() // 2, screen.get_height() // 2 + pause_text.get_height() // 2 + 15))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p: 
                            pausesound = mixer.Sound(r'resources/sounds/pause.wav').play()
                            isPaused = not isPaused
                            if pause_start_time is not None:
                                pause_time += pygame.time.get_ticks() - pause_start_time
                            pause_start_time = None

                        elif event.key == pygame.K_m:
                            toggle_mute()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                continue


            drawBunkers()

            drawEnemies()

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_timer - pause_time) // 1000  

            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Time Left: {maxTimeLimit - elapsed_time}", True, (166, 134, 240))
            screen.blit(timer_text, (10, 40))

            if maxTimeLimit - elapsed_time <= 0:
                isGameOver = True
                isWon = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()
                    if event.key == pygame.K_p: 
                        isPaused = not isPaused
                        pausesound = mixer.Sound(r'resources/sounds/pause.wav').play()
                        # toggle_mute()
                    if event.key == pygame.K_s:
                        settings.sfx_enabled = not settings.sfx_enabled                     
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        playerX_change -= PLAYER_SPEED
                    elif event.key == pygame.K_RIGHT:
                        playerX_change += PLAYER_SPEED
                    if event.key == pygame.K_UP:
                        playerY_change -= PLAYER_SPEED
                    elif event.key == pygame.K_DOWN:
                        playerY_change += PLAYER_SPEED
                    if event.key == pygame.K_SPACE:
                        if bullet_state:
                            fire_bullet(playerX, playerY)
                            bullet_state = False
                            if settings.sfx_enabled:
                                mixer.Sound(r'resources\sounds\laser2.wav').play()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        playerY_change = 0
            
            for bullet in player_bullets[:]:  
                bullet['y'] -= BULLET_SPEED
                screen.blit(bulletImage, (bullet['x'], bullet['y']))

                if bullet['y'] < 0:
                    player_bullets.remove(bullet)
                    bullet_state = True
                    
                collided_enemy = isCollision(bullet['x'], bullet['y'])
                if collided_enemy:
                    if settings.sfx_enabled:
                        mixer.Sound(r'resources/sounds/explosion.wav').play()
                    collided_enemy['lives'] -= 1
                    if collided_enemy['lives'] <= 0:
                        collided_enemy['alive'] = False
                        enemyAliveLocations[collided_enemy['x_pos']][collided_enemy['y_pos']] = 0
                        score_value += 1
                    player_bullets.remove(bullet)
                    bullet_state = True

                hit_bunker = isBunkerHit(bullet['x'], bullet['y'])
                if hit_bunker:
                    if settings.sfx_enabled :
                        mixer.Sound(r'resources\sounds\explosion.wav').play()
                    hit_bunker['health'] -= 1
                    player_bullets.remove(bullet)
                    bullet_state = True

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
            if player_blink:
                if (curr_time - player_blink_start_time) < player_invincible_duration:
                    # Blink: Show player every few frames
                    if (curr_time // 100) % 2 == 0:
                        player(playerX - 20, playerY + 10)  # visible
                    # else: invisible this frame
                else:
                    player_blink = False  # End blink
                    player(playerX - 20, playerY + 10)
            else:
                player(playerX - 20, playerY + 10)

            if bulletY <= 0:
                bulletY = playerY

            curr_time = pygame.time.get_ticks()

            for bullet in enemy_bullets[:]:
                bullet['y'] += BULLET_SPEED
                screen.blit(enemyBulletImage, (bullet['x'], bullet['y']))

                hit_bunker = isBunkerHit(bullet['x'], bullet['y'])
                if hit_bunker:
                    if settings.sfx_enabled :
                        mixer.Sound(r'resources\sounds\explosion.wav').play()
                    hit_bunker['health'] -= 1
                    enemy_bullets.remove(bullet)

                if isPlayerHit(bullet['x'], bullet['y'], playerX - 20, playerY + 10):
                    if not player_blink:
                        player_blink = True
                        player_blink_start_time = curr_time
                    if settings.sfx_enabled :
                        mixer.Sound(r'resources\sounds\explosionWarning.mp3').play()
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

                if EnemyColStillAlive:
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()
                    if event.key == pygame.K_p: 
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    if event.key == pygame.K_s: 
                        settings.sfx_enabled = not settings.sfx_enabled                     
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        
            restart = gameOver(True if isWon else False, score_value, maxTimeLimit - elapsed_time, noOfLives)
            if restart:
                isGameOver = False
                running = True
                noOfLives = 3
                score_value = 0
                playerX = 375
                playerY = 500
                playerX_change = 0
                playerY_change = 0
                bulletX = 0
                bulletY = 0
                enemy_bullets.clear()
                start_timer = pygame.time.get_ticks()

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
            pygame.display.update()
        
# main_game()