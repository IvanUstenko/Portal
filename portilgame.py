
import pygame
import os

class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = image_herodown
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 3
        self.health = 100
        self.inertia = 0
        self.drc = 'down'
        
 
    def move(self, keys, color):
        if s[pygame.K_a]:
            self.color_reactions(color)
            self.rect.x -= self.speed + self.inertia
            if self.rect.x < 0:
                self.rect.x = 0
            self.drc = 'left'
            self.image = image_heroleft
        elif s[pygame.K_d]:
            self.color_reactions(color)
            self.rect.x += self.speed + self.inertia
            if self.rect.x > 450:
                self.rect.x = 450
            self.drc = 'right'
            self.image = image_heroright 
        elif s[pygame.K_w]:
            self.color_reactions(color)
            self.rect.y -= self.speed + self.inertia
            if self.rect.y < 0:
                self.rect.y = 0
            self.drc = 'up'
            self.image = image_heroup
        elif s[pygame.K_s]:
            self.color_reactions(color)
            self.rect.y += self.speed + self.inertia
            if self.rect.y > 450:
                self.rect.y = 450
            self.drc = 'down'
            self.image = image_herodown
        else:
            self.inertia -= 0.1
            if self.inertia < 0:
                self.inertia = 0
            if self.drc == 'down':
                self.rect.y += self.inertia
                if self.rect.y > 450:
                    self.rect.y = 450
            if self.drc == 'up':
                self.rect.y -= self.inertia
                if self.rect.y < 0:
                    self.rect.y = 0
            if self.drc == 'right':
                self.rect.x += self.inertia
                if self.rect.x > 450:
                    self.rect.x = 450
            if self.drc == 'left':
                self.rect.x -= self.inertia
                if self.rect.x < 0:
                    self.rect.x = 0
        
    def color_reactions(self, color):
        if color == (255, 0, 255, 255):
            self.inertia += 0.1
            if self.inertia > 10:
                self.inertia = 10      
        if color == (255, 255, 2535, 255):
            self.inertia -= 0.1
            if self.inertia < 0:
                self.inertia = 0
        if color == (255, 0, 0, 255):
            self.inertia -= 0.2
            if self.inertia < -2:
                self.inertia = -2
                
class Portal(pygame.sprite.Sprite):
    def __init__(self, group, imageLeft, imageUp):
        super().__init__(group)
        self.image = imageLeft
        self.imageLeft = imageLeft
        self.imageUp = imageUp
        self.rect = self.image.get_rect()

    def set_PairPortal(self, Portal):
        self.PairPortal = Portal

    def teleport(self, hero):
        if self.PairPortal.rect.x == 0:
            X = 9
            hero.drc = 'right'
            hero.image = image_heroright
            hero.rect = image_heroright.get_rect()
        elif self.PairPortal.rect.x == 492:
            X = 439
            hero.drc = 'left'
            hero.image = image_heroleft
            hero.rect = image_heroleft.get_rect()
        else:
            X = self.PairPortal.rect.x
        if self.PairPortal.rect.y == 0:
            Y = 9
            hero.drc = 'down'
            hero.image = image_herodown
            hero.rect = image_herodown.get_rect()
        elif self.PairPortal.rect.y == 492:
            Y = 441
            hero.drc = 'up'
            hero.image = image_heroup
            hero.rect = image_heroup.get_rect()
        else:
            Y = self.PairPortal.rect.y
        hero.rect.x, hero.rect.y = X, Y
    def moving(self, hero):
        if hero.drc == 'left':
            self.image = self.imageLeft
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = hero.rect.y
        elif hero.drc == 'right':
            self.image = self.imageLeft
            self.rect = self.image.get_rect()
            self.rect.x = 492
            self.rect.y = hero.rect.y
        elif hero.drc == 'up':
            self.image = self.imageUp
            self.rect = self.image.get_rect()
            self.rect.y = 0
            self.rect.x = hero.rect.x
        elif hero.drc == 'down':
            self.image = self.imageUp
            self.rect = self.image.get_rect()
            self.rect.y = 492
            self.rect.x = hero.rect.x
    def update(self, btn, hero):
        if btn:
            self.moving(hero)
        if pygame.Rect.colliderect(hero.rect, self.rect):
            self.teleport(hero)               


