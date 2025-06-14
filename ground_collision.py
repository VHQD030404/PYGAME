def check_collision(self,tiles):
    return [tile for tile in tiles if self.rect.colliderect(tile.rect)]
def in_collision_x (self, tiles):
    colliders=check_collision(self,tiles)
    for obj in colliders:
        if self.rect.colliderect(obj.rect):
            if self.velocity.x>0:
                self.rect.right=obj.rect.left
            elif self.velocity.x<0:
                self.rect.left=obj.rect.right
                self.velocity.x = 0 #DỪNG DI CHUYỂN
def in_collision_y (self, tiles):
    colliders=check_collision(self,tiles)
    for obj in colliders:
        if self.rect.colliderect(obj.rect):
            if self.velocity.y<0:
                self.rect.top = obj.rect.bottom
                self.velocity.y=0
                #pygame.time.delay(500)
            if self.velocity.y>0:
                self.rect.bottom = obj.rect.top #ĐẶT NV LÊN NỀN
                self.velocity.y = 0 #DỪNG DI CHUYỂN CHIỀU DỌC
                self.isGrounded=True