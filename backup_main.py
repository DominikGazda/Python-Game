import pygame, os , random, sys
import defines as gm
import time


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#ekran i gra
screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption('Giereczka')
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
        self.lifes = 3
        self.bar = HealthBar(self.lifes)
        self.damage_delay = 1

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
        print(time.time() - self.damage_delay)
        if (self.damage_delay == 1) or (time.time() - self.damage_delay) > 2:
             self.damage_delay = time.time()
             self.lifes -= 1
             self.bar.decreaseHealth()

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

        #kolizja z platformami w poziomie
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)

        for p in colliding_platforms:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
            if self.movement_x < 0:
                self.rect.left = p.rect.right
        #w pionie
        for p in colliding_platforms:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top

            if self.movement_y < 0:
                self.rect.top = p.rect.bottom
        #kolizja z przedmiotami
        colliding_items = pygame.sprite.spritecollide(self, self.level.set_of_items, False)
        for item in colliding_items:

            if item.name == 'doors':
               print("dotykasz drzwi ez")
               del self.level
               self.level = Level_2(player)
               self.level.draw(screen)
               self.image = gm.ISAAC_DOWN
               self.stop()

        # kolizja z przedmiotami animowanymi
        colliding_items = pygame.sprite.spritecollide(self, self.level.set_of_animate_items, False)
        for aitem in colliding_items:
          if aitem.name != 'strong_card_picked':
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
                player.image = gm.STRONG_CARD_PICKED
                aitem.name = 'strong_card_picked'
                self.stop()
        #kolizja z enemy
        colliding_enemies = pygame.sprite.spritecollide(self,self.level.set_of_enemies,False)
        for enemy in colliding_enemies:
            if enemy.lifes:
                self.player_health_take()


    def draw(self, surface):
            surface.blit(self.image, self.rect)
            self.bar.draw(self.rect.x, self.rect.y)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shoot()
            if event.key == pygame.K_d:
                self.turn_right()
            if event.key == pygame.K_a:
                self.turn_left()
            if event.key == pygame.K_w:
                self.turn_up()
            if event.key == pygame.K_s:
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
            bullet = Bullet(gm.BASIC_BULLET, self.direction_of_movement ,self.rect.centerx, self.rect.centery+15)
            self.level.set_of_bullets.add(bullet)

#klasa pocisku
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [rect_center_x, rect_center_y]
        self.direction_of_movement = direction


    def update(self):
        if self.direction_of_movement == 'right':
            self.rect.x += 15
        elif self.direction_of_movement == 'left':
            self.rect.x -= 15
        elif self.direction_of_movement == 'up':
            self.rect.y -= 15
        else:
            self.rect.y += 15


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, health):
        super().__init__()
        self.health_max = health
        self.health_current = health
        self.width = 80

    def decreaseHealth(self):
         self.health_current -= 1
         if self.health_current <= 0:
             self.width = 0
             self.bar = None
         else:
            dzielnik = self.health_max / self.health_current
            self.width = int(80 / dzielnik)


    def draw(self, rect_x, rect_y):
        self.frame = pygame.draw.rect(screen, gm.WHITE, (rect_x - 2, rect_y - 17, 84, 14))
        self.bar = pygame.draw.rect(screen, gm.RED, (rect_x, rect_y - 15, self.width, 10))

#klasa przedmiotu
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]


class ItemWithAnimation(Item):
    def __init__(self, image , name , rect_center_x, rect_center_y):
        super().__init__(image, name ,rect_center_x,rect_center_y)
        self.lifes = 4
        self.image_list = gm.POOP
    def update(self):
        if self.lifes == 4:
            self.image = self.image_list[0]
        elif self.lifes == 3:
            self.image = self.image_list[1]
        elif self.lifes == 2:
            self.image = self.image_list[2]
        elif self.lifes == 1:
            self.image = self.image_list[3]
        elif self.lifes == 0:
            self.image = self.image_list[4]
            self.name = 'strong_card'


    def draw(self, surface):
        surface.blit(self.image, self.rect)



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


#Klasa przeciwnika(red)
class RedEnemy(Enemy):
    def __init__(self, start_image, image_list_right, image_list_left, image_list_up, image_list_down,height,
                 movement_x = 0, movement_y =0):
        super().__init__(start_image,image_list_right,image_list_left,image_list_up,image_list_down,movement_x,movement_y)
        self.rect.y = height



player = Player(gm.ISAAC_DOWN)

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
        self.image.set_alpha(0)
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

        for p in self.set_of_platforms:
            p.update()
        for enemy in self.set_of_enemies:
            enemy.update()
        for i in self.set_of_animate_items:
            i.update()

        # kolizja z enemy
        for enemy in self.set_of_enemies:
            colliding_bullets = pygame.sprite.spritecollide(enemy, self.set_of_bullets, False)
            for bullet in colliding_bullets:
                enemy.lifes -= 1
                enemy.enemy_bar_update()
                bullet.kill()
        for aitems in self.set_of_animate_items:
            colliding_bullets = pygame.sprite.spritecollide(aitems, self.set_of_bullets, False)
            for bullet in colliding_bullets:
                aitems.lifes -= 1
                bullet.kill()

    def _delete_bullet(self):
         for bullet in self.set_of_bullets:
             if bullet.rect.left > gm.WIDTH-50 or bullet.rect.right < 50 or bullet.rect.top < 30 or bullet.rect.bottom > gm.HEIGHT-25:
                    bullet.kill()
#klasa mapa 1

class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.create_items()
        self.create_platforms()
        self.create_enemies()


    def create_items(self):
        shotgun = Item(gm.STRONG_CARD, 'strong_card', 100, gm.HEIGHT - 120)
        doors = Item(gm.DOORS_UP, 'doors', 683,gm.HEIGHT - 700)

        self.set_of_items.add(shotgun)
        self.set_of_items.add(doors)

    def create_enemies(self):
        enemy1 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 260)
        enemy2 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 420)
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
        self.create_items()
        self.create_platforms()
        self.create_enemies()

    def create_items(self):
        shotgun = Item(gm.STRONG_CARD, 'strong_card', 100, gm.HEIGHT - 120)
        doors = Item(gm.DOORS_UP, 'doors', 683, gm.HEIGHT - 700)
        poop = ItemWithAnimation(gm.POOP_1,'poop', 100, gm.HEIGHT-400)
        self.set_of_items.add(shotgun)
        self.set_of_animate_items.add(poop)

    def create_enemies(self):
        enemy1 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 260)
        #enemy2 = RedEnemy(gm.RED_START, gm.RED_R, gm.RED_L, gm.RED_U, gm.RED_D, 420)
        self.set_of_enemies.add(enemy1)
        #self.set_of_enemies.add(enemy2)
    def create_platforms(self):
        ws_platform_static = [[gm.WIDTH-1332, 740, 0, gm.HEIGHT-740], [gm.WIDTH-30, 740, 1332,gm.HEIGHT-740], [gm.WIDTH, 40, 0, gm.HEIGHT - 30], [gm.WIDTH, 1, 0, gm.HEIGHT - 740]]

        for ws in ws_platform_static:
            platform_object = Platform(gm.LIGHTBLUE, *ws)
            self.set_of_platforms.add(platform_object)


# Tworzenie obiektów

current_level = Level_1(player)
player.level = current_level
player.rect.center = screen.get_rect().center


# Game loop dopóki nie klikniemy X gra działa

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(gm.background,(0, 0))
    # pętla z funkcjami przycisków
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
    player.update()
    current_level.draw(screen)
    player.draw(screen)
    # aktualizacja okna
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

