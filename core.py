import random, sys
from hud import *
import defines as gm
import time
from mainmenu import *
from health_bar import *
from bullets_module import *
from items_module import *
from threading import Thread

pygame = gm.pygame
hud = HUD()
hidden = gm.hidden
screen = gm.screen
score = gm.score
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.items = {}
        self.movement_x = 0
        self.movement_y = 0
        self.level = None
        self._count = 0
        self.direction_of_movement = 'down'
        self.lifes = 3#3
        self.bar = HealthBar(self.lifes)
        self.damage_delay = 1
        self.bombs_count = 0
        self.hitbox = gm.hitbox_sprite
        self.hitbox_rect = self.hitbox.rect
        self.control_allowed = True

    def turn_right(self):
        if self.direction_of_movement == 'left' or self.direction_of_movement =='down' or self.direction_of_movement == 'up':
            self.direction_of_movement = 'right'
        self.movement_x = 6

    def turn_left(self):
        if self.direction_of_movement == 'right' or self.direction_of_movement == 'down' or self.direction_of_movement == 'up':
            self.direction_of_movement = 'left'
        self.movement_x = -6

    def turn_up(self):
        if self.direction_of_movement == 'left' or self.direction_of_movement == 'down' or self.direction_of_movement == 'right':
            self.direction_of_movement = 'up'
        self.movement_y = -6

    def turn_down(self):
        if self.direction_of_movement == 'left' or self.direction_of_movement == 'right' or self.direction_of_movement == 'up':
            self.direction_of_movement = 'down'
        self.movement_y = 6

    def stop(self):
        self.movement_x = 0
        self.movement_y = 0

    def player_health_take(self):
        # print(time.time() - self.damage_delay)
        if (self.damage_delay == 1) or (time.time() - self.damage_delay) > 2:
            if self.lifes > 0:
                 self.damage_delay = time.time()
                 self.lifes -= 1
                 self.bar.decreaseHealth()
                 if self.lifes <= 0:
                    self.image = gm.ISAAC_dead

    def update(self):

        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if self.movement_x > 0:
            self._move(gm.IMAGES_R)

        if self.movement_x < 0:
            self._move(gm.IMAGES_L)

        if self.movement_y > 0:
            self._move(gm.IMAGES_D)

        if self.movement_y < 0:
            self._move(gm.IMAGES_U)

        #rysowanie prostokąta
        pseudo_rect = self.rect.inflate(-20,-20)
        width = int(self.rect.right-self.rect.left)
        height = int(self.rect.bottom-self.rect.top)
        self.hitbox_rect.left = self.rect.left + 20
        self.hitbox_rect.top = self.rect.top + 60

        ##Borders collide detect##
        if self.rect.x < 30:
            self.rect.x = 30

        if self.rect.x > gm.WIDTH-110:
            self.rect.x = gm.WIDTH-110

        if self.rect.y < 20:
            self.rect.y = 20

        if self.rect.y > gm.HEIGHT-140:
            self.rect.y = gm.HEIGHT-140
        ##

        #kolizja z przedmiotami
        colliding_items = pygame.sprite.spritecollide(self.hitbox, self.level.set_of_items, False)

        for item in colliding_items:

            if item.name == 'doors_level_1':
                del self.level
                self.level = Level_1(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_UP
                self.rect.y -= 20
                self.stop()

            if item.name == 'doors_level_0':
                del self.level
                self.level = Level_0(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_DOWN
                self.image = gm.ISAAC_UP
                self.rect.y -= 20
                self.stop()

            if item.name == 'doors_level_2':
                del self.level
                self.level = Level_2(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_DOWN
                self.rect.y +=20
                self.stop()

            if item.name == 'doors_level_3':
                del self.level
                self.level = Level_3(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_UP
                self.rect.y -=20
                self.stop()
            if item.name == 'doors_level_4':
                del self.level
                self.level = Level_4(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_DOWN
                self.rect.y += 20
                self.stop()

            if item.name == 'doors_level_5':
                del self.level
                self.level = Level_5(self)
                self.level.draw(screen)
                self.image = gm.ISAAC_DOWN
                self.rect.x = 650
                self.rect.y = 50
                self.stop()

            if item.name == 'rock':
                if self.movement_x > 0:
                    self.rect.right = item.rect.left
                if self.movement_x < 0:
                    self.rect.left = item.rect.right
                if self.movement_y > 0:
                    self.rect.bottom = item.rect.top
                if self.movement_y < 0:
                    self.rect.top = item.rect.bottom

            if item.name == 'bomb':
                self.bombs_count += 3
                hud.set_bombs_count(self.bombs_count)
                self.items[item.name] = 1
                item.image = gm.BOMB
                self.image = gm.BOMB_PICKED
                item.name = 'bomb_picked'
                self.level.set_of_items.remove(item)
                self.stop()

            if item.name =='heart':
                self.items[item.name] = 1
                self.image = gm.HEART_PICKED
                self.level.set_of_items.remove(item)
                self.bar.increaseHealth()
                self.stop()

            if item.name == 'door_key':
                #self.items[item.name] = 1
                self.image = gm.DOORS_KEY_PICKED
                self.level.set_of_items.remove(item)
                self.stop()
                if isinstance(self.level, Level_1):
                    self.level.set_of_items.add(Item(gm.DOORS_UP_OPEN, 'doors_level_2', 683, gm.HEIGHT - 700))
                elif isinstance(self.level, Level_2):
                    self.level.set_of_items.add(Item(gm.DOORS_DOWN_OPEN, 'doors_level_3', 683, gm.HEIGHT - 40))
                elif isinstance(self.level, Level_3):
                    self.level.set_of_items.add(Item(gm.DOORS_UP_OPEN, 'doors_level_4',683, gm.HEIGHT - 700))
                elif isinstance(self.level, Level_4):
                    self.level.set_of_items.add(Item(gm.BOSS_DOORS_OPEN, 'doors_level_5', 683, gm.HEIGHT - 40))



        if isinstance(self.level, Level_3):
            colliding_items = pygame.sprite.spritecollide(self.hitbox, self.level.set_of_bullets, False)
            for bullets in colliding_items:
                self.player_health_take()
        # kolizja z przedmiotami animowanymi
        colliding_items = pygame.sprite.spritecollide(self.hitbox, self.level.set_of_animate_items, False)
        for aitem in colliding_items:
          if aitem.name != 'strong_card_picked' and aitem.name != 'spikes' and aitem.name != 'explosion':
            if self.movement_x > 0:
                self.rect.right = aitem.rect.left
            if self.movement_x < 0:
                self.rect.left = aitem.rect.right
            if self.movement_y > 0:
                self.rect.bottom = aitem.rect.top
            if self.movement_y < 0:
                self.rect.top = aitem.rect.bottom
            if aitem.name == 'strong_card':
                self.items[aitem.name] = 1
                aitem.lifes -= 1
                aitem.image = gm.POOP_6
                self.image = gm.STRONG_CARD_PICKED
                aitem.name = 'strong_card_picked'
                self.stop()
          if aitem.name == 'spikes':
              if aitem.image == aitem.image_list[4]:
                  self.player_health_take()

        #kolizja z enemy
        colliding_enemies = pygame.sprite.spritecollide(self.hitbox,self.level.set_of_enemies,False)
        for enemy in colliding_enemies:
            if enemy.lifes > 0:
                self.player_health_take()


    def draw(self, surface):
            surface.blit(gm.hitbox, gm.hitbox_sprite.rect)
            surface.blit(self.image, self.rect)
            self.bar.draw(self.rect.x, self.rect.y)

    def get_event(self, event):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and keys[pygame.K_w]:
            self.stop()
        if keys[pygame.K_a] and keys [pygame.K_w]:
            self.stop()
        if keys[pygame.K_d] and keys [pygame.K_s]:
            self.stop()
        if keys[pygame.K_a] and keys[pygame.K_s]:
            self.stop()

        if event.type == pygame.KEYDOWN:
            if self.control_allowed:
                if event.key == pygame.K_SPACE and self.lifes > 0:
                    self.shoot()
                if event.key == pygame.K_RETURN and self.lifes > 0:
                    self.plant_bomb()
                if event.key == pygame.K_d and self.lifes > 0:
                    self.turn_right()
                elif event.key == pygame.K_a and self.lifes > 0:
                    self.turn_left()
                elif event.key == pygame.K_w and self.lifes > 0:
                    self.turn_up()
                elif event.key == pygame.K_s and self.lifes > 0:
                    self.turn_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.stop()
            if event.key == pygame.K_a:
                self.stop()
            if event.key == pygame.K_w:
                self.stop()
            if event.key == pygame.K_s:
                self.stop()

    def _move(self, image):
         if self._count < 2:
            self.image = image[0]
         elif self._count < 4:
             self.image = image[1]
         elif self._count < 6:
             self.image = image[2]
         elif self._count < 8:
            self.image = image[3]

         if self._count >= 8:
             self._count = 0
         else:
             self._count +=1

    def shoot(self):
        if len(self.level.set_of_bullets) <3:
            bullet = Bullet(gm.BASIC_BULLET, self.direction_of_movement ,self.rect.centerx, self.rect.centery+15)
            self.level.set_of_bullets.add(bullet)


    def plant_bomb(self):
            if(self.bombs_count > 0):
                bomb = ItemWithAnimation(gm.EXPLOSION[0], gm.EXPLOSION, 'explosion', self.rect.x+40, self.rect.y+48)
                self.level.set_of_animate_items.add(bomb)
                self.bombs_count -= 1
                hud.set_bombs_count(self.bombs_count)

#klasa  przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_image, image_list_right,
                 image_list_left, image_list_up, image_list_down,
                 movement_x=0, movement_y=0):
        super().__init__()
        self.image = start_image
        self.rect = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.image_list_right = image_list_right
        self.image_list_left = image_list_left
        self.image_list_up = image_list_up
        self.image_list_down = image_list_down
        self.direction_of_movement = 'down'
        self.lifes = 2
        self._count = 0
        self.bar = HealthBar(self.lifes)
        self.id = 'Basic'

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bar.draw(self.rect.x, self.rect.y)

    def _move(self, image_list):
        if self._count < 2:
            self.image = image_list[0]
        elif self._count < 4:
            self.image = image_list[1]
        elif self._count < 6:
            self.image = image_list[2]
        elif self._count < 8:
            self.image = image_list[3]
        if self._count >= 8:
            self._count = 0
        else:
            self._count += 1

    def enemy_bar_update(self):
        self.bar.decreaseHealth()

#Klasa przeciwnika(red)
class RedEnemy(Enemy):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_up, image_list_down,height, width,
                 movement_x = 0, movement_y =0):
        super().__init__(start_image,image_list_right,image_list_left,image_list_up,image_list_down,movement_x,movement_y)
        self.rect.y = height
        self.rect.x = width
        self.lifes = 3
        self.bar = HealthBar(self.lifes)
        self.id = 'Red'

    def update(self):
        if self.lifes <= 0:
            self.kill()
            if self.direction_of_movement == 'left':
                self.image = gm.RED_DEADR
            else:
                self.image = gm.RED_DEADL

        if self.movement_x == 252:
            self.movement_x = -252

        if self.lifes > 0:
            if self.movement_x >= 0:
                if self.rect.x < 1260:
                  self.movement_x += 1
                  self.rect.x += 5
                  self._move(self.image_list_right)
                  self.direction_of_movement = 'right'
            elif self.movement_x < 0:
                if self.rect.x >= 0:
                    self.movement_x += 1
                    self.rect.x -= 5
                    self._move(self.image_list_left)
                    self.direction_of_movement = 'left'



#klasa przeciwnika (devil)
class DevilEnemy(Enemy):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_up, image_list_down,height, width, name,
                 movement_x = 0, movement_y =0):
        super().__init__(start_image,image_list_right,image_list_left,image_list_up,image_list_down,movement_x,movement_y)
        self.rect.y = height
        self.rect.x = width
        self.lifes = 2
        self.bar = HealthBar(self.lifes)
        self.name = name

    def update(self):
        if self.lifes <= 0:
            self.kill()
            if self.direction_of_movement == 'left':
                self.image = gm.DEVIL_DEADR
            else:
                self.image = gm.DEVIL_DEADL


        if self.name == 'devil1':
           if self.lifes:
            if self.rect.y == gm.HEIGHT - 200:
                self.rect.x += 5
                self.direction_of_movement ='right'
                self._move(self.image_list_right)
            if self.rect.x == 900:
                self.rect.y -= 5
                self._move(self.image_list_up)
                self.direction_of_movement = 'right'
            if self.rect.y == gm.HEIGHT - 600:
                self.rect.x -= 5
                self._move(self.image_list_left)
                self.direction_of_movement = 'left'
            if self.rect.x == 400 and self.rect.y != gm.HEIGHT-200:
                self.rect.y += 5
                self._move(self.image_list_down)
                self.direction_of_movement = 'left'

        if self.name == 'devil2':
          if self.lifes:
            if self.rect.y == gm.HEIGHT - 200:
                self.rect.x += 5
                self._move(self.image_list_right)
                self.direction_of_movement = 'right'
            if self.rect.x == 900:
                self.rect.y -= 5
                self._move(self.image_list_up)
                self.direction_of_movement = 'right'
            if self.rect.y == gm.HEIGHT - 600:
                self.rect.x -= 5
                self._move(self.image_list_left)
                self.direction_of_movement = 'left'
            if self.rect.x == 400 and self.rect.y != gm.HEIGHT - 200:
                self.rect.y += 5
                self._move(self.image_list_down)
                self.direction_of_movement = 'left'

        if self.name == 'devil3':
            if self.lifes:
                if self.rect.y == gm.HEIGHT - 200:
                    self.rect.x += 5
                    self.direction_of_movement = 'right'
                    self._move(self.image_list_right)
                if self.rect.x == 900:
                    self.rect.y -= 5
                    self._move(self.image_list_up)
                    self.direction_of_movement = 'right'
                if self.rect.y == gm.HEIGHT - 500:
                    self.rect.x -= 5
                    self._move(self.image_list_left)
                    self.direction_of_movement = 'left'
                if self.rect.x == 400 and self.rect.y != gm.HEIGHT - 200:
                    self.rect.y += 5
                    self._move(self.image_list_down)
                    self.direction_of_movement = 'left'

#Klasa przeciwnika(red)
class BossEnemy(Enemy):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_up, image_list_down,height, width,
                 movement_x = 0, movement_y =0):
        super().__init__(start_image,image_list_right,image_list_left,image_list_up,image_list_down,movement_x,movement_y)
        self.rect.y = height
        self.rect.x = width
        self.lifes = 10
        self.bar = HealthBar(self.lifes)
        self.id = 'Boss'

    def update(self):
        if self.lifes <= 0:
            self.kill()
            self.image = gm.BOSS_DEAD

        if self.lifes:
            if self.rect.y == gm.HEIGHT - 200 and self.rect.x <900:
                self.rect.x += 20
                self.direction_of_movement = 'right'
                self._move(self.image_list_right)
            if self.rect.x == 900 and self.rect.y != gm.HEIGHT-600:
                self.rect.y -= 20
                self._move(self.image_list_up)
                self.direction_of_movement = 'right'
            if self.rect.y == gm.HEIGHT - 400 and self.rect.x != 1000:
                self.rect.x -= 20
                self._move(self.image_list_left)
                self.direction_of_movement = 'left'
            if self.rect.x == 400 and self.rect.y != gm.HEIGHT - 600:
                self.rect.y -= 20
                self._move(self.image_list_down)
                self.direction_of_movement = 'left'
            if self.rect.y == gm.HEIGHT -600 and self.rect.x != 1000 :
                self.rect.x += 20
                self.direction_of_movement = 'right'
                self._move(self.image_list_right)
            if self.rect.x == 1000 and self.rect.y >= gm.HEIGHT-600:
                self.rect.y += 20
                self._move(self.image_list_down)
                self.direction_of_movement = 'left'
            if self.rect.y == gm.HEIGHT -180:
                self.rect.x -= 20
                self._move(self.image_list_left)
                self.direction_of_movement = 'left'


#klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, rect_x, rect_y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill(colour)
        self.rect.x = rect_x
        self.rect.y = rect_y

    def draw(self, surface):
       # self.image.set_alpha(0)
        surface.blit(self.image, self.rect)


#klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_bullets = pygame.sprite.Group()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_animate_items = set()
        self.set_of_platforms = set()
        self.set_of_enemies = set()
        self.player = player

    def draw(self, surface):
        self.set_of_bullets.draw(surface)
        self.set_of_items.draw(surface)
        for p in self.set_of_platforms:
            p.draw(surface)
        for enemy in self.set_of_enemies:
            enemy.draw(surface)
        for i in self.set_of_animate_items:
            i.draw(surface)

    def update(self):
        self.set_of_bullets.update()
        self._delete_bullet()
        self._delete_bomb()

        for p in self.set_of_platforms:
            p.update()
        for enemy in self.set_of_enemies:
            enemy.update()
        for i in self.set_of_animate_items:
            i.update()

        #wieża strzela
        if len(self.set_of_bullets) < 1:
            for item in self.set_of_items:
                if item.name == 'tower':
                 bullet = Bullet(gm.STONE_BULLET, 'down', item.rect.centerx, item.rect.centery + 50)
                 self.set_of_bullets.add(bullet)


        # kolizja z enemy
        for enemy in self.set_of_enemies:
            colliding_bullets = pygame.sprite.spritecollide(enemy, self.set_of_bullets, False)
            for bullet in colliding_bullets:
                if enemy.lifes > 0:
                    enemy.lifes -= 1
                    enemy.enemy_bar_update()
                    bullet.kill()

                    if enemy.lifes == 0:
                        if enemy.id == 'Red':
                            score.add_score(200)
                        if enemy.id == 'Basic':
                            score.add_score(100)
                        if enemy.id == 'Boss':
                            score.add_score(1000)
                del bullet


        #kolizja rzeczy z bombami
       # for items in self.set_of_items:
            #colliding_items = pygame.sprite.spritecollide(items, self.set_of_animate_items,False)
           # for aitem in colliding_items:
               # if aitem.name =='explosion':
                   # items.kill()


        for aitems in self.set_of_animate_items:
            colliding_bullets = pygame.sprite.spritecollide(aitems, self.set_of_bullets, False)
            for bullet in colliding_bullets:
                if aitems.name == 'poop':
                    aitems.lifes -= 1
                    bullet.kill()



        for items in self.set_of_items:
            colliding_bullets = pygame.sprite.spritecollide(items, self.set_of_bullets, False)
            for bullet in colliding_bullets:
                if items.name == 'rock':
                    bullet.kill()

        for items in self.set_of_items:
            for aitems in self.set_of_animate_items:
                if items.name =='rock':
                    if aitems.name == 'explosion':
                        if aitems.rect_1.colliderect(items):
                            items.kill()
                        if aitems.rect_2.colliderect(items):
                            items.kill()



    def _delete_bullet(self):
         for bullet in self.set_of_bullets:
             if bullet.rect.left > gm.WIDTH-50 or bullet.rect.right < 50 or bullet.rect.top < 30 or bullet.rect.bottom > gm.HEIGHT-25:
                    bullet.kill()

    def _delete_bomb(self):
        item_to_delete = None
        for aitems in self.set_of_animate_items:
            if aitems.name == 'end_explosion':
                item_to_delete = aitems
        if item_to_delete != None:
            if item_to_delete.name == 'end_explosion':
                self.set_of_animate_items.remove(item_to_delete)



#klasa mapa 1

class Level_0(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Tutorial"
        self.create_items()

    def create_items(self):
        doors = Item(gm.DOORS_DOWN_OPEN, 'doors_level_1', 683, gm.HEIGHT - 40)
        self.set_of_items.add(doors)

    def chapter_end(self):
        pass


class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Level 1"
        self.create_items()
        #self.create_platforms()
        self.create_enemies()


    def create_items(self):

        door_key = Item(gm.DOOR_KEY, 'door_key', 100, gm.HEIGHT - 120)
        doors_level_0 = Item(gm.DOORS_DOWN, 'doors', 683, gm.HEIGHT - 40)
        doors_level_1 = Item(gm.DOORS_UP, 'doors_level', 683, gm.HEIGHT - 700)
        rock_1 = Item(gm.ROCK, 'rock', 80, gm.HEIGHT - 260)
        rock_2 = Item(gm.ROCK, 'rock', 140, gm.HEIGHT - 260)
        rock_3 = Item(gm.ROCK, 'rock', 200, gm.HEIGHT - 260)
        rock_6 = Item(gm.ROCK, 'rock', 260, gm.HEIGHT - 260)
        rock_4 = Item(gm.ROCK, 'rock', 260, gm.HEIGHT - 140)
        rock_5 = Item(gm.ROCK, 'rock', 260, gm.HEIGHT - 80)
        rock_7 = Item(gm.ROCK, 'rock', 260, gm.HEIGHT - 200)
        bomb = Item(gm.BOMB, 'bomb', 1000, gm.HEIGHT - 120)
        self.set_of_items.add(door_key)
        self.set_of_items.add(doors_level_0)
        self.set_of_items.add(doors_level_1)
        self.set_of_items.add(rock_1)
        self.set_of_items.add(rock_2)
        self.set_of_items.add(rock_3)
        self.set_of_items.add(rock_4)
        self.set_of_items.add(rock_5)
        self.set_of_items.add(rock_6)
        self.set_of_items.add(rock_7)
        self.set_of_items.add(bomb)


    def create_enemies(self):
        enemy1 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 100,0)
        enemy2 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 350,0)
        self.set_of_enemies.add(enemy1)
        self.set_of_enemies.add(enemy2)

    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]
        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)

