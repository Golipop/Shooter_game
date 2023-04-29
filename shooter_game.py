from time import time as timer
from pygame import *
from random import *

mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y, w , h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def Fire(self):
        pulya = Bullet('bullet.png', 10, self.rect.centerx, self.rect.top, 15, 20)
        bull.add(pulya)

lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620) 
            lost += 1

class Bum(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bull = sprite.Group()

monsters = sprite.Group()

aster = sprite.Group()

for i in range(5):
    monster = Enemy('SUGOMA.png', randint(1, 3), randint(80, 620), -40, 80, 50)
    monsters.add(monster)

for i in range(2):
    ast = Bum('asteroid.png', randint(1, 3), randint(80, 620), -100, 100, 100)
    aster.add(ast)
    
window = display.set_mode((700,500))
display.set_caption('Амогус')

clock = time.Clock()
FPS = 70

bg = transform.scale(image.load('galaxy.jpg'), (700,500))
player = Player('AMOGUS.png', 8, 320, 400, 150 , 100)

font1 = font.SysFont('Times New Roman', 36)


mixer.music.load('sabbotazh.ogg')
mixer.music.play()

shot = mixer.Sound('d8a048f-8891-4b.ogg')
victor = mixer.Sound('papap.ogg')
over = mixer.Sound('amogus-bass-boost.ogg')

game = True
finish = False



num_fire = 0
rel_time = False
life = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    player.Fire()
                    shot.play()
                    num_fire += 1
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                    
    if finish != True:
        window.blit(bg, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bull.draw(window)
        bull.update()
        aster.draw(window)
        aster.update()
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Убито: ' + str(score), 1, (255, 255, 255))
        win = font1.render('ТЫ ПОБЕДИЛ', True, (255, 255, 0))
        lose = font1.render('ТЫ БОТ', True, (255, 255, 0))
        window.blit(text_lose, (10, 50))
        window.blit(text_score, (10, 15))
        collides = sprite.groupcollide(monsters, bull, True, True)
        sprite_list = sprite.spritecollide(player, monsters, False)
        lsf = sprite.spritecollide(player, aster, False)
        for i in collides:
            score += 1
            monster = Enemy('SUGOMA.png', randint(1, 3), randint(80, 620), -40, 80, 50)
            monsters.add(monster)
        if score > 10:
            finish = True
            window.blit(win,(200, 200))
            mixer.music.stop()
            victor.play()
        if lost >= 3 or sprite_list or lsf:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()
            over.play()
            
    keys_pressed = key.get_pressed()
    if keys_pressed[K_r]:
        score = 0
        lost = 0
        finish = False
        for i in monsters:
            i.rect.x = randint(0, 500)
            i.rect.y = -100
        for i in aster:
            i.rect.x = randint(0, 500)
            i.rect.y = -100
        player.rect.x = 320
        player.rect.y = 400
        over.stop()
    if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                kd = font1.render('Перезарядка...', 1, (255, 255, 0))
                window.blit(kd, (320, 400))
            else:
                num_fire = 0
                rel_time = False
    display.update()
    clock.tick(FPS)
