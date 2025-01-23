#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
lost = 0
score = 0
max_lost = 3
life = 5
goal = 10
font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))



font2 = font.SysFont("Arial", 36)
#создай игру "

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65 ,65))
        self.speed = player_speed
        self.rect = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y =player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Enemy (GameSprite):
   def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1  

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, 15, 20, 15)
       bullets.add(bullet)



win_width = 700
win_height = 500
       
spacesilo = Player("rocket.png", 5, win_height - 100, 80, 100, 10)
finish = False
run = True

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40 , 80, 50, randint(1,5))
    monsters.add(monster)
    bullets = sprite.Group()
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("shooter")
background=transform.scale(image.load("vrgames.jpg"),(win_width,win_height))
game = True
finish = False

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy("asteroid.png", randint(80, win_width - 80), -40 , 80, 50, randint(1,5))
    asteroids.add(asteroid)

clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

rel_time = False
num_fire = 0


while run:
    
   
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire +1
                    spacesilo.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True    
            
    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счёт:"  + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))
       #производим движения спрайтов
        spacesilo.update()
        monsters.update()
        asteroids.update()
        monsters.draw(window)
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False        
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png" , randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(spacesilo, monsters, False) or sprite.spritecollide(spacesilo, asteroids, False):
            sprite.spritecollide(spacesilo,monsters, True)
            sprite.spritecollide(spacesilo,asteroids, True)
            life = life -1
            asteroid = Enemy("asteroid.png", randint(80, win_width - 80), -40 , 80, 50, randint(1,5))
            asteroids.add(asteroid)
            
        
        if score>= goal:
            finish = True
            window.blit(win, (200,200))
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


       #обновляем их в новом местоположении при каждой итерации цикла
        spacesilo.reset()
  

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for n in monsters:
            n.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy("ufo.png" , randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy("asteroid.png", randint(80, win_width - 80), -40 , 80, 50, randint(1,5))
            asteroids.add(asteroid)
    
   #цикл срабатывает каждые 0.05 секунд
    time.delay(50)
    clock.tick(FPS)
    display.update()
