import pygame
import math
import random
from pygame import Vector2
from ground_collision import in_collision_x, in_collision_y
from animations import Animator
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

class GameObject (pygame.sprite.Sprite):
    """create an root rectangular object that has a object type, the object type can be choose from this list: enemy, hazard, deadzone"""
    
    def __init__(self, x, y, width, height, obj_type, color):
        super().__init__()
        self.rect=pygame.Rect(x, y, width, height)
        self.type=obj_type
        self.color=color
        
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class enemy (GameObject):
    
    def __init__(self,x,y,width=20,height=20):
        super().__init__(x, y, width, height, "enemy", RED)
        self.gravity=0
        self.velocity=Vector2(0,0)
        self.movespeed=150
        self.direction = 1
        self.animations_data = {"idle": ("assets/images/Enemy.png", 4)}
        self.animator = Animator(self.animations_data, scale_factor=2, animation_speed=800)
        self.state = "idle"
        # Cập nhật kích thước thực tế dựa trên animation frame
        self.rect.width = self.animator.frame_w * self.animator.scale_factor
        self.rect.height = self.animator.frame_h * self.animator.scale_factor
    def in_moving(self, player, d_time, tiles, view_range=500):
        if abs(self.rect.x - player.rect.x) < view_range:  # neu nam trong pham vi nhin
            # di theo player
            if self.rect.x < player.rect.centerx:
                self.velocity.x = self.movespeed
                self.direction = 1
            elif self.rect.x > player.rect.centerx:
                self.velocity.x = -self.movespeed
                self.direction = -1
        else:
            # di tu nhien
            self.velocity.x = self.movespeed * self.direction

        # update vi tri
        prev_x = self.rect.x
        self.rect.x += int(self.velocity.x * d_time)

        # kt va cham va dao huong di chuyen
        in_collision_x(self, tiles)
        if self.rect.x == prev_x:  # neu cham tile
            self.direction *= -1  # di nguoc lai
            self.velocity.x = self.movespeed * self.direction
        self.gravity = 800  # Tăng dần trọng lực (giống như rơi)
        self.velocity.y = self.gravity
        self.rect.y += int(self.velocity.y * d_time)
        in_collision_y(self, tiles)
        if self.velocity.x == 0:
            self.state = "idle"
        else:
            self.state = "idle"
        self.animator.state = self.state
        self.animator.play_animate(self.velocity.x)
    def draw(self, surface):
        # Thay vì vẽ hình chữ nhật, vẽ animation
        avatar = self.animator.get_avatar()
        surface.blit(avatar, (self.rect.x, self.rect.y))
class hazard (GameObject):

    def __init__(self, x, y, width=100, height=40):
        super().__init__(x, y, width, height, "hazard", (0,0,255,100))

class entrance (GameObject):
    def __init__(self, x, y, index,width= 20, height=200):
        super().__init__(x,y,width,height,"entrance",WHITE)
        self.index=index
class Collectable_items(GameObject):
    def __init__(self, x, y, width=20, height=20):
        super().__init__(x,y,width,height,"heal",GREEN)
        # Tạo surface và image
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Nền trong suốt
        self.heal_amount = 1

        # Hiệu ứng bay lơ lửng
        self.float_offset = 0
        self.float_speed = 0.01
        self.original_y = y

        # Trạng thái
        self.collected = False

    def update(self):
        """Cập nhật hiệu ứng bay lơ lửng"""
        if not self.collected:
            self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * 3
            self.rect.y = self.original_y + self.float_offset

    def draw(self, surface):
        """Vẽ vật phẩm đơn giản không nhấp nháy"""
        if not self.collected:
            # Vẽ hình vuông nền
            pygame.draw.rect(surface, self.color, self.rect)

            # Vẽ dấu "+" trắng
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2
            pygame.draw.line(surface, WHITE, (center_x - 5, center_y), (center_x + 5, center_y), 2)
            pygame.draw.line(surface, WHITE, (center_x, center_y - 5), (center_x, center_y + 5), 2)

    def apply_effect(self, player):
        """Áp dụng hiệu ứng khi nhặt vật phẩm"""
        if (self.collected or
                not hasattr(player, 'hp') or
                not hasattr(player, 'max_hp') or
                player.hp >= player.max_hp):
            return False  # Không thể nhặtx`
        player.hp = min(player.hp + self.heal_amount, player.max_hp)
        self.collected = True
        return True
def generate_collectables(tilemap):
    """Tạo một vật phẩm ngẫu nhiên trên platform"""
    collectables = pygame.sprite.Group()
    platforms = tilemap.get_platforms()

    if not platforms:
        return collectables

    platform = random.choice(platforms)
    all_tile_rects = [tile.rect for tile in tilemap.tiles]
    collectable_width = 20
    collectable_height = 20

    # Random vị trí trên platform
    min_x = platform.rect.left + 10
    max_x = platform.rect.right - 10 - collectable_width
    x = random.randint(min_x, max_x)
    y = platform.rect.top - collectable_height - 5

    # Kiểm tra va chạm
    collectable_rect = pygame.Rect(x, y, collectable_width, collectable_height)
    if not any(collectable_rect.colliderect(tile_rect) for tile_rect in all_tile_rects):
        collectables.add(Collectable_items(x, y))

    return collectables