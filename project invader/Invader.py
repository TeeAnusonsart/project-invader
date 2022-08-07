from msilib.schema import Class
import sys, pygame, pygame.mixer
from pygame.locals import *
import random

pygame.init()

size = width, height = 1200, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
background = pygame.image.load("spacebg.png").convert()
ship = pygame.image.load("spaceship.png").convert_alpha()
ship = pygame.transform.scale(ship, (64, 64))
bulletpicture = pygame.image.load("Bullet.png").convert_alpha()
bulletpicture = pygame.transform.scale(bulletpicture, (10,15))
enemy=pygame.image.load("enemy.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (64, 64))
enemybullet=pygame.image.load("enemybullet.png").convert_alpha()
enemybullet = pygame.transform.flip(enemybullet, False, True)
enemybullet=pygame.transform.scale(enemybullet, (32, 50))
shoot = pygame.mixer.Sound("shoot.wav")
hit= pygame.mixer.Sound("enemy_hit.wav")


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.helth=100
        self.rect=ship.get_rect()
    
    def update(self):
        self.rect.center = (self.x,self.y)
    
    

class Enemy:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.health=100
        self.rect = enemy.get_rect()

    def update(self):
        self.rect.center = (self.x,self.y)

    def hit(self,bulletrect):
        return self.rect.colliderect(bulletrect)
    


class EnemyBullet:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.rect = enemybullet.get_rect()

    def update(self):
        self.rect.center = (self.x,self.y)

    def hit(self,playerrect):
        return self.rect.colliderect(playerrect)

    def shoot(self,shoot):
        self.shoot=shoot


class Bullet:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect = bulletpicture.get_rect()

    def update(self):
        self.rect.center = (self.x,self.y)


def main():
    enemybullets=[]
    bullets = []
    enemys=[]
    timer_start = pygame.time.get_ticks()
    Level=0
    wave=0
    enemy_speed_x=1
    enemy_speed_y=2
    x=0
    y=0
    enemybullet_speed=3
    lost=False
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    def generate_enemys():
        enemy_count = 32
        enemy_colums = 8
        enemy_rows = 0

        for i in range(enemy_count):
            if(i % enemy_colums == 0):
                enemy_rows += 80
            enemys.append(
                Enemy(
                    (i % enemy_colums)*width/enemy_colums + width/enemy_colums/2 + 0,
                    enemy_rows-384)
                )
    
    def redraw():
        screen.blit(background, (0, 0))
        level_label = main_font.render(f"Level: {Level}", 1, (255,255,255))

        screen.blit(level_label, (width - level_label.get_width() - 10, 10))

    while True:
        redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                bullets.append(Bullet(event.pos[0], my))
                pygame.mixer.Sound.play(shoot)
            
        clock.tick(60)
        
        if lost==False:
            mx, my = pygame.mouse.get_pos()
        

        
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pressed = pygame.key.get_pressed()
        player=Player(mx,my)
        player.update()
        
        

        if len(enemys)==0:
            deltaTime=0
            timer_end = pygame.time.get_ticks()
            deltaTime = (timer_end - timer_start) / 1000
            y=0

            if deltaTime >8:
                Level+=1
                wave +=5
                for i in range(wave):
                    if Level % 3 == 0 :
                        enemys.append(Enemy(random.randint(64,1100),random.randint(-1000,-120)))
                for i in range(wave*2):
                    if Level % 3 == 2 :
                        enemys.append(Enemy(random.randint(-600,600),random.randint(-1500,-120)))
                
                if Level % 3 == 1:
                    generate_enemys()
                timer_start=timer_end+7000
                
        

        # update bullet position
        for bullet in bullets:
            bullet.y -= 10
            bullet.update()
            screen.blit(bulletpicture, bullet.rect)
            if bullet.y < 0:
                bullets.remove(bullet)

        x+=enemy_speed_x
        if x == 70 or x == -70:
            enemy_speed_x=-enemy_speed_x
            x=0
                

        # bullet collided with enemy
        for e in enemys:
            
            e.shoot=random.randint(1,100000)
            if Level %3 ==0 :
                    e.y+=2
                    e.update()
                    
            if Level %3 == 1:

                y+=enemy_speed_y

                if y<11000:
                    e.y+=enemy_speed_y

            
                e.x += enemy_speed_x

            if Level %3 ==2 :
                    e.y += 2
                    e.x += 1
                    
            e.update()
        
            for b in bullets:
                if(e.hit(b)):
                    enemys.remove(e)
                    bullets.remove(b)
                    pygame.mixer.Sound.play(hit)

                    
            if e.y > height:
                enemys.remove(e)
            if (e.hit(player)):
                enemys.remove(e)
                lost=True
            screen.blit(enemy, e.rect)


            if e.shoot>=99900-Level*2:
                enemybullets.append(EnemyBullet(e.x,e.y))

        for eb in enemybullets:
            eb.y+=enemybullet_speed
            eb.update()
            screen.blit(enemybullet,eb.rect)
            if (eb.hit(player)):
                enemybullets.remove(eb)
                lost=True

        if lost==True:
            lost_text = lost_font.render("GAME OVER PRESS R TO RESTART", 1, (255,255,255))
            screen.blit(lost_text,((width/2-lost_text.get_width()/2),350))
            #pressed = pygame.key.get_pressed()
            if pressed[pygame.K_r] :
                main()

            
        screen.blit(ship, (mx-32, my-32))
        pygame.display.flip()

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    while True:
        screen.blit(background, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

main_menu()