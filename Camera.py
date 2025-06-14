import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)

        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.MAP_W, self.MAP_H = 1920, 1080  # Kích thước map

        self.CONST = vec(
            -self.DISPLAY_W / 2 + player.rect.width / 2,
            -self.DISPLAY_H / 2 + player.rect.height / 2
        )

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()
class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        super().__init__(camera, player)

    def scroll(self):
        # Tính offset mượt bằng float trước
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)

        # Giới hạn offset theo kích thước map
        self.camera.offset_float.x = max(0, min(self.camera.offset_float.x, self.camera.MAP_W - self.camera.DISPLAY_W))
        self.camera.offset_float.y = max(0, min(self.camera.offset_float.y, self.camera.MAP_H - self.camera.DISPLAY_H))

        self.camera.offset = self.camera.offset_float.elementwise().int()
