#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://hi-im.laria.me/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (me@laria.me)
# or leave a comment on this gist.

# Very simple tetris implementation
# 
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.




fp = open("/home/shailesh/Desktop/pyTet/hiScores",'r');      #opening high score file
l = fp.readlines();
fp.close()
stt=''
l = [int(i) for i in l]						#creating a list consisting of the lines of the file(scores) as elements

def hiScoreString(lst):						#returns the string which is to be displayed on the screen
	st = ""
	for i in range(3):
		st+=(str(i+1)+") "+str(lst[-(i+1)])+"\n")
	return st
def fileString(lst):						#returns the string which is to be written to the file
	st = ""
	for i in range(3):
		st+=(str(lst[i])+"\n")
	#st = st[:-1]
	return st

class Node:
 
    # Function to initialise the node object
    def __init__(self, data):
        self.data = data  # Assign data
        self.next = None  # Initialize next as null
 
 
# Linked List class contains a Node object
class LinkedList:
 
    # Function to initialize head
    def __init__(self,size):
        self.size = size
        self.head = None

#shapes linked lists
#T shape
Tl=LinkedList(4)
Tl.head=Node([[1, 1, 1],
     [0, 1, 0]])
Tl.head.next=Node([[1,0],
                   [1,1],
                   [1,0]])
Tl.head.next.next=Node([[0, 1, 0],
     [1, 1, 1]])
Tl.head.next.next.next=Node([[0,1],
                   [1,1],
                   [0,1]])
Tl.head.next.next.next.next=Tl.head #reset

#inverse Z shape
inZl=LinkedList(2)
inZl.head=Node([[0, 2, 2],
     [2, 2, 0]])
inZl.head.next=Node([[2,0],
                     [2,2],
                     [0,2]])
inZl.head.next.next=inZl.head

#Z shape
Zl=LinkedList(2)
Zl.head=Node([[3, 3, 0],
     [0, 3, 3]])
Zl.head.next=Node([[0,3],
                   [3,3],
                   [3,0]])
Zl.head.next.next=Zl.head #reset

#L shape
L=LinkedList(4)
L.head=Node([[4, 0, 0],
     [4, 4, 4]])
L.head.next=Node([[0,4],
                  [0,4],
                  [4,4]])
L.head.next.next=Node([[4, 4, 4],
                       [0, 0, 4]])
L.head.next.next.next=Node([[4,4],
                  [4,0],
                  [4,0]])
L.head.next.next.next.next=L.head #reset

#inverse L shape
inL=LinkedList(4)
inL.head=Node([[0, 0, 5],
     [5, 5, 5]])
inL.head.next=Node([[5,5],
                  [0,5],
                  [0,5]])
inL.head.next.next=Node([[5, 5, 5],
                         [5,0,0]])
inL.head.next.next.next=Node([[5,0],
                  [5,0],
                  [5,5]])
inL.head.next.next.next.next=inL.head #reset

#straight line
ll=LinkedList(2)
ll.head=Node([[6, 6, 6, 6]])
ll.head.next=Node([[6],
                   [6],
                   [6],
                   [6]])
ll.head.next.next=ll.head #reset

#box shape
box=LinkedList(1)
box.head=Node([[7, 7],
     [7, 7]])
box.head.next=box.head #reset

#end of shape definitions with all rotations linked in anticlockwise rotation order

from random import randrange as rand
import pygame, sys

# The configuration
cell_size =	40
cols =		10
rows =		22
maxfps = 	30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) #color table for background grid
]

# Define the shapes of the single parts
tetris_shapes = [Tl,inZl,Zl,L,inL,ll,box]


def rotate_anticlockwise(shape):				#Anticlockwise
 return shape.next.data

def check_collision(board, shape, offset):        #offset = [x,y] where x and y denote coordinates of top left block of shape
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):            #These two lines are iterating across squares of 'shape'
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]: #at a position of 'shape' where a block is filled, if the board is also filled
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]                                #deletes particular row
    return [[0 for i in xrange(cols)]] + board	#adds an empty row to the top so that dimensions of board remain constant

def join_matrixes(mat1, mat2, mat2_off):                # when shape falls, this function merges already existent dropped blocks and blocks of shape
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1	][cx+off_x] += val      #-1 is because, after seeing that a collision occurs, shaped is moved back one stepward and then joining occurs
    return mat1

def new_board():										#creates new board entirely
    board = [ [ 0 for x in xrange(cols) ]
            for y in xrange(rows) ]
    board += [[ 1 for x in xrange(cols)]]
    return board

