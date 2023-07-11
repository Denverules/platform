
import pygame as pg
import os
level=1
inventory=[]
vec = pg.math.Vector2 
pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()
ACC = 0.5
WIDTH=1920
HEIGHT=1080
class Enemy:
    def __init__(self, kill, hp, damage, speed):
        self.kill = kill
        self.hp = hp
        self.damage = damage
        self.speed = speed

FRIC = -0.1
rcount=0
lcount=0
class Player(pg.sprite.Sprite):

    def __init__(self):
        global lcount,rcount,change
        super().__init__()
        self.surf=leftgs[0]
        change=False

        self.rect = self.surf.get_rect()

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        global lcount,rcount,change
        if level==1 and not change:
            self.pos=vec((200,900))
            change=True
        elif level ==2 and not change:
            self.pos = vec((200, 200))
            change=True
        self.acc = vec(0, 0.3)
        self.surf=rightgs[0]
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_LEFT]:
            rcount=0
            if lcount==4:
                lcount=0
            elif lcount<=4:
                lcount+=1
            self.acc.x = -ACC
            for i in leftgs:
                if leftgs.index(i) == lcount:
                    self.surf = i
        if pressed_keys[pg.K_RIGHT]:
            self.acc.x = ACC
            lcount=0
            if rcount==4:
                rcount=0
            elif rcount <4:
                rcount += 1
            for i in rightgs:
                if rightgs.index(i) == rcount:
                    self.surf = i

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def update(self):
        global rcount,lcount
        hits = pg.sprite.spritecollide(p1, platforms, False)
        self.surf=leftgs[5]
        if p1.vel.y > 0:
            self.surf=leftgs[5]
            if not hits:
                self.surf=leftgs[5]
            else:
                self.move()
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def jump(self):
        hits = pg.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -10
    def win(self):
        global win,change
        hits=pg.sprite.spritecollide(self,wins,True)
        if hits:
            win=True
            change=False
def waitforclick():
    while True:
        for event in pg.event.get():
            if event.type ==pg.QUIT:
                quit()
            if event.type==pg.MOUSEBUTTONDOWN:
                return True

def waitforclickpos(minx,maxx,miny,maxy):
    while True:
        print('p')
        for event in pg.event.get():
            if event.type ==pg.QUIT:
                quit()
            mx,my=pg.mouse.get_pos()
            if event.type==pg.MOUSEBUTTONDOWN:
                if minx<=mx<=maxx and miny<=my<=maxy:
                    return True
def rectmaker(surface,x,y):
  a,b=surface.get_size()
  rectangle=pg.rect.Rect(x,y,a,b)
  return rectangle
def displayinv():
    global inventory,screen
    x=100
    for i in inventory:
        y = 200
        screen.blit(i, (x, y))
        x += 50
        if x >= 600:
            x = 100
            y += 100

assetpath='assets/'
empty=(0,0,0,0)
def assetloader(loaded,names,path,convert=True):
  empty=(0,0,0)
  for i in range(len(names)):
    if convert:
      image=str(names[i])+'.png'
      loaded.append(pg.image.load(os.path.join(path,image)).convert())
      loaded[i].set_colorkey(empty)
    else:
      image=str(names[i])+'.png'
      loaded.append(pg.image.load(os.path.join(path,image)))

runleft=['still','left1','left2','left3','left4','falling']
leftgs=[]
runright=['still','right1','right2','right3','right4']
rightgs=[]
assetloader(leftgs,runleft,'assets/character/run/',False)
assetloader(rightgs,runright,'assets/character/run/',False)
bgimgs=['sky']
bgs=[]
assetloader(bgs,bgimgs,'assets/')
ui=['paused','gameover','win','round','control']
uiimages=[]
assetloader(uiimages,ui,'assets/ui',False)
coordinates=[75,75]
moving=False
movement={pg.K_LEFT:[-10,0],pg.K_RIGHT:[10,0]
            ,pg.K_UP:[0,-10],pg.K_DOWN:[0,10]}
class Platform(pg.sprite.Sprite):
    def __init__(self,img,x,y):
        super().__init__()
        self.surf = img
        self.rect = self.surf.get_rect(center = (x,y))
tiles=[]
tilenames=['grass','door']
assetloader(tiles,tilenames,'assets/tiles')
p1=Player()

l1=[[1,1600,800],[0,200,900],[0,600,900],[0,700,650],[0,1000,650],[0,1200,900],[0,1600,900]]
level1=[]
for i in l1:
    xpos=i[1]
    ypos=i[2]
    plat=Platform(tiles[i[0]],xpos,ypos)
    level1.append(plat)
l2=[[1,1400,300],[0,300,400],[0,600,650],[0,800,850],[0,1100,650],[0,1400,400]]
level2=[]
for i in l2:
    xpos =i[1]
    ypos =i[2]
    plat=Platform(tiles[i[0]],xpos,ypos)
    level2.append(plat)
all_Sprites=pg.sprite.Group()
all_Sprites.add(p1)

platforms = pg.sprite.Group()

centre=(777,348)
wins=pg.sprite.Group()
wins.add(level1[0])
wins.add(level2[0])

def pause():
    while True:
        print('paused')
        screen.blit(uiimages[0],centre)
        pg.display.flip()
        if waitforclick():
            break
        else:
            print('p')
            screen.blit(uiimages[0],(0,0))
def fail():
    while True:
        screen.blit(bgs[0],(0,0))
        screen.blit(uiimages[1],centre)
        pg.display.flip()
        if waitforclick():
            pg.quit()
def Win():
    global level,win
    while True:
        screen.blit(bgs[0],(0,0))
        if level ==2:
            screen.blit(uiimages[2],centre)
            pg.display.flip()

        else:
            screen.blit(uiimages[3],centre)
            pg.display.flip()
        if waitforclick():
            if level==2:
                quit()
            level+=1
            win=False
            break

def playing():
    global win
    win=False
    global screen,coordinates,moving,movement
    control=False
    while True:
        p1.win()
        if level == 1:
            control=True
            for i in level1:
                platforms.add(i)
                all_Sprites.add(i)
        elif level == 2:
            control=False
            for i in level2:
                all_Sprites.add(i)
                platforms.add(i)
                all_Sprites.remove(level1)
                platforms.remove(level1)
        elif level ==3:
                Win()


        for event in pg.event.get():
            if event.type ==pg.QUIT:
                quit()
            if event.type==pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_UP]:
                    p1.jump()
                elif pg.key.get_pressed()[pg.K_ESCAPE]:
                    pause()
            if event.type==pg.MOUSEBUTTONDOWN:
                print(pg.mouse.get_pos())
        screen.blit(bgs[0],(0,0))
        if control:
            screen.blit(uiimages[4],(300,200))
        if win:
            Win()
        p1.move()
        p1.update()
        if p1.pos[1]>1080:
            fail()
        for entity in all_Sprites:
            screen.blit(entity.surf,entity.rect)

        pg.display.update()
        clock.tick(30)


running = True
playing()



