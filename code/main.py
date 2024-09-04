from settings import * 
from sprites import *
from support import import_tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),vsync=1)
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites=AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        # self.scr=import_tilemap(13,5,join('../screens','BombJack1'))
        
        # load game
        self.setup()
        self.run()
    
    def setup(self):
        tmx_map=load_pygame(join('../data','maps','level1.tmx'))
        
        # self.back_image=tmx_map.get_layer_by_name('back').image
        self.back_image=pygame.Surface((256,192))
        self.back_image.fill('gray')
        self.back_image=pygame.transform.scale_by(self.back_image,SCALE)
        
        for x,y,image in tmx_map.get_layer_by_name('platforms').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,(self.all_sprites,self.collision_sprites))
            
        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name=='player':
                Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 
            pygame.display.set_caption(f'FPS:{self.clock.get_fps() :.1f}')

            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:self.running=False
                    if event.key==K_TAB:Game()
                    
            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.blit(self.back_image,(0,0))
            self.all_sprites.draw()
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    Game()