class TetrisApp(object):
    def __init__(self):
        pygame.init()									#initializes all imported pygame submodules
        pygame.key.set_repeat(250,25)	#enables repeated keyboard input, first parameter is delay in ms after first key is pressed,second denotes interval between read of successive keypresses
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]        #setting alternate black and grey pattern of board

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))      #initializes display of required height and width
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        k=rand(len(tetris_shapes))
        self.next_rock_head = tetris_shapes[k].head
        self.next_rock = tetris_shapes[k].head.data
        self.init_game()

    def new_rock(self):
        self.rock = self.next_rock[:]					#
        self.rock_head = self.next_rock_head
        k = rand(len(tetris_shapes))
        self.next_rock_head = tetris_shapes[k].head
        self.next_rock = tetris_shapes[k].head.data
        self.rock_x = int(cols / 2 - len(self.rock[0])/2)             #rock_x refers to x coordinate of starting position of shape, initialized to middle column of board
        self.rock_y = 0						#rock_x refers to the y coordinate of the starting position of shape, initialized to top row

        if check_collision(self.board,
                           self.rock,
                           (self.rock_x, self.rock_y)):
            self.gameover = True				#if a collision occurs as soon as the shape is initialized, then gameover

    def init_game(self):                   #new game
        self.board = new_board()
        self.new_rock()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 500)         #USEREVENT occurs repeatedly after a time of 1000ms

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():                            #splitlines() splits msg with the delimiter '\n'
            self.screen.blit(				#blit draws something on the display screen
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),			#Hence msg is drawn out on the screen at the position (x,y)
                    (0,0,0)),
                (x,y))
            y+=14						#moves onto next line

    def center_msg(self, msg): #displays message in center of screen
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22 - 100))

    def draw_matrix(self, matrix, offset):              #draws shape at required position
        off_x, off_y  = offset      #(off_x,off_y) is position of top left corner of shape
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(          #draws a rectangle of color specified by colors[val] ( each block has a unique color specified by a number value in tetris_shapes
                        self.screen,
                        colors[val],
                        pygame.Rect(	   			#defines a rectangular area of desired size, which is to be drawn
                            (off_x+x) *			#Here a square is defined and drawn for each iteration, resulting #in the final shape
                              cell_size,
                            (off_y+y) *
                              cell_size,
                            cell_size,
                            cell_size),0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level			#adds points depending on number of rows cleared(deleted)
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 500-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.rock_x + delta_x			#moves shape by delta_x
            if new_x < 0:					#
                new_x = 0				#doesn't allow movement outside board
            if new_x > cols - len(self.rock[0]):		#
                new_x = cols - len(self.rock[0])	#
            if not check_collision(self.board,
                                   self.rock,
                                   (new_x, self.rock_y)):
                self.rock_x = new_x			#if no collision, replace shape with original position by new shape
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()				#updates screen after changes have been made to it, similar to plt.show()
        sys.exit()

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.rock_y += 1			#moves ycoordinate of rock to next row
            if check_collision(self.board,
                               self.rock,
                               (self.rock_x, self.rock_y)):
                self.board = join_matrixes(     #if collision, join board and shape starting at (rock_x,rock_y)
                  self.board,
                  self.rock,
                  (self.rock_x, self.rock_y))
                self.new_rock()		#as old rock is no longer usable, new rock is created
                cleared_rows = 0		#number of cleared rows in this turn is set to zero
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:				#checks if not even one empty spot in row
                            self.board = remove_row(		# if so, row is deleted
                              self.board, i)
                            cleared_rows += 1			#number of cleared rows in this turn is incremented
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)                                #passes number of cleared rows to add_cl_lines in order to change the score
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):		#function is called every iteration and hence rock drops continuously without user input until a collision
                pass

    def rotate_rock(self):
        if not self.gameover and not self.paused:
            new_rock = rotate_anticlockwise(self.rock_head)
            if not check_collision(self.board,
                                   new_rock,
                                   (self.rock_x, self.rock_y)):
                self.rock_head = self.rock_head.next
                self.rock = new_rock

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
	global l;
        key_actions = {
            'ESCAPE':	self.quit,
            'LEFT':		lambda:self.move(-1),
            'RIGHT':	lambda:self.move(+1),
            'DOWN':		lambda:self.drop(True),
            'UP':		self.rotate_rock,
            'p':		self.toggle_pause,
            'SPACE':	self.start_game,
            'RETURN':	self.insta_drop
        }

        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()           #initializing a clock it has a maxfps rate, and is hence caled dont burn my cpu
        while 1:
	
            self.screen.fill((0,0,0))			#gives screen a default black colour
            if self.gameover:
		if flag==0:
			stt=''
			if l[0]<self.score:
				stt = "Congrats! New High Score!!!"
				l[0] =self.score               #replaces lowest hiscore value in l with new score if new score is greater
			l.sort()
			flag=1;

                self.center_msg("""Game Over!\nYour score: %d
Press space to continue\n""" % self.score + stt +"\nHigh scores are:\n"+ hiScoreString(l))
		fp = open("/home/shailesh/Desktop/pyTet/hiScores",'w');
		fp.write(fileString(l));                        #writes new hiscores to file
		fp.close()
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
		    flag = 0;							#
                    pygame.draw.line(self.screen,			#
                        (255,255,255),				#
                        (self.rlim+1, 0),			#
                        (self.rlim+1, self.height-1))		#draws display column on right of board
                    self.disp_msg("Next:", (			#
                        self.rlim+cell_size,			#
                        2))					#
                    self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0)) #draws black background grid
                    self.draw_matrix(self.board, (0,0))		#draws board
                    self.draw_matrix(self.rock,			#draws shape
                        (self.rock_x, self.rock_y))
                    self.draw_matrix(self.next_rock,		#draws next shape to come in the display column
                        (cols+1,2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:			
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()					#quits game under quit condition
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                        +key):					#if any key is pressed, an action is performed according to key_actions dictionary
                            key_actions[key]()

            dont_burn_my_cpu.tick(maxfps)					#setting maxfps rate for clock

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
