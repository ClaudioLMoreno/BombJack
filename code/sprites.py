from settings import *
from support import import_image

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display=pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            if hasattr(sprite,'hitbox'):
                self.display.blit(sprite.image,sprite.rect.topleft+vector(-(4*SCALE),0)) 
                pygame.draw.rect(self.display,'white',sprite.hitbox,1)
            else:
                self.display.blit(sprite.image,sprite.rect) 
        
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.image=pygame.transform.scale_by(self.image,SCALE)
        self.rect=self.image.get_frect(center=pos)

class Player(Sprite):
    def __init__(self,pos,groups,collision_sprites):
        surf=import_image(join('../','images','player','player'))
        super().__init__(pos,surf,groups)
        self.collision_sprites=collision_sprites
        self.direction=vector()
        self.speed=80*SCALE
        self.gravity=8*SCALE
        self.jump_speed=-(6*SCALE)
        self.on_floor=False
        self.hitbox=self.rect.inflate(-(7*SCALE),-(SCALE))
    
    def input(self):
        keys=pygame.key.get_pressed()
        keyp=pygame.key.get_just_pressed()
        self.direction.x=(keys[K_d]-keys[K_a])
        
        if keys[K_w]:
            if self.on_floor:
                self.direction.y=self.jump_speed
                self.on_floor=False
                
        if keyp[K_w] and self.direction.y>0:                
            self.direction.y=-(SCALE*.5)  
            
    def move(self,dt):
        # horizontal
        self.hitbox.x+=self.direction.x*self.speed*dt
        self.collision('h')
        
        # vertical
        self.direction.y+=self.gravity*dt
        self.hitbox.y+=self.direction.y
        
        self.collision('v')
        if self.hitbox.bottom>WINDOW_HEIGHT:
            self.on_floor=True
            self.direction.y=0
            self.hitbox.bottom=WINDOW_HEIGHT
            
        if self.on_floor:
            self.direction.y=0
        
        if self.hitbox.left<0:self.hitbox.left=0
        if self.hitbox.right>GAME_WIDTH:self.hitbox.right=GAME_WIDTH
        if self.direction.y>3*SCALE:self.direction.y=3*SCALE
        self.rect.topleft=self.hitbox.topleft

    def collision(self,dir):
        self.on_floor=False
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if dir=='h':
                    if self.direction.x>0:self.hitbox.right=sprite.rect.left
                    if self.direction.x<0:self.hitbox.left=sprite.rect.right
                if dir=='v':
                    if self.direction.y>0:
                        self.hitbox.bottom=sprite.rect.top
                        self.on_floor=True
                    if self.direction.y<0:
                        self.hitbox.top=sprite.rect.bottom
                        self.on_floor=False
                        self.direction.y*=.8
    
    def update(self,dt):
        self.input()
        self.move(dt)        