#klasa mapa 2
class Level_2(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Level 2"
        self.create_enemies()
        self.create_items()
       # self.create_platforms()


    def create_items(self):
        doors_level_1 = Item(gm.DOORS_UP, 'doors', 683, gm.HEIGHT - 700)
        doors_level_3 = Item(gm.DOORS_DOWN, 'doors_level', 683, gm.HEIGHT - 40)
        poop = ItemWithAnimation(gm.POOP_1, gm.POOP, 'poop', 670, gm.HEIGHT-320)

        # pion lewy
        spikes_1 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 520, gm.HEIGHT / 2 - 60)  # lewy górny
        spikes_3 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 520, gm.HEIGHT / 2 + 60)
        spikes_5 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 520, gm.HEIGHT / 2)
        spikes_15 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 520, gm.HEIGHT / 2 - 120)
        spikes_6 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 520, gm.HEIGHT / 2 + 120)
        # pion prawy
        spikes_2 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2 - 60)
        spikes_4 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2 + 60)
        spikes_7 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2 - 120)
        spikes_12 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2)
        spikes_9 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2 + 120)
        # poziom góra
        spikes_10 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 760, gm.HEIGHT / 2 - 120)
        spikes_11 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 700, gm.HEIGHT / 2 - 120)
        spikes_13 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 580, gm.HEIGHT / 2 - 120)
        spikes_14 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 640, gm.HEIGHT / 2 - 120)
        spikes_8 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 820, gm.HEIGHT / 2 - 120)
        # poziom dół
        spikes_16 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 760, gm.HEIGHT / 2 + 120)
        spikes_17 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 700, gm.HEIGHT / 2 + 120)
        spikes_18 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 640, gm.HEIGHT / 2 + 120)
        spikes_19 = ItemWithAnimation(gm.SPIKES[0], gm.SPIKES, 'spikes', 580, gm.HEIGHT / 2 + 120)

        door_key = Item(gm.DOOR_KEY, 'door_key', 100, gm.HEIGHT - 120)
        self.set_of_animate_items.add(spikes_1)
        self.set_of_animate_items.add(spikes_2)
        self.set_of_animate_items.add(spikes_3)
        self.set_of_animate_items.add(spikes_4)
        self.set_of_animate_items.add(spikes_5)
        self.set_of_animate_items.add(spikes_6)
        self.set_of_animate_items.add(spikes_7)
        self.set_of_animate_items.add(spikes_8)
        self.set_of_animate_items.add(spikes_9)
        self.set_of_animate_items.add(spikes_10)
        self.set_of_animate_items.add(spikes_11)
        self.set_of_animate_items.add(spikes_12)
        self.set_of_animate_items.add(spikes_13)
        self.set_of_animate_items.add(spikes_14)
        self.set_of_animate_items.add(spikes_15)
        self.set_of_animate_items.add(spikes_16)
        self.set_of_animate_items.add(spikes_17)
        self.set_of_animate_items.add(spikes_18)
        self.set_of_animate_items.add(spikes_19)

        self.set_of_animate_items.add(poop)
        self.set_of_items.add(door_key)
        self.set_of_items.add(doors_level_1)
        self.set_of_items.add(doors_level_3)

    def create_enemies(self):
        enemy1 = DevilEnemy(gm.DEVIL_START, gm.DEVIL_R, gm.DEVIL_L, gm.DEVIL_U, gm.DEVIL_D, 540, 400,'devil1')
        enemy2 = DevilEnemy(gm.DEVIL_START, gm.DEVIL_R, gm.DEVIL_L, gm.DEVIL_U, gm.DEVIL_D, 240, 900, 'devil2')
        self.set_of_enemies.add(enemy1)
        self.set_of_enemies.add(enemy2)
    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]

        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)

