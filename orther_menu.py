import sys
import pygame
import os
from setting import WIDTH, HEIGHT
from sound_manager import SoundManager
BLACK =(0,0,0,0)
WHITE=(255,255,255)
BGCOLOR=(25, 117, 30)
BUTTON_COLOR = (25,40,30)
BUTTON_HOVER_COLOR = (147, 186, 0)
SLIDER_COLOR = (150, 150, 150)
SLIDER_HANDLE_COLOR = (200, 200, 200)
START_WIDTH = 1024
START_HEIGHT = 1024
os.environ['SDL_VIDEO_CENTERED'] = '1'

sound_manager = SoundManager()
def init_audio():
    sound_manager.load_music("assets/sound/game-music.mp3")
    sound_manager.load_sound("button_click", "assets/sound/mouse-click.mp3")
    sound_manager.play_music()

def draw_text(text, size, color, x, y, screen):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
class Button:
    def __init__(self, x, y, width, height, text, action=None, sound_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.sound_manager = sound_manager

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BGCOLOR, self.rect, 2, border_radius=10)

        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                self.action()
            return True
        return False

"""KHỞI TẠO START MENU"""
def show_start_screen(screen):
    # Tạo cửa sổ start menu với kích thước riêng
    start_screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT))
    # Load ảnh nền cho start menu

    background = pygame.image.load("assets/images/bg_menu_start.png")
    background = pygame.transform.scale(background, (START_WIDTH, START_HEIGHT))

    # Load logo game

    logo = pygame.image.load("assets/images/logo.png")  # Thay bằng đường dẫn logo của bạn
    logo_rect = logo.get_rect(center=(START_WIDTH // 2, START_HEIGHT // 4 + 100))
    # Tạo các nút
    start_button = Button(START_WIDTH//2 - 100, START_HEIGHT//2 + 100, 200, 60, "START")
    quit_button = Button(START_WIDTH//2 - 100, START_HEIGHT//2 + 200, 200, 60,  "QUIT")
    buttons = [start_button, quit_button]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for button in buttons:
                button.check_hover(mouse_pos)
                if button.handle_event(event):
                    if button == start_button:
                        # Khi bắt đầu game, trả về cửa sổ với kích thước game chính
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        sound_manager.play_sound("button_click")
                        sound_manager.stop_music()
                        return True
                    if button == quit_button:
                        sound_manager.play_sound("button_click")
                        pygame.quit()
                        sys.exit()
                        return False


        # Vẽ
        screen.blit(background, (0, 0))
        # Vẽ logo
        if logo:
            screen.blit(logo, logo_rect)
        # Vẽ các nút
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return True

def show_pause_screen(screen):
    pause_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    replay_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 60, "REPLAY")
    resume_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, "RESUME")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 60, "QUIT")
    buttons = [replay_button, resume_button, quit_button]
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for button in buttons:
                button.check_hover(mouse_pos)
                if button.handle_event(event):
                    if button == replay_button:
                        sound_manager.play_sound("button_click")
                        return "replay"
                    if button == resume_button:
                        sound_manager.play_sound("button_click")
                        return "resume"
                    if button == quit_button:
                        sound_manager.play_sound("button_click")
                        return "menu"
        pause_screen.fill(BGCOLOR)
        draw_text("PAUSE", 100, WHITE, WIDTH // 2, HEIGHT // 4, pause_screen)
        # Vẽ các nút
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return "resume"
def show_game_over_screen(screen):
    sound_manager.play_sound("game_over")
    background = pygame.image.load("assets/images/gameover.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    replay_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 60, "REPLAY")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 , 200, 60, "QUIT")
    buttons = [replay_button, quit_button]
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for button in buttons:
                button.check_hover(mouse_pos)
                if button.handle_event(event):
                    if button == replay_button:
                        sound_manager.play_sound("button_click")
                        return "replay"
                    if button == quit_button:
                        sound_manager.play_sound("button_click")
                        return "menu"
        screen.blit(background, (0, 0))
        # Vẽ các nút
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return "menu"