import pygame
import random
import math
from typing import List

# Khởi tạo Pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Cửa sổ game
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dust Particle with Object Pooling")

class DustParticle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 0
        self.y = 0
        self.size = 0
        self.color = WHITE
        self.speed = 0
        self.angle = 0
        self.lifetime = 0
        self.alpha = 0
        self.active = False
        
    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(1, 3)
        self.color = random.choice([GRAY, LIGHT_GRAY])
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, math.pi * 2)
        self.lifetime = random.randint(30, 100)
        self.alpha = 255
        self.active = True
        
    def update(self):
        if not self.active:
            return
            
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / 100))
        
        if self.lifetime <= 0:
            self.active = False
            
    def draw(self, surface):
        if not self.active:
            return
            
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            particle_surface, 
            (*self.color, self.alpha),
            (self.size, self.size), 
            self.size
        )
        surface.blit(particle_surface, (self.x - self.size, self.y - self.size))

class ParticlePool:
    def __init__(self, size):
        self.pool: List[DustParticle] = [DustParticle() for _ in range(size)]
        self.size = size
        
    def get_particle(self, x, y):
        for particle in self.pool:
            if not particle.active:
                particle.spawn(x, y)
                return particle
        # Nếu hết particle trong pool, tạo thêm (hoặc không làm gì)
        return None
        
    def update(self):
        for particle in self.pool:
            particle.update()
            
    def draw(self, surface):
        for particle in self.pool:
            particle.draw(surface)
            
    def active_count(self):
        return sum(1 for p in self.pool if p.active)

# Tạo pool với 1000 hạt
particle_pool = ParticlePool(1000)

# Vòng lặp chính
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for _ in range(5):
                particle_pool.get_particle(event.pos[0], event.pos[1])
    
    # Tạo hạt ngẫu nhiên
    if random.random() < 0.3:
        particle_pool.get_particle(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        )
    
    particle_pool.update()
    particle_pool.draw(screen)
    
    # Hiển thị số hạt đang active (debug)
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Active particles: {particle_pool.active_count()}", True, WHITE)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()