import pygame
import random
from abc import ABC, abstractmethod

class Particle(ABC):
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.lifetime = 0
        self.max_lifetime = 0
        self.active = False
        self.size = 1
        self.alpha = 0

    def reset(self, pos, velocity, lifetime, size):
        self.active = True
        self.pos = pos.copy()
        self.velocity = velocity.copy()
        self.lifetime = 0
        self.max_lifetime = lifetime
        self.size = size
        self.alpha = 0

    def update(self, d_time):
        if not self.active:
            return
        self.lifetime += d_time
        if self.lifetime >= self.max_lifetime or self.pos.x < -self.size:
            self.active = False
            return
        self.pos += self.velocity * d_time
        third = self.max_lifetime / 3
        if self.lifetime < third:
            self.alpha = min(255, self.alpha + 100 * d_time / third)
        elif self.lifetime > 2 * third:
            self.alpha = max(0, self.alpha - 100 * d_time / third)

    @abstractmethod
    def draw(self, surface):
        pass

class DustParticle(Particle):
    def reset(self, pos):
        velocity = pygame.Vector2(random.uniform(-20, 20), random.uniform(-20, 20))
        super().reset(pos, velocity, random.uniform(0.5, 1.5), random.randint(1, 2))

    def update(self, d_time):
        if self.active:
            self.velocity += pygame.Vector2(random.uniform(-20, 20), random.uniform(-20, 20)) * d_time
            super().update(d_time)

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, (255, 245, 200, int(self.alpha)),
                             pygame.Rect(int(self.pos.x) - self.size, int(self.pos.y) - self.size, self.size * 2, self.size * 2))
    def point_in_polygon(self, point, polygon):
        x, y = point
        inside = False
        n = len(polygon)
        for i in range(n):
            j = (i - 1) % n
            px, py = polygon[i]
            qx, qy = polygon[j]
            if ((py > y) != (qy > y)) and (x < (qx - px) * (y - py) / (qy - py) + px):
                inside = not inside
        return inside

class SmokeParticle(Particle):
    def __init__(self):
        super().__init__()
        self.image = None

    def reset(self, pos):
        if self.image is None:
            self.image = pygame.image.load("assets/smoke.png").convert_alpha()
        velocity = pygame.Vector2(-100,0)
        super().reset(pos, velocity, 5, 20)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def update(self, d_time):
        if self.active:
            super().update(d_time)
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.image.set_alpha(int(self.alpha))

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect.topleft)

class ParticleSystem:
    def __init__(self, pool_size=50):
        self.particles = [DustParticle() for _ in range(pool_size // 2)] + [SmokeParticle() for _ in range(pool_size // 2)]
        self.types = {"dust": DustParticle, "smoke": SmokeParticle}
        self.dust_timer = 0
        self.smoke_timer = 0
        self.dust_interval = 0.1
        self.smoke_interval = 0.5
        self.dust_polygon = None
        self.smoke_active = False

    def get_particle(self, particle_type):
        for particle in self.particles:
            if not particle.active and isinstance(particle, self.types[particle_type]):
                return particle
        particle = self.types[particle_type]()
        self.particles.append(particle)
        return particle

    def start_dust_effect(self, polygon):
        self.dust_polygon = polygon

    def stop_dust_effect(self):
        self.dust_polygon = None

    def start_smoke_effect(self):
        self.smoke_active = True

    def stop_smoke_effect(self):
        self.smoke_active = False

    

    def spawn_particles(self, particle_type, area, count=20):
        for _ in range(count):
            particle = self.get_particle(particle_type)
            if particle:
                if particle_type == "dust" and isinstance(area, list):
                    min_x, max_x = min(p[0] for p in area), max(p[0] for p in area)
                    min_y, max_y = min(p[1] for p in area), max(p[1] for p in area)
                    pos = pygame.Vector2(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
                    while not particle.point_in_polygon(pos, area):
                        pos = pygame.Vector2(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
                else:  # Rect cho smoke
                    pos = pygame.Vector2(random.randint(area.left, area.right), random.randint(area.top, area.bottom))
                particle.reset(pos)

    def update(self, d_time):
        self.dust_timer += d_time
        self.smoke_timer += d_time
        if self.dust_polygon and self.dust_timer >= self.dust_interval:
            self.spawn_particles("dust", self.dust_polygon)
            self.dust_timer = 0
        if self.smoke_active and self.smoke_timer >= self.smoke_interval:
            self.spawn_particles("smoke", pygame.Rect(0, 180, 1920, 480))
            self.smoke_timer = 0
        for particle in self.particles:
            if particle.active:
                particle.update(d_time)

    def draw(self, surface):
        if self.smoke_active or self.dust_polygon:
            for particle in self.particles:
                if particle.active:
                    particle.draw(surface)