class Escape(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = image_escapeon
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.status = 'opened'

    def open(self):
        self.image = image_escapeon
        self.status = 'opened'

    def close(self):
        self.image = image_escapeoff
        self.status = 'closed'

    def update(self, board, box, button, hero, escape):
        global now_level
        global levels
        if self.status == 'opened' and pygame.Rect.colliderect(hero.rect, self.rect):
            if now_level == 8:
                now_level = 0
                
            else:
                now_level += 1
            levels[now_level](board, box, button, hero, escape, port_or, port_blue)
        
        
        

class Box(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = image_box
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isSelected = False
    def update(self, isButtonPressed, heroRect):
        if isButtonPressed and pygame.Rect.colliderect(heroRect, self.rect):
            self.isSelected = not self.isSelected
            if self.isSelected:
                self.X = self.rect.x - heroRect.x
                self.Y = self.rect.y - heroRect.y
        if self.isSelected:
            self.rect.x, self.rect.y = heroRect.x + self.X, heroRect.y + self.Y
                
class Board:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.board = [[0] * heigth for _ in range(width)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
       
    def render(self):
        for i in range(0, self.heigth):
            for k in range(0, self.width):
                pygame.draw.rect(screen, (0, 0, 0), (self.left  + self.cell_size * i, self.top + self.cell_size * k, self.cell_size, self.cell_size), 00)
                if self.board[k][i] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (self.left  + self.cell_size * i, self.top + self.cell_size * k - 1, self.cell_size - 1, self.cell_size - 1), 0)
                elif self.board[k][i] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), (self.left  + self.cell_size * i, self.top + self.cell_size * k - 1, self.cell_size - 1, self.cell_size - 1), 0)
                else:
                    pygame.draw.rect(screen, (255, 0, 255), (self.left  + self.cell_size * i, self.top + self.cell_size * k - 1, self.cell_size - 1, self.cell_size - 1), 0)
            
    def get_coords(self, pos):
        a = pos[0]
        b = pos[1]
        if not(a // self.cell_size + 1 > self.width) and not(b // self.cell_size + 1 > self.heigth):
             return((a // self.cell_size, b // self.cell_size))
        else:
            return None

        

class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = image_buttonoff
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.changes = {}
        self.ispressed = False
        
    def pressed(self, board):
        for i in self.changes.keys():
            if i == 'escape_open':
                self.changes[i].open()
            else:
                board.board[i[0]][i[1]] = self.changes[i][1]
        self.ispressed = True
        self.image = image_buttonon
        return board
      
    def unpressed(self, board):
        for i in self.changes.keys():
            if i == 'escape_open':
                self.changes[i].close()
            else:
                board.board[i[0]][i[1]] = self.changes[i][0]
        self.ispressed = False
        self.image = image_buttonoff
        return board
        
# для создания нового уровня, надо создать функцию, создающая уровень. Ркомендуется называть её start_leveln, где n - номер уровня
# надо добавить новую функцию в список levels в главном блоке программы
# в классе Escape надо исправить блок:
#if now_level == n:
#    now_level = 0
#else:
    #now_level += 1
# в now_level == n, n должно равнятся кол-ву уровней минус 1
def start_leveltest(Board, box, button, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,1,1,1,1,0,0]#построение поля
    Board.board[1] = [0,0,0,0,1,1,1,1,0,0]#0 - белый цвет, стандартная панель
    Board.board[2] = [0,0,0,0,1,1,1,1,0,0]#1 - красный цвет, лава
    Board.board[3] = [0,0,0,0,1,1,1,1,0,0]#2 - фиолетовый цвет, ускоряющая панель
    Board.board[4] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[5] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[6] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[7] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[8] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[9] = [0,0,0,0,1,1,1,1,0,0]
    box.isSelected = False#
    box.rect.x = 200 #координаты коробки
    box.rect.y = 200
    button.rect.x = 100 #координаты кнопки
    button.rect.y = 100
    button.changes = {(3, 4) : [0, 2], 'escape_open':escape} #словарь, где вводятся изменения поля, при нажатие кнопки:
    #в круглых кноках вводятся координаты клетки, сначала в каком по номеру списке она находится, потом на каком месте стоит в этом списке
    #в квадратных скобках вводится сначала изначальное состояние клетки, потом которое должно быть после нажатия
    #если надо, чтобы при нажатии кнопки открывалась дверь, то вводится 'escape_open':escape
    hero.rect.x = 0 #изначальное положение персонажа
    hero.rect.y = 0
    escape.rect.x = 492 #координаты выхода
    escape.rect.y = 448
    port_or.rect.x = 0 #изначальное положение порталов
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
 
def start_End(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = -100
    escape.rect.y = -100
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('Вы прошли игру!!!', 1, (0, 255, 0))
    

def start_levelTutorial1(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('Для передвижения используются клавиши WASD\nЧтобы пройти на следующий уровень зайдите в голубую дверь', 1, (0, 255, 0))
    print('Для передвижения используются клавиши WASD\nЧтобы пройти на следующий уровень зайдите в голубую дверь')
    
def start_levelTutorial2(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('Нажмите ЛКМ, чтобы поставить синий портал\nНажмите ПКМ, чтобы поставить оранжевый портал\nЗаходя в синий портал, вы выходите из оранжевого и наоборот', 1, (0, 255, 0))
    print('Нажмите ЛКМ, чтобы поставить синий портал Нажмите ПКМ, чтобы поставить оранжевый портал Заходя в синий портал, вы выходите из оранжевого и наоборот')

def start_levelTutorial3(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,0,0,1,1,0,0,0,0,0]
    Board.board[6] = [0,0,0,1,1,0,0,0,0,0]
    Board.board[7] = [0,0,0,1,1,0,0,0,0,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('Красные клетки--ЛАВА\nЗаходя в неё вы будете замедляться\nЕсли остановитесь, то умрёте', 1, (0, 255, 0))
    print('Красные клетки--ЛАВА Заходя в неё вы будете замедляться Если остановитесь, то умрёте')
    
def start_levelTutorial4(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[1] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[2] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[3] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[4] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[5] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[6] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[7] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[8] = [0,0,0,2,2,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('Фиолетовые клетки--ускорители\nПопадая на них вы будете ускоряться', 1, (0, 255, 0))
    print('Фиолетовые клетки--ускорители\nПопадая на них вы будете ускоряться')
    
def start_levelTutorial5(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[1] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[2] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[3] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[4] = [2,2,2,2,2,1,1,0,0,0]
    Board.board[5] = [2,2,2,2,2,1,1,0,0,0]
    Board.board[6] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[7] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[8] = [0,0,0,2,2,1,1,0,0,0]
    Board.board[9] = [0,0,0,0,0,1,1,0,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('С помощью ускорения вы можете пробегать по лаве', 1, (0, 255, 0))
    print('С помощью ускорения вы можете пробегать по лаве')
    
def start_levelTutorial6(Board, box, button, hero, escape, port_or, port_blue):
    global text
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,0,0,0,0,0,0,0,0]
    box.isSelected = False
    box.rect.x = 400
    box.rect.y = 400
    button.rect.x = 450
    button.rect.y = 0
    button.changes = {'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 0
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    text = font.render('С помощью коробок вы можете нажимать на кнопки(желтые кружочки)\nЧтобы подобрать или отпустить коробку нажмите E\nЕсли дверь закрыта, то вокруг неё красный контур, иначе -- зелёный', 1, (0, 255, 0))
    print('С помощью коробок вы можете нажимать на кнопки(желтые кружочки). Чтобы подобрать или отпустить коробку нажмите E Если дверь закрыта, то вокруг неё красный контур, иначе -- зелёный')


def start_level1(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[1] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[2] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[3] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[4] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[5] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[6] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[7] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[8] = [0,0,0,0,1,1,1,1,0,0]
    Board.board[9] = [0,0,0,0,1,1,1,1,0,0]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level2(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [1,1,1,1,1,1,1,1,1,0]
    Board.board[2] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[3] = [1,1,1,1,1,1,1,1,1,0]
    Board.board[4] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[5] = [0,1,1,1,1,1,1,1,1,1]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [1,1,1,1,1,1,1,1,1,0]
    Board.board[8] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[9] = [0,0,1,1,1,1,1,1,1,1]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 0
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level3(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[1] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[2] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[3] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[4] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[5] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[6] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[7] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[8] = [0,0,0,1,1,1,0,0,0,0]
    Board.board[9] = [0,0,0,1,1,1,0,0,0,0]
    box.isSelected = False
    box.rect.x = 400
    box.rect.y = 400
    button.rect.x = 450
    button.rect.y = 0
    button.changes = {'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 0
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level4(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,1,1,1,1,0,0,0]
    Board.board[1] = [0,0,0,1,1,1,1,0,0,0]
    Board.board[2] = [0,0,0,1,1,1,1,0,0,0]
    Board.board[3] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[4] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[5] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[6] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[7] = [0,0,0,1,1,1,1,0,0,0]
    Board.board[8] = [0,0,0,1,1,1,1,0,0,0]
    Board.board[9] = [0,0,0,1,1,1,1,0,0,0]
    box.isSelected = False
    box.rect.x = 450
    box.rect.y = 450
    button.rect.x = 450
    button.rect.y = 0
    button.changes = {'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 0
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level5(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [2,2,2,2,2,2,2,2,2,2]
    Board.board[2] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[3] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[4] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[5] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[6] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[7] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[8] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[9] = [1,1,1,1,1,1,1,1,1,1]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 348
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
 
def start_level6(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,0,1,1,1,1,0]
    Board.board[1] = [0,0,0,0,0,1,1,1,1,0]
    Board.board[2] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[3] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[4] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[5] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[6] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[7] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[8] = [0,0,0,0,0,1,1,1,1,1]
    Board.board[9] = [0,0,0,0,0,1,1,1,1,1]
    box.isSelected = False
    box.rect.x = 150
    box.rect.y = 300
    button.rect.x = 450
    button.rect.y = 0
    button.changes = {(5,4):[0,2], (6,4):[0,2], (7,4):[0,2], (8,4):[0,2], (9,4):[0,2], (5,3):[0,2], (5,2):[0,2], (5,1):[0,2], (5,0):[0,2], 'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 248
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
 
def start_level8(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,1,1,0,0,2,1,2,2]
    Board.board[1] = [0,0,1,1,0,0,1,1,0,0]
    Board.board[2] = [1,1,0,0,1,2,0,0,1,1]
    Board.board[3] = [1,1,0,0,1,1,0,0,1,1]
    Board.board[4] = [0,0,1,1,0,0,1,1,0,0]
    Board.board[5] = [0,0,1,1,0,0,1,1,0,0]
    Board.board[6] = [1,1,0,0,1,1,0,0,1,1]
    Board.board[7] = [1,1,0,0,1,1,0,0,1,1]
    Board.board[8] = [0,0,1,1,0,0,1,1,2,2]
    Board.board[9] = [0,0,1,1,0,0,1,1,0,0]
    box.isSelected = False
    box.rect.x = 450
    box.rect.y = 50
    button.rect.x = 225
    button.rect.y = 225
    button.changes = {(4,2):[1,2],(5,2):[1,2],(4,3):[1,2],(5,3):[1,2],'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 450
    escape.rect.x = 0
    escape.rect.y = 223
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level7(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,0,0,0,0,0,0,0,0,0]
    Board.board[1] = [2,2,2,2,2,2,2,2,2,2]
    Board.board[2] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[3] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[4] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[5] = [0,1,1,1,1,1,1,1,1,1]
    Board.board[6] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[7] = [1,1,1,1,1,1,1,1,1,0]
    Board.board[8] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[9] = [1,1,1,1,1,1,1,1,1,1]
    box.isSelected = False
    box.rect.x = 0
    box.rect.y = 250
    button.rect.x = 450
    button.rect.y = 350
    button.changes = {(8,9):[1,2],(9,9):[1,2],'escape_open':escape}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0
    
def start_level9(Board, box, button, hero, escape, port_or, port_blue):
    Board.board[0] = [0,1,2,1,1,0,0,0,1,1]
    Board.board[1] = [0,1,2,1,0,1,0,1,0,1]
    Board.board[2] = [0,1,2,1,0,0,1,0,0,1]
    Board.board[3] = [0,1,2,1,0,1,0,1,0,1]
    Board.board[4] = [0,1,1,1,1,0,0,0,1,1]
    Board.board[5] = [0,1,1,1,1,1,1,1,1,1]
    Board.board[6] = [0,1,1,1,1,1,1,1,1,0]
    Board.board[7] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[8] = [1,1,1,1,1,1,1,1,1,1]
    Board.board[9] = [2,2,2,2,2,0,1,1,1,1]
    box.isSelected = False
    box.rect.x = -100
    box.rect.y = -100
    button.rect.x = -100
    button.rect.y = -100
    button.changes = {}
    hero.rect.x = 0
    hero.rect.y = 0
    escape.rect.x = 492
    escape.rect.y = 448
    port_or.rect.x = 0
    port_or.rect.y = 0
    port_blue.rect.x = 0
    port_blue.rect.y = 0  
    
    
 
 
def load_image(name, colorkey=(0,0,0)):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
board = Board(10, 10)
board.set_view(0, 0, 50)
running = True
image_heroright = load_image("hero_right.png")
image_heroleft = load_image("hero_left.png")
image_heroup = load_image("hero_up.png")
image_herodown = load_image("hero_under.png")
image_PortalBlueLeft = load_image('blue_portalleft.png')
image_PortalOrangeLeft = load_image('orange_portalleft.png')
image_PortalBlueUp = load_image('blue_portalup.png')
image_PortalOrangeUp = load_image('orange_portalup.png')
image_buttonoff = load_image("button_off.png")
image_buttonon = load_image("button_on.png")
image_box = load_image("Crate.png")
image_escapeon = load_image("escape_on.png")
image_escapeoff = load_image("escape_off.png")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
button = Button(all_sprites, 450, 0)
box = Box(all_sprites, 300,300)
escape = Escape(all_sprites, 492, 448)
port_or = Portal(all_sprites, image_PortalOrangeLeft, image_PortalOrangeUp)
port_blue = Portal(all_sprites, image_PortalBlueLeft, image_PortalBlueUp)
port_or.set_PairPortal(port_blue)
port_blue.set_PairPortal(port_or)
hero = Hero(all_sprites)
all_sprites.draw(screen)
font = pygame.font.Font(None, 13)
text = font.render('', 1, (0, 0, 255))
TextX,TextY = 0, 0
now_level = 0
levels = []
levels.append(start_levelTutorial1)
levels.append(start_levelTutorial2)
levels.append(start_levelTutorial3)
levels.append(start_levelTutorial4)
levels.append(start_levelTutorial5)
levels.append(start_levelTutorial6)

levels.append(start_level1)
levels.append(start_level2)
levels.append(start_level3)
levels.append(start_level4)
levels.append(start_level5)
levels.append(start_level6)
levels.append(start_level7)
levels.append(start_level8)
levels.append(start_level9)
#levels.append(start_leveln) - это надо прописать длядобавления нового уровня в список levels
levels[now_level](board, box, button, hero, escape, port_or, port_blue)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                port_blue.update(True, hero)
            elif event.button == 3:
                port_or.update(True, hero)
    coords = (hero.rect.x + 26, hero.rect.y + 25)
    s = pygame.key.get_pressed()
    if pygame.Rect.colliderect(hero.rect, button.rect) or pygame.Rect.colliderect(box.rect, button.rect):
        button.pressed(board) 
    else:
        button.unpressed(board)
    screen.fill((255,255,255))
    board.render()
    screen.blit(text, (TextX, TextY))
    port_or.update(False, hero)
    port_blue.update(False, hero)
    if hero.health == 0:
        hero.health = 100
        start_leveltest(board, box)
    hero.move(s, screen.get_at(coords))
    box.update(s[pygame.K_e], hero.rect)
    all_sprites.draw(screen)
    if hero.inertia == -2:
        levels[now_level](board, box, button, hero, escape, port_or, port_blue)
    escape.update(board, box, button, hero, escape)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
