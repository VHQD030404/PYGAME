import pygame
import random
import sys
from playerv2 import player
from setting import *
from gameObjectv2 import entrance, generate_collectables
from level import LevelManager
from orther_menu import show_start_screen, show_pause_screen, show_game_over_screen, init_audio, sound_manager
from vfx import VFXManager
#ĐỊNH NGHĨA CÁC MÀU CẦN DÙNG
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
BGCOLOR=(25,40,30)

CLOCK=pygame.time.Clock()
FPS=100

"""KHỞI TẠO CÁC BIẾN ĐẦU TIÊN"""
icon = pygame.image.load("assets/images/logo.png")
p1=player(60,600)
level_list_data= [
    ("assets/tilemap/lv0.csv",
     {1: (40,HEIGHT-100),
      3: (40,HEIGHT-100),
      2: (WIDTH-80,HEIGHT//2+100),
      4: (WIDTH-80,HEIGHT//2+100)}),
    ("assets/tilemap/lv1.csv",
     {1: (40,HEIGHT//2),
      3: (40,HEIGHT//2),
      2: (WIDTH-40,HEIGHT//2),
      4: (WIDTH-40,HEIGHT//2)}),
    ("assets/tilemap/lv2.csv",
     {1: (40,HEIGHT//2),
      3: (40,HEIGHT//2),
      2: (WIDTH-80,100),
      4: (WIDTH-80,HEIGHT-250)}),
    ("assets/tilemap/lv3.csv",
     {1: (40,HEIGHT//2-100),
      3: (40,HEIGHT//2+150),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv4.csv",
     {1: (50,HEIGHT//2-120),
      3: (60,HEIGHT-160),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv5.csv",
     {1: (50,HEIGHT//2-200),
      3: (40,HEIGHT-200),
      2: (WIDTH-80,150),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv6.csv",
     {1: (50,HEIGHT//2-200),
      3: (40,HEIGHT-250),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT//2+150)}),
    ("assets/tilemap/lv7.csv",
     {1: (40,HEIGHT//2-250),
      3: (40,HEIGHT//2+150),
      2: (WIDTH-80,60),
      4: (WIDTH-80,60)}),
    ("assets/tilemap/lv8.csv",
     {1: (40,HEIGHT-200),
      3: (40,HEIGHT-200),
      2: (WIDTH-80,100),
      4: (WIDTH-80,100)}),
    ("assets/tilemap/lv9.csv",
     {1: (40,HEIGHT-200),
      3: (40,HEIGHT-200),}),
    ]
levelmanager=LevelManager(level_list_data, p1)
#levelmanager.load_level(1, 1) #DEBUG LEVEL
entrances=pygame.sprite.Group()
entrances.add(
    entrance(-40, 0, 1, 50, HEIGHT//2),
    entrance(-40, HEIGHT//2, 3, 50, HEIGHT//2),
    entrance(WIDTH-10, 0, 2,50,HEIGHT//2),
    entrance(WIDTH-10, HEIGHT//2, 4,50,HEIGHT//2)
    )
vfxmanager=VFXManager()

"""KHỞI TẠO ĐẦU TIÊN"""
pygame.init()
pygame.mixer.init()
init_audio()
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAVE ADVENTURE")
mouse_pos = pygame.mouse.get_pos()
font = pygame.font.SysFont(None, 48)
collectables = generate_collectables(levelmanager.level.tilemap)
game_active = True
paused=False
bg1 = pygame.image.load("assets/bgIMG.png").convert()
bg9 = pygame.image.load("assets/endBG.png").convert()
"""VÒNG LẶP GAME"""
if not show_start_screen(screen):
    running = False
else:
    running = True
    sound_manager.load_music("assets/bgm/hangSonDoongBGM.mp3")
    sound_manager.play_music()
while running:
    
    d_time=d_time = CLOCK.tick(FPS)/1000
    #print(d_time) #SHOW DELTA TIME TO DEBUG
    screen.fill(BGCOLOR)
    if levelmanager.level_index==0:
        screen.blit(bg1, (0, 0))
    elif levelmanager.level_index==9:
        screen.blit(bg9, (0,0))
    for event in pygame.event.get():
            # Nhấn ESC để pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               paused = True
        elif event.type == CHANGE_LV_EVT:
            levelmanager.go_to_level(event.index)
            collectables = generate_collectables(levelmanager.level.tilemap)
        if event.type == CHANGE_VFX:
            levelmanager.level.tilemap
        if event.type == pygame.QUIT:
            running = False

    if p1.isAlive:
        for item in collectables:
            item.draw(screen)
        for en in entrances:
            pass  # en.draw(screen) #để debug
        p1.draw(screen)
        vfxmanager.update(d_time, levelmanager.level_index)
        vfxmanager.draw(levelmanager.level_index, screen)
        levelmanager.level.draw(screen)
        if paused:
            result = show_pause_screen(screen)
            if result == "resume":
                paused = False
            elif result == "menu":
                sound_manager.play_music()
                # Quay về menu chính
                if show_start_screen(screen):
                    p1.isAlive = True
                    p1 = player(0, 0)
                    collectables = generate_collectables(levelmanager.level.tilemap)
                    levelmanager = LevelManager(level_list_data, p1)
                else:
                    running = False
            elif result == "replay":
                p1.isAlive = True
                p1 = player(0, 0)  # Tạo player mới
                levelmanager = LevelManager(level_list_data, p1)
                # Reset level manager
                collectables = generate_collectables(levelmanager.level.tilemap)
                paused = False
        else:
            p1.update_moving(levelmanager.level.get_tiles(), d_time)
            p1.update_hit(levelmanager.level.tilemap.game_objects, entrances)
            levelmanager.level.update(d_time, p1)
            if p1.should_show_game_over():
                sound_manager.stop_music()
                p1.isAlive = False
        collided_items = pygame.sprite.spritecollide(p1, collectables, False)
        for item in collectables:
            if pygame.sprite.collide_rect(p1, item):
                if item.apply_effect(p1):
                    collectables.remove(item)
    else:
        result = show_game_over_screen(screen)
        if result == "replay":
            # Reset game
            p1.isAlive = True
            p1 = player(0, 0)  # Tạo player mới
            levelmanager = LevelManager(level_list_data, p1)
            paused = False
        elif result == "menu":
            sound_manager.play_music()
            # Quay về menu chính
            if show_start_screen(screen):
                p1.isAlive = True
                p1 = player(0, 0,)
                levelmanager = LevelManager(level_list_data, p1)
                paused = False
            else:
                running = False
    collectables.update()
    #pygame.draw.rect(screen, WHITE, p1.rect) #SHOW HITBOX
    pygame.display.update() #update màn hình

pygame.quit()
sys.exit()