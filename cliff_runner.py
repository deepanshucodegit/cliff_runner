import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        self.gravity=0
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity=-20
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index>=len(self.player_walk):
                self.player_index=0
            self.image=self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type=="fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos=180
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos=300
        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900,1100),y_pos))


    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index>=len(self.frames):
            self.animation_index=0
        self.image=self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x-=4
        self.destroy()

    def destroy(self):
        if self.rect.x<=-100:
            self.kill()




def player_animation():
    global player_surface,player_index
    if player_rect.bottom<300:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index>=len(player_walk):player_index=0
        player_surface=player_walk[int(player_index)]

def obstacle_movement(list):
    if list:
        for rect in list:
            rect.x -= 5
            if rect.bottom==300:
                screen.blit(snail_surface, rect)
            else:
                screen.blit(fly_surface, rect)
        obstacle_rect_list=[obstacle for obstacle in list if obstacle.x>-100]
        return obstacle_rect_list
    else:
        return []

def collision(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:return True
def displayscore():
    current_time=pygame.time.get_ticks()-starttime
    gamescore_surface=gamescore_font.render(f"score: {int(current_time*0.01)}",False,"gold")
    gamescore_rect = gamescore_surface.get_rect(topleft=(0, 0))
    screen.blit(gamescore_surface, gamescore_rect)
    return current_time



#initialization of screen
pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("adventure island 2")
clock=pygame.time.Clock()
game_active=False


player=pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group=pygame.sprite.Group()

#load images
sky_surface=pygame.image.load("graphics/Sky.png").convert()
ground_surface=pygame.image.load("graphics/Ground.png").convert()
#loadfont
gamename_font=pygame.font.Font("font/Pixeltype.ttf",50)
gamescore_font=pygame.font.Font("font/Pixeltype.ttf",50)
#gamescore_surface=gamescore_font.render("SCORE",False,(64,64,64))
gamename_surface=gamename_font.render("adventure island2",False,"black")
#gamescore_rect=gamescore_surface.get_rect(topleft=(0,0))
gameover_font=pygame.font.Font("font/Pixeltype.ttf",60)
gameover_surface=gameover_font.render("Game Over",False,"red")
startagain_font=pygame.font.Font("font/Pixeltype.ttf",60)
startagain_surface=startagain_font.render("press enter to start",False,"gold")
#character loading
snail_surface=pygame.image.load("graphics/snail/snail1.png").convert_alpha()
player_walk_1=pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2=pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_jump=pygame.image.load("graphics/player/jump.png").convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0
snail_frame_1=pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2=pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames=[snail_frame_1,snail_frame_2]
snail_index=0
snail_surface=snail_frames[snail_index]

fly_frame_1=pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2=pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames=[fly_frame_1,fly_frame_2]
fly_index=0
fly_surface=fly_frames[fly_index]

player_surface=player_walk[player_index]
player_rect=player_surface.get_rect(midbottom=(40,300))
fly_surface=pygame.image.load("graphics/fly/fly1.png").convert_alpha()

player_gravity=0
starttime=0
score=0

obstacle_rect_list=[]

#timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,300)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and player_rect.bottom>=290 :
                player_gravity=-20
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                game_active=True
                starttime=pygame.time.get_ticks()
        if game_active:
            if event.type==obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly","snail","snail"])))

            if event.type==snail_animation_timer:
                if snail_index==0:snail_index=1
                else:snail_index=0
                snail_surface=snail_frames[snail_index]
            if event.type==fly_animation_timer:
                if fly_index==0:fly_index=1
                else:fly_index=0
                fly_surface=fly_frames[fly_index]
    if game_active:
        screen.blit(sky_surface,(0,-100))
        #screen.blit(ground_surface, (0, 300))
        #screen.blit()

        displayscore()
        score = displayscore()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active=collision_sprite()

    else:
        screen.fill((94,129,162))
        obstacle_rect_list.clear()
        if score!=0:
            screen.blit(gameover_surface,(290,100))
            score_message = gamescore_font.render(f"your score: {int(score * 0.01)}", False, "green")
            screen.blit(score_message, (260, 160))
        else:
            screen.blit(gamename_surface, (250, 100))
        screen.blit(startagain_surface, (190, 250))
    pygame.display.update()
    clock.tick(60)
