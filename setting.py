import pygame
WIDTH, HEIGHT = 1920, 1080 #kích thước window
def cd_is_over (last_time, duration):
    "return True if from last time to now is equal or longer than durration"
    return pygame.time.get_ticks() - last_time >= duration
CHANGE_LV_EVT = pygame.USEREVENT + 1
PLAYER_DEAD_EVT = pygame.USEREVENT + 2
LEVEL_WIN_EVT = pygame.USEREVENT + 3
CHANGE_VFX=pygame.USEREVENT+4
# v.v. thêm sau nếu cần