#klasa mapa 3
class Level_3(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Level 3"
        self.create_items()
        #self.create_platforms()
        self.create_enemies()


    def create_items(self):

        doors_level_0 = Item(gm.DOORS_DOWN, 'doors_level_22', 683, gm.HEIGHT - 40)
        doors_level_1 = Item(gm.DOORS_UP, 'doors_level', 683, gm.HEIGHT - 700)
        tower1 = Item(gm.TOWER, 'tower', 200, gm.HEIGHT -680)
        tower2 = Item(gm.TOWER, 'tower', 500, gm.HEIGHT -680)
        tower3 = Item(gm.TOWER, 'tower', 1200, gm.HEIGHT -680)
        tower4 = Item(gm.TOWER, 'tower', 900, gm.HEIGHT -680)

        door_key = Item(gm.DOOR_KEY, 'door_key', 100, gm.HEIGHT - 120)

        self.set_of_items.add(door_key)
        self.set_of_items.add(doors_level_0)
        self.set_of_items.add(doors_level_1)
        self.set_of_items.add(tower1)
        self.set_of_items.add(tower2)
        self.set_of_items.add(tower3)
        self.set_of_items.add(tower4)
        self.set_of_items.add(door_key)

    def create_enemies(self):
        pass


    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]
        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)

