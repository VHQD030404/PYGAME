import pygame, csv, os
import random
from gameObjectv2 import enemy
from setting import HEIGHT
from particle import ParticleSystem

enemies=pygame.sprite.Group()
class Tile(pygame.sprite.Sprite):
    def __init__(self, path,x,y,tile_type="ground"):
        super().__init__()
        self.image=pygame.image.load(path)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.type = tile_type

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    

class TileMap:
    def __init__(self, filepath):
        """create a tilemap with map in .csv file in filepath"""
        #tile grid=16 -> tile size =60
        #tile grid = 64 -> tile size = 15
        self.tile_size = 60
        self.start_x, self.start_y = 0, 0
        self.tiles, self.game_objects = self.load_tiles(filepath)

        self.map_surface = pygame.Surface((self.map_w, self.map_h)) #cai nay phai chay sau load tiles
        self.map_surface.set_colorkey((0, 0, 0)) #key mau den của nền
        
        #self.load_map()

    def draw_map(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        for obj in self.game_objects:
            obj.draw(surface)

    def update_Obj(self, d_time, player):
        for obj in self.game_objects:
            if isinstance(obj, enemy):
                obj.in_moving(player, d_time, self.tiles, view_range=500)

    def load_map(self):
        """this just need to load 1 time before game running"""
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filepath):
        map = []
    
        # Kiểm tra file tồn tại
        if not os.path.exists(filepath):
            print(f"Không tìm thấy file: {filepath}")
            return []
        try:
            with open(filepath) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    map.append(list(row))
            print(f"Đọc file: {filepath}")
        except Exception as e:
            print(f"Lỗi khi đọc file {filepath}: {e}")
        
        return map

    def load_tiles(self, filepath):
        tiles = []
        enemies = pygame.sprite.Group()
        map_data = self.read_csv(filepath)
        x, y = 0, 0
        for row in map_data:
            x = 0
            for tile in row:
                if tile == '-1':
                    # nếu tile này không có gì để vẽ thì chỉ tăng x và y chọn đến tile tiếp theo
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '0':
                    tiles.append(Tile("assets/mossyblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '1':
                    tiles.append(Tile("assets/stoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '2':
                    tiles.append(Tile("assets/vineblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '3':
                    tiles.append(Tile("assets/vinevineblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '4':
                    tiles.append(Tile("assets/wetstoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '5':
                    tiles.append(Tile("assets/drystoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '6':
                    tiles.append(Tile("assets/darkstoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '7':
                    tiles.append(Tile("assets/stalactite.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '8':
                    tiles.append(Tile("assets/verywetstoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '9':
                    tiles.append(Tile("assets/middrystoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '10':
                    tiles.append(Tile("assets/mossyvineblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '11':
                    tiles.append(Tile("assets/mossywetstoneblock2.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '12':
                    tiles.append(Tile("assets/mossywetstoneblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '13':
                    tiles.append(Tile("assets/mossysblock.png", x * self.tile_size, y * self.tile_size, "ground"))
                elif tile == '14':
                    enemies.add(enemy(x * self.tile_size, y * self.tile_size, ))
                x += 1
            y += 1
        self.map_w = x * self.tile_size
        self.map_h = y * self.tile_size
        return tiles, enemies
    def get_platforms(self):
        """Lấy danh sách các platform có thể đặt vật phẩm"""
        return [tile for tile in self.tiles if tile.type == "ground"]

    def get_safe_spawn_positions(self, collectable_size=20, padding=10):
        """Lấy các vị trí an toàn để đặt vật phẩm"""
        safe_positions = []

        for tile in self.tiles:
            if tile.type == "ground":  # Chỉ xét các tile platform
                # Tính toán vùng an toàn trên platform
                min_x = tile.rect.left + padding
                max_x = tile.rect.right - padding - collectable_size
                min_y = tile.rect.top - collectable_size - 5  # Bay phía trên platform
                max_y = tile.rect.top - 5

                if max_x > min_x:  # Chỉ thêm nếu có đủ chỗ
                    safe_positions.append({
                        'x_range': (min_x, max_x),
                        'y': random.randint(min_y, max_y),
                        'platform': tile
                    })

        return safe_positions

    def get_all_tiles(self):
        """Trả về danh sách tất cả các tile"""
        return self.tiles