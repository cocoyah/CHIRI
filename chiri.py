import pygame
from sys import exit
from pygame.sprite import Group

# def draw_grid():
#     for line in range(0, 16):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        
        #mouse pos
        pos = pygame.mouse.get_pos()

        #mouseover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def walk_animation(self):
        walk_cooldown = 0
        
        if self.counter > walk_cooldown:
            self.counter = 0
            self.player_index += 1
            if self.player_index >= len(self.player_right):
                self.player_index = 0
            if self.direction == 1:
                self.image = self.player_right[self.player_index]
            if self.direction == -1:
                self.image = self.player_left[self.player_index]
        else:
            self.idle_animation()
    
    def idle_animation(self):
        self.player_idle_index += 0.5
        if self.player_idle_index >= len(self.player_idle_list):
            self.player_idle_index = 0
        if self.direction == 1:
            self.image = self.player_idle_list[int(self.player_idle_index)]
        if self.direction == -1:
            self.image = self.player_idle_left_list[int(self.player_idle_index)]
    
    def jump_animation(self):
        jump_cooldown = 0

        if self.vel_y != 0:
            if self.vel_y > 0:
                if self.direction == 1:
                    self.image = self.player_jump_right_list[self.player_jump_index]
                elif self.direction == -1:
                    self.image = self.player_jump_left_list[self.player_jump_index]
            else:
                if self.direction == 1:
                    self.image = self.player_jump_right_list[0]
                elif self.direction == -1:
                    self.image = self.player_jump_left_list[0]

            if self.counter > jump_cooldown:
                self.counter = 0
                self.player_jump_index += 1
                if self.player_jump_index >= len(self.player_jump_right_list):
                    self.player_jump_index = 0

            if self.vel_y >= 0:
                self.jumped = False
        else:
            self.idle_animation()

    def update(self, game_over):

        self.dx = 0
        dy = 0

        if game_over == 0:
            #keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
                self.player_jump_index = 0
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                self.counter += 1
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                self.dx -= 5
                self.counter += 1 
                self.direction  = -1
            if key[pygame.K_RIGHT]:
                self.dx += 5
                self.counter += 1
                self.direction  = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.player_index = 0

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision with screen boundaries
            if self.rect.left + self.dx < 0:
                self.rect.left = 0
            if self.rect.right + self.dx > screen_width:
                self.rect.right = screen_width
            if self.rect.top + dy < 0:
                self.rect.top = 0
            if self.rect.bottom + dy > screen_height:
                self.rect.bottom = screen_height
                dy = 0

            #check for collision
            self.in_air = True
            for tile in map.tile_list:
                #collision x direction
                if tile[1].colliderect(self.rect.x + self.dx , self.rect.y, self.width, self.height):
                    self.dx = 0
                #collision y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom -self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top -self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                    
            #collision with obstacles
            if pygame.sprite.spritecollide(self, rock_group, False):
                game_over = -1

            #collision with water
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1

            tree_collision = pygame.sprite.spritecollide(self, tree_group, False)
            if tree_collision:
                for tree in tree_collision:
                    if self.dx > 0:  # Moving right
                        self.rect.right = min(tree.rect.left, self.rect.right)
                    elif self.dx < 0:  # Moving left
                        self.rect.left = max(tree.rect.right, self.rect.left)

                if self.dx < 0:
                    self.dx = 0

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

                
            #update player coordinates
            self.rect.x += self.dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.player_dead
            draw_text('GAME OVER', font, red, screen_width // 2 -132, screen_height // 2 - 110)
            if self.rect.y > 1:
                self.rect.y -= 5

        if game_over == 0:
            #animation
            if self.jumped:
                self.jump_animation()
            elif self.dx != 0 or self.vel_y != 0:
                self.walk_animation()
            else:
                self.idle_animation()

        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255,255), self.rect, 2)

        return game_over
    
    
    def reset(self, x, y):
        self.player_right = []
        self.player_left = []
        self.player_idle_list = []
        self.player_idle_left_list = []
        self.player_jump_right_list = []
        self.player_jump_left_list = []
        self.player_index = 0
        self.player_idle_index = 0
        self.player_jump_index = 0
        self.counter = 0
        self.idle_counter = 0

        for walk in range(1, 21):
            player_walk_right = pygame.image.load(f'img/CuteGirl/Walk ({walk}).png').convert_alpha()
            player_walk_right = pygame.transform.scale(player_walk_right, (50, 90))
            player_walk_left = pygame.transform.flip(player_walk_right, True, False)
            self.player_right.append(player_walk_right)
            self.player_left.append(player_walk_left)

        for num in range(1, 17):
            player_idle = pygame.image.load(f'img/CuteGirl/Idle ({num}).png').convert_alpha()
            player_idle = pygame.transform.scale(player_idle, (50, 90))
            player_idle_left = pygame.transform.flip(player_idle, True, False)
            self.player_idle_list.append(player_idle)
            self.player_idle_left_list.append(player_idle_left)
        
        for jump in range(1, 31):
            player_jump_right = pygame.image.load(f'img/CuteGirl/Jump ({jump}).png').convert_alpha()
            player_jump_right = pygame.transform.scale(player_jump_right, (50, 90))
            player_jump_left = pygame.transform.flip(player_jump_right, True, False)
            self.player_jump_right_list.append(player_jump_right)
            self.player_jump_left_list.append(player_jump_left)
        
        player_dead= pygame.image.load('img/CuteGirl/ghost.png').convert_alpha()
        self.player_dead = pygame.transform.scale(player_dead, (50, 80))

        self.image = self.player_jump_right_list[self.player_jump_index]
        self.image =self.player_idle_list[self.player_idle_index]
        self.image = self.player_right[self.player_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.dx = 0
        self.jumped = False
        self.direction = 1
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile >= 1 and tile <= 16 or tile == 18 or tile == 21:
                    img_path = f'img/Tiles/{tile}.png'
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile) 
                if tile == 17: 
                    water = Water(col_count * tile_size, row_count * tile_size)
                    water_group.add(water)            
                if tile == 19:
                    rock = Obstacles(col_count * tile_size + 5, row_count * tile_size + 12, 'green')
                    rock_group.add(rock)     
                if tile == 22:
                    tree = Obstacles(col_count * tile_size, row_count * tile_size + 24, 'tree_1')
                    tree_group.add(tree)
                if tile == 26:
                    mush = Obstacles(col_count * tile_size - 40, row_count * tile_size + 33, 'mush_2')
                    mush_group.add(mush)
                if tile == 27:
                    mush_1 = Obstacles(col_count * tile_size - 60, row_count * tile_size + 30, 'mush_1')
                    mush_1_group.add(mush_1)
                if tile == 28:
                    sign_2 = Obstacles(col_count * tile_size, row_count * tile_size, 'sign_2')
                    sign_2_group.add(sign_2)
                if tile == 30:
                    bush_1 = Obstacles(col_count * tile_size, row_count * tile_size, 'bush_1')
                    bush_1_group.add(bush_1)
                if tile == 31:
                    bush_2 = Obstacles(col_count * tile_size + 10, row_count * tile_size + 27, 'bush_2')
                    bush_2_group.add(bush_2)
                if tile == 32:
                    bush_3 = Obstacles(col_count * tile_size + 20, row_count * tile_size + 77, 'bush_3')
                    bush_3_group.add(bush_3)
                if tile == 34:
                    mushroom = Mushroom(col_count * tile_size + 10, row_count * tile_size + 27)
                    mushroom_group.add(mushroom)
                if tile == 35:
                    exit = Exit(col_count * tile_size -20, row_count * tile_size + 2)
                    exit_group.add(exit)
                col_count += 1
            row_count +=  1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_type):
        pygame.sprite.Sprite.__init__(self)

        if obstacle_type == 'green':
            green_1 = pygame.image.load('img/Obstacle/frame-1.png').convert_alpha()
            green_2 = pygame.image.load('img/Obstacle/frame-2.png').convert_alpha()
            scaled_size = (40, 40)
            self.frames = [
                pygame.transform.scale(green_1, scaled_size),
                pygame.transform.scale(green_2, scaled_size)
            ]
        
        if obstacle_type == 'tree_1':
            tree_1 = pygame.image.load('img/Object/Tree_1.png').convert_alpha()
            tree_1 = pygame.transform.scale(tree_1, (70, 28))
            self.frames = [tree_1]

        if obstacle_type == 'mush_1':
            mush_1 = pygame.image.load('img/Object/Mushroom_1.png').convert_alpha()
            mush_1 = pygame.transform.scale(mush_1, (20, 20))
            self.frames = [mush_1]
        
        if obstacle_type == 'mush_2':
            mush_2 = pygame.image.load('img/Object/Mushroom_2.png').convert_alpha()
            mush_2 = pygame.transform.scale(mush_2, (20, 20))
            self.frames = [mush_2]

        if obstacle_type == 'sign_2':
            sign_2 = pygame.image.load('img/Object/Sign_2.png').convert_alpha()
            sign_2 = pygame.transform.scale(sign_2, (60, 50))
            self.frames = [sign_2]
        
        if obstacle_type == 'bush_1':
            bush_1 = pygame.image.load('img/Object/Bush (1).png').convert_alpha()
            bush_1 = pygame.transform.scale(bush_1, (90, 50))
            self.frames = [bush_1]
            
        if obstacle_type == 'bush_2':
            bush_2 = pygame.image.load('img/Object/Bush (3).png').convert_alpha()
            bush_2 = pygame.transform.scale(bush_2, (35, 25))
            self.frames = [bush_2]

        if obstacle_type == 'bush_3':
            bush_3 = pygame.image.load('img/Object/Bush (4).png').convert_alpha()
            bush_3 = pygame.transform.scale(bush_3, (35, 25))
            self.frames = [bush_3]

        self.frames_index = 0

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def animation_state(self):
        obs_cooldown = 0
        if self.move_counter > obs_cooldown:
            self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1 
            self.move_counter *= -1

        self.animation_state()
    
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        water_img = pygame.image.load('img/Tiles/17.png')
        self.image = pygame.transform.scale(water_img, (tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        mushroom_img = pygame.image.load('img/Object/Mushroom_2.png')
        self.image = pygame.transform.scale(mushroom_img, (tile_size // 2,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        exit_img = pygame.image.load('img/Object/Sign_1.png')
        self.image = pygame.transform.scale(exit_img, (60,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


pygame.init()

game_active = True
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Chiri')

font_score = pygame.font.SysFont('Arial Black',20)
font = pygame.font.SysFont('Cooper Black',40)

tile_size = 50
game_over = 0
main_menu = True
score = 0

red = (255,99,71)

bg_surface = pygame.image.load('img/BG/BG.png').convert()
restart_img = pygame.image.load('img/restart_button.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img, (225, 225))
start_img = pygame.image.load('img/start_button.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (250,95))
exit_img = pygame.image.load('img/exit_button.png').convert_alpha()
exit_img = pygame.transform.scale(exit_img, (250,95))

game_title = pygame.image.load('img/game_title.png').convert_alpha()
game_title = pygame.transform.scale(game_title, (581,232))

water = pygame.image.load('img/Tiles/18.png').convert_alpha()
water = pygame.transform.scale(water, (300,50))

water_top = pygame.image.load('img/Tiles/17.png').convert_alpha()
water_top = pygame.transform.scale(water_top, (50,50))

map_level_1 = [
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,32],
[22,31,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,31,35],
[2,3,34,-1,-1,-1,-1,-1,-1,-1,34,-1,-1,1,2,2],
[5,10,3,-1,-1,-1,-1,-1,-1,-1,13,15,-1,12,9,9],
[9,9,16,-1,-1,19,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,13,14,14,15,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,13,15,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,21,-1],
[30,28,-1,-1,-1,-1,-1,13,15,-1,-1,34,-1,21,21,21],
[2,3,-1,-1,-1,-1,-1,-1,-1,-1,1,2,2,2,2,2],
[2,2,2,2,2,3,17,17,17,17,4,5,5,5,5,5],
[5,5,5,5,5,6,18,18,18,18,4,5,5,5,5,5],
]

player = Player(0, screen_height - 230)

rock_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
mush_group = pygame.sprite.Group()
mush_1_group = pygame.sprite.Group()
sign_2_group = pygame.sprite.Group()
bush_1_group = pygame.sprite.Group()
bush_2_group = pygame.sprite.Group()
bush_3_group = pygame.sprite.Group()

mushroom_group = pygame.sprite.Group()
score_mushroom = Mushroom(tile_size // 2 - 15, tile_size // 2 - 12)
mushroom_group.add(score_mushroom)

exit_group = pygame.sprite.Group()
#crate_group = pygame.sprite.Group()


map = World(map_level_1)

#Button
restart_button = Button(screen_width // 2 - 110, screen_height // 2 - 115, restart_img)
start_button = Button(screen_width // 2 - 125, screen_height // 2 - 50, start_img)
exit_button = Button(screen_width // 2 - 125, screen_height // 2 + 50, exit_img)

while game_active:

    screen.blit(bg_surface,(0,0))

    if main_menu == True:
        if exit_button.draw():
            game_active = False
        if start_button.draw():
            main_menu = False
        screen.blit(game_title,(102,10))

    else:

        screen.blit(water, (250,550))
        screen.blit(water_top, (250,500))
        screen.blit(water_top, (500,500))
        
        map.draw()
        tree_group.draw(screen)
        mush_group.draw(screen)
        bush_1_group.draw(screen)
        bush_2_group.draw(screen)
        bush_3_group.draw(screen)

        sign_2_group.draw(screen)
        mush_1_group.draw(screen)
        # crate_group.draw(screen)

        if game_over == 0:
            rock_group.update()
            #score
            #check if a mushroom has been collected
            if pygame.sprite.spritecollide(player, mushroom_group, True):
                score += 1
            draw_text('X ' + str(score), font_score, red, 45, 10)


        rock_group.draw(screen)
        water_group.draw(screen)
        mushroom_group.draw(screen)

        exit_group.draw(screen)
        bush_2_group.draw(screen)
        bush_3_group.draw(screen)

        game_over = player.update(game_over)

        #player has died 
        if game_over == -1: 
            if restart_button.draw():
                player.reset(50, screen_height - 230)
                player = Player(0, screen_height - 230)
                game_over = 0
                score = 0

        if game_over == 1:
            main_menu = True
            
        
        #draw_grid()
    for event in pygame.event.get(): #player input
        if event.type == pygame.QUIT:
            game_active = False

      
    pygame.display.update() 
    clock.tick(40)

pygame.quit()
exit()