class Level_4(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Level 4"
        self.create_items()
        #self.create_platforms()
        self.create_enemies()


    def create_items(self):

        door_key = Item(gm.DOOR_KEY, 'door_key', 100, gm.HEIGHT - 120)
        doors_level_0 = Item(gm.BOSS_DOORS, 'doors_level', 683, gm.HEIGHT - 40)
        doors_level_1 = Item(gm.DOORS_UP, 'doors', 683, gm.HEIGHT - 700)
        rock_1 = Item(gm.ROCK, 'rock', 1286, gm.HEIGHT - 260)
        rock_6 = Item(gm.ROCK, 'rock', 1226, gm.HEIGHT - 260)
        rock_2 = Item(gm.ROCK, 'rock', 1086, gm.HEIGHT - 260)
        rock_3 = Item(gm.ROCK, 'rock', 1156, gm.HEIGHT - 260)
        rock_4 = Item(gm.ROCK, 'rock', 1086, gm.HEIGHT - 140)
        rock_7 = Item(gm.ROCK, 'rock', 1086, gm.HEIGHT - 200)
        rock_5 = Item(gm.ROCK, 'rock', 1086, gm.HEIGHT - 80)
        bomb = Item(gm.BOMB, 'bomb', 1000, gm.HEIGHT - 120)
        heart = Item(gm.HEART,'heart', 1266, gm.HEIGHT - 130)
        self.set_of_items.add(door_key)
        self.set_of_items.add(doors_level_0)
        self.set_of_items.add(doors_level_1)
        self.set_of_items.add(rock_1)
        self.set_of_items.add(rock_2)
        self.set_of_items.add(rock_3)
        self.set_of_items.add(rock_4)
        self.set_of_items.add(rock_5)
        self.set_of_items.add(rock_6)
        self.set_of_items.add(rock_7)
        self.set_of_items.add(bomb)
        self.set_of_items.add(heart)


    def create_enemies(self):
        enemy1 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 100,0)
        enemy2 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 350,0)
        enemy3 = DevilEnemy(gm.DEVIL_START, gm.DEVIL_R, gm.DEVIL_L, gm.DEVIL_U, gm.DEVIL_D, 540, 400,'devil3')
        self.set_of_enemies.add(enemy1)
        self.set_of_enemies.add(enemy2)
        self.set_of_enemies.add(enemy3)

    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]
        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)


