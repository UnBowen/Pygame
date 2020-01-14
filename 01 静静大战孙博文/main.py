import random
import time
import pygame
# from plane_sprites import *

pygame.init()

SCREEN = pygame.Rect(0,0,1200,675)
BGPICTURE = pygame.Rect(0,0,1200,1566)
CREAT_ENEMY_EVENT = 24
ENEMY_FASTER = 2
ENEMY_COME_FASTER = 3
ENEMY_STRONGER_TIMES = 5

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image_name,speed=3):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

class Background(GameSprite):
    def __init__(self, is_alt = False):
        super().__init__('./image/sky1.png')
        if is_alt:
            self.rect.y = -BGPICTURE.height
    def update(self):
        super().update()
        if self.rect.y >= BGPICTURE.height:
            self.rect.y = -BGPICTURE.height

class Enemy(GameSprite):
    enemy_speeder = 15
    def __init__(self):
        super().__init__('./image/孙博文1.png',speed = random.uniform(3,Enemy.enemy_speeder))
        self.rect.bottom = 0
        max_x = SCREEN.width - self.rect.width
        self.rect.x = random.randrange(0, max_x, self.rect.width)
    def update(self):
        super().update()
        if self.rect.y >= SCREEN.height:
            self.kill()



class Hero(GameSprite):
    def __init__(self):
        super().__init__('./image/静静1.png')
        self.rect.centerx = SCREEN.centerx
        self.rect.bottom = SCREEN.bottom - 30
        self.speedy = 0
        self.bullets = pygame.sprite.Group()
        self.love = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speedy
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        elif self.rect.centerx > SCREEN.right:
            self.rect.centerx = SCREEN.right
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN.bottom:
            self.rect.bottom = SCREEN.bottom

    def fire(self):
        bullet = Bullet()

        bullet.rect.bottom = self.rect.y
        bullet.rect.centerx = self.rect.centerx

        self.bullets.add(bullet)

    def fall_love(self):
        love = Love()
        love.rect.centerx = self.rect.centerx
        love.rect.centery = self.rect.y
        self.love.add(love)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__('./image/平底锅1.png',speed = -5)


    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

class Love(GameSprite):
    def __init__(self):
        super().__init__('./image/Love1.png',speed = 0)


class GamePlay(object):


    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN.size)
        self.clock = pygame.time.Clock()
        self.enemykill = 0
        self.__creat_sprites()
        self.flag = True
        self.enemy_come_speed = 1000

        pygame.time.set_timer(CREAT_ENEMY_EVENT, self.enemy_come_speed)

    def __creat_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)




    def start_game(self):

        while self.flag:
            self.clock.tick(80)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            self.__score_display()

            pygame.display.update()


        while not self.flag:
                self.__event_handler()


    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GamePlay.__game_over()
            elif event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_RIGHT]:
                self.hero.speed = 10
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed = -10
            else:
                self.hero.speed = 0

            if keys_pressed[pygame.K_UP]:
                self.hero.speedy = -10
            elif keys_pressed[pygame.K_DOWN]:
                self.hero.speedy = 10
            else:
                self.hero.speedy = 0

            if keys_pressed[pygame.K_SPACE]:
                self.hero.fire()

    def __score_display(self):
        text = pygame.font.Font(r'C:\py\飞机大战\image\灵动指书手机字体.ttf',50)
        text_fmt = text.render(str('干掉  %d  个孙博文' %self.enemykill),1,(0,0,0))
        self.screen.blit(text_fmt,(10,10))


    def __check_collide(self):
        killenemy = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group, True, True)
        if killenemy:
            self.enemykill += 1

            if self.enemykill% ENEMY_STRONGER_TIMES == 0:
                pygame.time.set_timer(CREAT_ENEMY_EVENT, int(self.enemy_come_speed/ENEMY_COME_FASTER))
                Enemy.enemy_speeder += ENEMY_FASTER


        ret = pygame.sprite.groupcollide(self.hero_group, self.enemy_group, False, False)
        if ret:
            self.hero.fall_love()
            self.flag = False


    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.hero.love.update()
        self.hero.love.draw(self.screen)



    @staticmethod
    def __game_over():
        pygame.quit()
        exit()

# if __name__ == '__main__':
game = GamePlay()
game.start_game()
