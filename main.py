import pygame
from pygame.locals import *
from pygamelib import *
import random


class Player:
    def __init__(self,size=20,pos=(pygame.Vector2(640.,360.)),color = (0,0,255),speed = 300):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = Rect(pos.x,pos.y,size,size)
        self.speed = speed
        self.chain = []
        self.actColecttable = RandomCollectable() 
        self.Points = 0
        self.direction = pygame.Vector2(0,0)
        self.last_pos = self.pos
        #self.movable = False
        pygame.time.set_timer(pygame.USEREVENT,25)
        
    def update_chain(self):
        self.chain.append(PlayerChain(pos=pygame.Vector2(self.pos.x - self.size,self.pos.y - self.size)))
    
    def update_rect(self):
        #self.rect = Rect(self.pos.x,self.pos.y,5,5)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.rect.colliderect(self.actColecttable.rect):
            self.eat(self.actColecttable)
        self.update_chain_rect()

    def Events(self,dt):
        for e in pygame.event.get():
         if e.type == pygame.USEREVENT: 
            if self.direction.x == 1:
                self.pos.x += self.speed * dt
            elif self.direction.x == -1:
                self.pos.x -= self.speed * dt
            if self.direction.y == 1:
                self.pos.y += self.speed * dt
            if self.direction.y == -1:
                self.pos.y -= self.speed * dt
                
                
           
    
    def update_pos(self,dt):
        
        keys = pygame.key.get_pressed()
        
        if self.pos.x >=1280 or self.pos.x <=0 or self.pos.y >=720 or self.pos.y <=0:
            self.DEAD()
       
        #elif self.clock_pos.get_time()>1000:
        #    print("One second has passed...")
       
        else:
            
            if keys[pygame.K_w]:
                #dprint('w')
                #self.pos.y -= self.speed * dt
                self.direction.y = -1
                self.direction.x = 0
            if keys[pygame.K_s]:
                #self.pos.y += self.speed * dt
                self.direction.y = 1
                self.direction.x = 0
            if keys[pygame.K_a]:
                #self.pos.x -= self.speed * dt
                self.direction.x = -1
                self.direction.y = 0
            if keys[pygame.K_d]:
                #self.pos.x += self.speed * dt
                self.direction.x = 1
                self.direction.y = 0
                
            #self.Events(dt)
            #self.update_chain_pos(dt)
            #self.update_chain_rect()
            self.update_rect()
    #Zrobić rekurencyjnie
    #Każde ogniwo ma swoją ostatnią pozycje i daje ją do elementu tablicy n+1 i pobiera ostatnią pozycję n-1
    def update_chain_pos(self,dt):
        if len(self.chain) >0:
            for j in range(len(self.chain)):
                i =self.chain[j]
                if i == 0:
                    i.last_pos = i.pos
                    i.pos = self.last_pos
                else:
                    i.last_pos = i.pos
                    i.pos = self.chain[j-1].pos
                print(i.pos)
        self.update_chain_rect()
        
        
                    
                    
    def update_chain_rect(self):
        if len(self.chain) >0:
            for i in self.chain:
                i.rect.x = i.pos.x
                i.rect.y = i.pos.y
        
    def draw(self,screen):
        if len(self.chain) >0:
            for i in self.chain:
                pygame.draw.rect(screen,i.color,i.rect)
        pygame.draw.rect(screen,self.color,self.rect)
        self.actColecttable.draw(screen)
        
    def eat(self,Collectable):
        self.update_chain()
        #Collectable.__del__()
        self.actColecttable = RandomCollectable()
        print("MNIAM,MNIAM")
        self.addPoints()
        self.update_chain()
    
    def addPoints(self):
        self.Points += 1
        print("Punkty: ",self.Points)
    
    def chain_colide_check():
        pass
        
    def DEAD(self):
        print("Przegrana!")
        pygame.quit()
        print("Przegrana!")
        

class PlayerChain:
    def __init__(self, size=20, pos=pygame.Vector2(640, 360), color=(0, 0, 255), speed=300):
        self.size = size
        self.pos = pos
        self.color = color
        self.rect = Rect(self.pos.x,self.pos.y,size,size)
        self.last_pos = self.pos

class Collectable:
    def __init__(self,size = 15,color = (255,0,0)):
        self.pos = pygame.Vector2(random.randrange(25,1200),random.randrange(25,695))
        self.size = size
        self.color = color
        self.rect = Rect(self.pos.x,self.pos.y,size,size)
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)



def RandomCollectable():
    a = Collectable(size=20)
    return a
    

class SnakeApp:
    def __init__(self,screenSize=(1280,720)):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode(screenSize)
    
    def show_grid(self):
            for i in range(60):
                pygame.draw.rect(self.screen,(255,0,0),pygame.Rect(1*i*25,0,1,720))    
                
            for i in range(45):
                pygame.draw.rect(self.screen,(255,0,0),pygame.Rect(1,i*25,1280,1))    
                
        
    def run(self):
        Mag = Player(size = 20,color=(255,255,255))
        while self.running:
            self.screen.fill('Black')
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
            if event.type == pygame.USEREVENT: 
                Mag.last_pos = Mag.pos
                if Mag.direction.x == 1:
                    Mag.pos.x += Mag.speed * self.dt
                elif Mag.direction.x == -1:
                    Mag.pos.x -= Mag.speed * self.dt
                if Mag.direction.y == 1:
                    Mag.pos.y += Mag.speed * self.dt
                if Mag.direction.y == -1:
                    Mag.pos.y -= Mag.speed * self.dt
                Mag.update_chain_pos(self.dt)
            #Fizyka i inne nauki ścisłe
            Mag.update_pos(self.dt)
                
            #pygame.draw.circle(self.screen,(0,0,255),pygame.Vector2(self.screen.get_width()/2,self.screen.get_height()/2),5)
            #self.show_grid()
            #Drawing
            
            Mag.draw(self.screen)
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            
                    
                    
a = SnakeApp()
a.run()