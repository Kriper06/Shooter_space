from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound=mixer.Sound("fire.ogg")
img_back="galaxy.jpg"
img_hero="rocket.png"
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(player_image),(size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet("bul.png", self.rect.centerx, self.rect.top, 15,30,10)
        bullets.add(bullet)
lose=0
class Enemy(GameSprite):
    def update(self):
        global lose
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lose+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=30
        if self.rect.y<0:
            self.kill()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monsters.add(Enemy("ufo.png", randint(100, 600), 0, 65, 65, randint(5,10)))
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background=transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
font.init()
font1=font.Font("arial.ttf",36)
finish = False
run = True
score=0
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                ship.fire()

    sprites_list=sprite.groupcollide(monsters,bullets,True,True)
    for s in sprites_list:
        score+=1
        monsters.add(Enemy("ufo.png", randint(80,620),0,65,65,randint(1,5)))

    if lose>3 or sprite.spritecollide(ship,monsters, True):
        finish=True
        losing=font1.render("You lose",1,(255,0,0))
        window.blit(losing,(150,150))

    if not finish:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose=font1.render("Пропущено: "+str(lose), 1, (255, 255, 255))
        window.blit(text_lose,(10,50))
        text_score=font1.render("Повержено: "+str(score), 1, (255, 255, 255))
        window.blit(text_score,(10,25))
    display.update()
    time.delay(50)