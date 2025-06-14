import pygame
from setting import *
from pygame.math import Vector2
from animations import Animator
from ground_collision import in_collision_x, in_collision_y
from setting import cd_is_over
from level import *
from sound_manager import SoundManager
class player:
    """create a player with default moving input method and animation |
    x and y is the topleft position of player when game start,
    the size of player depend on size of .png image on animation and scale factor"""
    
    def __init__(self, x, y, scale_factor=2,move_speed=350, sound_manager=None):
        
        self.frame_w = 31 #self.sprite_sheet.get_width() // self.num_frames
        self.frame_h = 31 #self.sprite_sheet.get_height()
        self.scale_factor=scale_factor
        self.rect=pygame.Rect(x, y, 15*scale_factor, 25*scale_factor)
        
        self.animation_speed=700
        self.animator=Animator({
            "idle": ("assets/images/idle.png", 2),
            "walk": ("assets/images/walk.png", 8),
            "jump": ("assets/images/jump.png", 4),
            "fall": ("assets/images/fall.png", 4),
            "dead": ("assets/images/dead.png", 8)}
            , scale_factor, self.animation_speed)
        
        #PlaYER moVEment VAriaAble
        self.move_speed=move_speed
        self.velocity=Vector2(0,0)
        self.gravity=2500
        self.jump_force=-900
        self.isGrounded=False
        self.knockback_timer=0
        self.is_knock_back=False
        self.max_hp = 10
        self.hp = self.max_hp
        self.isAlive = True
        self.last_hitted = pygame.time.get_ticks()
        # âm thanh
        self.sound_manager = sound_manager if sound_manager else SoundManager()
        self._init_player_sounds()
        # hiệu ứng khi mất máu
        self.hit_flash = False
        self.hit_flash_timer = 0
        self.hit_flash_duration = 50  # Thời gian nhấp nháy (ms)
        self.hit_flash_interval = 20  # Khoảng thời gian giữa các lần nhấp nháy (ms)
        self.visible = True
        self.invincible = False  # Trạng thái bất tử tạm thời
        self.invincible_time = 0
        self.invincible_duration = 100
    def get_health(self):
        return f"{self.hp}/{self.max_hp}"
    def _init_player_sounds(self):
        """Khởi tạo tất cả âm thanh cho player"""
        self.sound_manager.load_sound("jump", "assets/sound/jump.mp3")
        self.sound_manager.load_sound("hurt", "assets/sound/hurt.mp3")
        self.sound_manager.load_sound("dead", "assets/sound/dead.mp3")
    def update_moving (self,grounds,d_time):
        if not self.isAlive and self.animator.dead_animation_played:
            return
        if self.rect.y > HEIGHT and self.isAlive:
            self.die()
            return
        self.velocity.x=0
        self.moving()
        self.update_flash_effect(d_time)
        #GRAVITY
        self.velocity.y += self.gravity*d_time
        self.update_knockback(d_time)

        """UPDATE MOVING AND COLLISION"""
        self.rect.x += int(self.velocity.x)*d_time
        in_collision_x(self, grounds)
        self.rect.y += int(self.velocity.y)*d_time
        in_collision_y(self, grounds)
        """limit moving"""
        if self.rect.left<=0 and self.velocity.x<0:
            self.rect.left=0
        elif self.rect.right>=WIDTH and self.velocity.x>0:
            self.rect.right=0
        if self.rect.bottom>HEIGHT:
            self.rect.bottom=HEIGHT
            self.velocity.y=-1
        """ANIMATION CONDITION AND UPDATE"""
        if not self.isAlive:
            self.animator.state = "dead"
            self.animator.play_animate(0)
            return
        elif self.isGrounded and self.velocity.x == 0:
            self.animator.state = "idle"
            # print("idle")
        elif self.velocity.y < 0:
            self.animator.state = "jump"
            # print("jumping")
        elif self.velocity.y > 0:
            self.animator.state = 'fall'
            # print("falling")
        self.animator.play_animate(self.velocity.x)
    """MOVING AND GROUND COLLISION"""
    def moving (self):
        """this need to put in running loop game"""
        key_in=pygame.key.get_pressed()
        self.velocity.x=0
        #JUMPING
        if key_in[pygame.K_SPACE] and self.isGrounded:
            self.sound_manager.play_sound("jump")
            self.velocity.y = self.jump_force
            self.isGrounded = False
        # extra jump
        if key_in[pygame.K_k] and self.isGrounded:
            self.sound_manager.play_sound("jump")
            self.velocity.y = self.jump_force * 2
            self.isGrounded = False
        # MOVING
        if key_in[pygame.K_LEFT] or key_in[pygame.K_a]:
            self.velocity.x = -self.move_speed  # sang trái
            self.animator.state = "walk"
            # print(self.move_speed)
        if key_in[pygame.K_RIGHT] or key_in[pygame.K_d]:
            self.velocity.x = self.move_speed  # sang phải
            self.animator.state = "walk"
            # print(self.move_speed)
            
    """OTHER GAME OBJECT COLLISION"""
    def update_flash_effect(self, d_time):
        """Cập nhật hiệu ứng nhấp nháy khi bị đánh"""
        if self.hit_flash:
            self.hit_flash_timer += d_time * 100
            self.invincible_time += d_time * 100

            # Chuyển trạng thái hiển thị
            if (self.hit_flash_timer // self.hit_flash_interval) % 2 == 0:
                self.visible = False
            else:
                self.visible = True

            # Kết thúc hiệu ứng
            if self.invincible_time >= self.invincible_duration:
                self.hit_flash = False
                self.visible = True
                self.invincible = False
                self.hit_flash_timer = 0
                self.invincible_time = 0
    def update_knockback(self,d_time):
        if self.is_knock_back:
            """VÀO ĐÂY ĐỂ SET THỜI GIAN BỊ KNOCKBACK"""
            if self.knockback_timer<.1:
                #pygame.time.wait(100) #hitstop time
                self.velocity.x-=self.move_speed*d_time*100
                #self.velocity.y=0
                self.velocity.y=-8*self.gravity*d_time
                self.knockback_timer+=d_time
            else:
                self.is_knock_back=False
                self.knockback_timer=0
    def in_check_hit (self, group):
        """RETURN THE OBJECT TYPE.
        *this need to put in running loop game"""
        for obj in group:
            if self.rect.colliderect(obj.rect):
                return obj.type  # trả về loại đối tượng bị va chạm
        return None  # k va chạm
    
    def update_hit(self, gameobjects, entrances): #xử lý va chạm
        """this need to put in running loop game"""
        collision_type = self.in_check_hit(gameobjects)
        current_time = pygame.time.get_ticks()
        for obj in gameobjects:
            if self.rect.colliderect(obj.rect):
                if obj.type == "enemy":
                    if current_time - self.last_hitted > self.invincible_duration:
                        print("Bị quái vật tấn công", current_time)
                        self.is_knock_back = True
                        self.sound_manager.play_sound("hurt")
                        self.take_damage(1)
                        self.last_hitted = current_time
                elif obj.type == "hazard":
                    print("Chết", current_time)
                    self.animator.state = 'dead'
                    self.sound_manager.play_sound("dead")
                    self.isAlive = False
                    self.velocity.x = 0
                    self.velocity.y = 0
        for entrance in entrances:
            if self.rect.colliderect(entrance.rect):
                pygame.event.post(pygame.event.Event(CHANGE_LV_EVT, {"index":entrance.index}))
                break
                #print(f"collide entrance number {entrance.index}")

    def take_damage(self, amount):
        """Giảm máu khi bị tấn công"""
        if self.invincible:
            return  # Đang bất tử, bỏ qua sát thương
        self.sound_manager.play_sound("dead")
        self.hp = max(0, self.hp - amount)
        self.hit_flash = True
        self.hit_flash_timer = 0
        self.visible = False  # ban đầu ẩn ngay khi bị đánh
        self.invincible = True
        self.invincible_time = 0

        if self.hp <= 0 or self.rect.y > HEIGHT:
            self.isAlive = False
            self.die()

    def die(self):
        """Xử lý khi máu = 0"""
        if not self.isAlive:  # Chỉ thực hiện nếu player còn sống
            self.animator.state = 'dead'
            self.sound_manager.play_sound("dead")
            self.velocity.x = 0
            self.velocity.y = 0
            print("Player đã chết")

            return True  # Trả về True khi player vừa chết
        return False  # Trả về False nếu đã chết trước đó

    def draw_health_bar(self, screen):
        """Vẽ thanh máu của player"""
        # Vị trí thanh máu (phía trên đầu player)
        bar_width = 50
        bar_height = 8
        bar_x = self.rect.x + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 15

        # Tính tỉ lệ máu hiện tại
        health_ratio = self.hp / self.max_hp  # Giả sử max_hp = 10

        # Vẽ nền thanh máu (màu đỏ)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Vẽ phần máu còn lại (màu xanh)
        current_width = bar_width * health_ratio
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_width, bar_height))

        # Vẽ viền thanh máu
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
        # Hiển thị số máu
        font = pygame.font.SysFont(None, 20)
        health_text = font.render(f"{self.hp}/{self.max_hp}", True, (255, 255, 255))
        screen.blit(health_text, (bar_x + bar_width // 2 - health_text.get_width() // 2, bar_y - 15))

    def should_show_game_over(self):
        """Kiểm tra có nên hiển thị Game Over chưa"""
        return not self.isAlive and self.animator.dead_animation_played

    def draw(self, screen):
        if self.visible or not self.hit_flash:  # Chỉ vẽ khi visible hoặc không trong hiệu ứng nhấp nháy
            screen.blit(self.animator.get_avatar(),
                        (self.rect.left - 7 * self.scale_factor, self.rect.top - 6 * self.scale_factor))
            self.draw_health_bar(screen)