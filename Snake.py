from sys import exit
from time import sleep
from copy import deepcopy
from random import randint

up = '\033[1A'
food = '🍎'
head = '◼ ️'
el = '⬛️'
wall = '⬜️'
space = '  '
zap = '⚡️'

class Field:
    def __init__(self, width, height):
        self.v = [[space for _ in range(width)] for _ in range(height)]
        self.w = width
        self.h = height
    
    def __str__(self):
        return (space+wall*(self.w+2)+'\n'+space+
            ('\n'+space).join(
                [wall+''.join(
                    line
                )+wall for line in self.v]
            )+
        '\n'+space+wall*(self.w+2)+('\n'+space*(self.w+3))*2+up*(self.h+4))
    
    def __getitem__(self, key):
        if not isinstance(key, tuple):
            return None
        return self.v[key[1]][key[0]]
    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            return
        #        y       x
        self.v[key[1]][key[0]] = value
    
    def copy(self):
        res = Field(self.w, self.h)
        res.v = deepcopy(self.v)
        return res

class Snake:
    def __init__(self,
            width=25, height=25, speed=5,
            foodLevel=None, length=None, finite=True,
            speedUp=1, chance=100, options=''):
        self.options = options
        self.chance= chance
        self.finite = finite
        self.foodLevel = foodLevel or int((width*height)**.125)
        self.speedUp = speedUp/10
        self.speed = speed
        self.width = width
        self.height = height
        self.field = Field(width, height)
        self.next = self.tempNext = 'up'
        self.active = 0
        x = (width+1)//2
        y = (height+1)//2
        self.keys = {
            'up':    ( 0,-1),
            'down':  ( 0, 1),
            'right': ( 1, 0),
            'left':  (-1, 0)
        }
        if length and length < 2:
            raise Exception('Snake must be longer')
        length = int(length or (width*height)**.25)
        self.points = length*self.speed
        self.body = [(x,y+i) for i in range(length)]
        for part in self.body:
            self.field[part] = el
        self.field[self.body[0]] = head
        self.generateFood()
        self.speed = speed
    
    def move(self):
        if self.active < 1: return
        if self.next != self.tempNext:
            for directions in (('up','down'),('left', 'right')):
                if self.tempNext in directions and self.next in directions:
                    self.tempNext = self.next
        self.next = self.tempNext
        dx, dy = self.keys[self.next]
        x, y = self.body[0]
        print(up*2,x,y,self.next,space*(self.width//2)+'\n'+space+f'Points:{int(self.points):3d}{space*((self.width-15)//2)}'+
            f'Size:{self.width:2d}x{self.height:2d}{space*((self.width-15)//2)}Speed: {self.speed}   ')
        if (self.finite and (
                not (0 <= x+dx < self.width) or not (0 <= y+dy < self.height)
                )) or self.body[0] in self.body[1:]:
            return self.restart(self.options)
        self.tail = self.body[-1]
        nextPos = (x+dx)%self.width, (y+dy)%self.height
        if self.field[nextPos] == food:
            self.body = [nextPos] + self.body
        else:
            self.body = [nextPos] + self.body[:-1]
            self.field[self.tail] = space
            if self.field[nextPos] == zap and len(self.body) > 2:
                half = (len(self.body)+1)//2
                for i in range(half, len(self.body)):
                    self.field[self.body[i]] = space
                self.body = self.body[:half]
        self.field[self.body[0]] = head
        self.field[self.body[1]] = el
        self.generateFood()

    def print(self):
        if self.active:
            print(self.field)
    
    def setnext(self, k):
        if not self.active:
            self.active = 1
        self.tempNext = k
    
    def generateFood(self):
        while str(self.field).count(food)+str(self.field).count(zap) < self.foodLevel:
            pos = self.body[0]
            while self.field[pos] not in (space,food):
                pos = (randint(1, self.width)-1, randint(1, self.height)-1)
            self.field[pos] = food if randint(1, self.chance) < self.chance else zap
            self.speed = round(self.speed+self.speedUp,4)
            self.points += self.speed
    
    def start(self):
        print(self.field)
        while True:
            sleep(1/abs(self.speed or 1))
            self.move()
            if self.active < 0:
                break
            self.print()
    
    def stop(self, text=' GAME OVER! ', end=True):
        self.active = -1 if end else not self.active
        half = (self.width+1-len(text)//2)//2
        print('\n'*(self.height+2)*end+space+el+el*half+text+el*half)
    
    def restart(self, options=''):
        self.stop(end=False)
        print(self.field)
        exec(f'self.__init__({options}, options="{options}")')
        print(up*2)
        self.active = 1
    
    def pause(self):
        self.active = not self.active
        print('\n'*(self.height+1))
        self.stop('GAME  PAUSED'+el, end=False)
        self.stop('Press p or any arrow key to continue', end=False)
        print(up*(self.height+5))
        return True

def main(default=''):
    options = input('Options: width=25, height=25, speed=5, foodLevel=1, length=5, finite=True, speedUp=1, chance=100\n')
    print(options)
    if options == '.exit':
        exit()
    elif not options:
        options = default
        #or 'finite=False, speed=3, speedUp=2, width=10, height=10, foodLevel=1, chance=10'
        #or 'foodLevel=10, speed=2, speedUp=1'
    return eval(f'Snake({options},options="{options}")')
