from tile_map import TileMap
import pygame
from particle import ParticleSystem
from setting import HEIGHT, WIDTH
class Level:
    
    def __init__(self, tilemap_path,size, spawn_points: dict[int: tuple[int, int]]):
        self.tilemap = TileMap(tilemap_path)
        self.spawn_points = spawn_points

    def update(self,d_time,player):
        self.tilemap.update_Obj(d_time, player)

    def draw(self, surface):
        self.tilemap.draw_map(surface)

    def get_tiles(self):
        return self.tilemap.tiles

class LevelManager:
    def __init__(self, level_list, player):
        """level list is a list: tuple(level_path, {spawnpoint_index: (x,y) })"""
        self.level_list = level_list
        self.level_index = 0
        self.player = player
        self.need_refresh=False
        self.load_level(0, spawnpoint_index=1)  # spawn mặc định
    def update(self,d_time):
        self.level.update(d_time, self.player)

    def load_level(self, lvindex, spawnpoint_index):
        """load the level number 'lvindex' in level data and place player to spawnpoint [spawnpoint_index]"""
        #lấy cặp dữ liệu của tuple với path: str, spawnpoints: dict {index_number: (x,y)}
        path, spawn_points = self.level_list[lvindex]
        self.level = Level(path,2, spawn_points)
        self.level_index = lvindex
        self.set_player(spawnpoint_index)
        
    def set_player(self,spawnpoint_index):
        spawn_pos=self.level.spawn_points.get(spawnpoint_index) #-> tuple
        if spawn_pos:
            self.player.rect.topleft=spawn_pos
            self.player.velocity=pygame.Vector2(0,0)
        else:
            pass
            raise ValueError(f"Spawn point '{spawnpoint_index}' not found in level {self.level_index}")


    def go_to_level (self, spawnpoint_index):
        lvindex = self.level_index
        next_spawnpoint=1
        
        if spawnpoint_index==1 or spawnpoint_index==3:
            if self.level_index==0:
                print("dang o level 0, khong con level truoc")
                return
            
            lvindex=self.level_index-1
            next_spawnpoint=spawnpoint_index+1
            
        elif spawnpoint_index==2 or spawnpoint_index==4:
            if self.level_index>=len(self.level_list)-1:
                print("dang o level cuoi, khong con level sau")
                return
            
            lvindex=self.level_index+1
            next_spawnpoint=spawnpoint_index-1
        try:
            self.load_level(lvindex, next_spawnpoint)
            print (f"go to level {lvindex+1} and spawn in spawnpoint number {next_spawnpoint}")
        except:
            print (f"number level {lvindex} and spawn in {next_spawnpoint} ERROR, the final level is {len(self.level_list)}")