class Level_5(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.level_name = "Level Boss"
        self.create_items()
        #self.create_platforms()
        self.create_enemies()



    def create_items(self):
        doors_level_1 = Item(gm.BOSS_DOORS_DOWN, 'doors', 683, gm.HEIGHT - 700)
        self.set_of_items.add(doors_level_1)


    def create_enemies(self):
        self.boss = BossEnemy(gm.BOSS_START, gm.BOSS_R, gm.BOSS_L, gm.BOSS_U, gm.BOSS_D, 540, 400)
        self.set_of_enemies.add(self.boss)


    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]
        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)

    def chapter_end(self):
        if self.boss.lifes <= 0:
            return 4


def game_start():
    flag = 1
    player = Player(gm.ISAAC_DOWN)
    current_level = Level_0(player)
    player.level = current_level
    player.rect.center = screen.get_rect().center
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(gm.background,(0, 0))
        if current_level.level_name == "Tutorial":
            screen.blit(gm.controls_bg, (int(gm.WIDTH/5-50), 250))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

            player.get_event(event)

        # rysowanie i aktualizacja obiektow
        current_level = player.level
        current_level.update()
        hud.display()
        player.update()
        current_level.draw(screen)
        player.draw(screen)
        if current_level.level_name == 'Level Boss':
            if current_level.chapter_end() == 4:
                player.stop()
                player.control_allowed = False
                gm.FPS = 10
                if flag == 1:
                    flag += 1
                chapter_win_screen()
            else:
                gm.FPS = 30

        if player.lifes <= 0:
            gm.FPS = 10
            player.stop()
            if lost_menu() == 1:
                del player
                del current_level
                return 3
        else:
            gm.FPS = 30

        # aktualizacja okna
        pygame.display.flip()
        clock.tick(gm.FPS)

game_menu = True
while game_menu:
    screen.fill((0, 0, 0))
    score.reset()
    hud.set_bombs_count(0)
    if mm() == 1:
        game_start()
            # lost_menu() # PLAYER SCORE <-
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

