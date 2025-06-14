import pygame
from setting import cd_is_over

class Animator:
    def __init__(self, animations_data: dict, scale_factor=1, animation_speed=800):
        """
        animations_data: dict dạng { "state": ("path", frame_count) }
        animation_speed: tổng thời gian để chạy hết 1 animation (ms)
        """
        self.scale_factor = scale_factor
        self.animation_speed = animation_speed
        self.animations = {}
        self.state = 'idle'
        self.load_animations(animations_data)
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.avatar = self.animations[self.state][0]
        self.frame_w = 31
        self.frame_h = 31
        self.dead_animation_played = False

    def load_animations(self, data):
        for state, (path, number_frame) in data.items():
            self.animations[state] = self.load_frames(path, number_frame)

    def load_frames(self, path, number_frame):
        """load the image sheet of animation from PATH and cut it to a list with NUMBER_FRAME of frame, 
        scale your character and all frame if your scale_factor is different 1"""
        
        sprite_sheet = pygame.image.load(path)
        self.frame_w = sprite_sheet.get_width() // number_frame
        self.frame_h = sprite_sheet.get_height()
        list_frame = [sprite_sheet.subsurface((i*self.frame_w, 0, self.frame_w, self.frame_h)) for i in range(number_frame)]
        if self.scale_factor != 1:
            list_frame = [pygame.transform.scale(frame, (self.frame_w * self.scale_factor, self.frame_h * self.scale_factor))
                          for frame in list_frame]
        return list_frame

    def play_animate(self, velocity_x):
        """this need to put in running loop game"""
        if self.state == 'dead' and self.dead_animation_played:
            return # Nếu animation dead đã chạy xong thì không làm gì cả
        if cd_is_over(self.last_update, self.animation_speed // len(self.animations[self.state])):
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            # Nếu là animation dead và đã đến frame cuối
            if self.state == 'dead' and self.frame_index == len(self.animations[self.state]) - 1:
                self.dead_animation_played = True
            if velocity_x < 0:
                self.avatar = pygame.transform.flip(self.animations[self.state][self.frame_index], True, False)
            else:
                self.avatar = self.animations[self.state][self.frame_index]
            self.last_update = pygame.time.get_ticks()

    def get_avatar(self):
        return self.avatar
