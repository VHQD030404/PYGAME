import pygame
from particle import ParticleSystem
from setting import HEIGHT, WIDTH
SUNLIGHTCOLOR=(255, 255, 180, 40)
class VFXManager:
    def __init__(self):
        self.particle_system = ParticleSystem(pool_size=50)
        self.sunlight_polygon1 = [(1260, 0), (WIDTH, 0), (600, HEIGHT), (-500, HEIGHT)]
        self.sunlight_polygon2 = [(1260, 0), (1680, 0), (1440, HEIGHT), (840, HEIGHT)]
        self.sunlight = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def update(self, d_time, lvindex):
        """Cập nhật particle system dựa trên level index"""
        if lvindex == 1:
            self.particle_system.start_smoke_effect()
            self.particle_system.update(d_time)
        elif lvindex in [7, 8]:
            self.particle_system.start_dust_effect(self.sunlight_polygon1)
            self.particle_system.update(d_time)
        elif lvindex == 9:
            self.particle_system.start_dust_effect(self.sunlight_polygon2)
            self.particle_system.update(d_time)
        else:
            self.particle_system.stop_smoke_effect()
            self.particle_system.stop_dust_effect()
            self.particle_system.update(d_time)

    def draw(self, lvindex, surface):
        """Vẽ ánh nắng và particle dựa trên level index"""
        if lvindex in [7, 8]:
            self.sunlight.fill((0, 0, 0, 0))
            pygame.draw.polygon(self.sunlight, SUNLIGHTCOLOR, self.sunlight_polygon1)
            surface.blit(self.sunlight, (0, 0))
        elif lvindex == 9:
            self.sunlight.fill((0, 0, 0, 0))
            pygame.draw.polygon(self.sunlight, (255, 255, 180, 40), self.sunlight_polygon2)
            surface.blit(self.sunlight, (0, 0))
        self.particle_system.draw(surface)