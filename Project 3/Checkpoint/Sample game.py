"""
Names: Soban and Sampada
This progrsm runs a game where user has to move the airplane with mouse clicks and shoot the minions by firing with right clicks.
If a minion hits the plane or a certain number of minions are missed, the program ends. The user wins if destroyed a certain number
of minions.
"""

from graphics import *
import time
import random
import sys

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SPEED = 10

class Minion:
    
    def __init__(self, x, y, speed, filename):
        
        self.dx = x
        self.dy = y
        self.speed = speed
        self.filename = filename
        self.minion = Image(Point(self.dx, self.dy), self.filename)
        
    def draw(self, win):
        
        self.minion.draw(win)
        
    def move(self):
        
        self.dy = self.speed
        self.minion.move(0, self.dy)
        
    def point(self):
        
        return self.minion.getAnchor()
        
    def undraw(self):
        self.minion.undraw()
        
class Airplane:
    
    def __init__(self, x, y, filename):
        
        self.dx = x
        self.dy = y
        self.filename = filename
        self.plane = Image(Point(self.dx, self.dy), self.filename)
    
    def draw(self, win):
        
        self.plane.draw(win)
        
    def move(self, point):
    
        self.dx = point.getX() - self.plane.getAnchor().getX() 
        self.plane.move(self.dx, 0)
        
def planemovement(plane, win):
    """
    This function controls the movement of plane left or right
    based on the returned coordinates of the mouse click.
    """
    point = win.checkMouse()
    if point != None:
        plane.move(point)
    
def setupMinions(win, speed, filename):
    """
    This function sets up minions and draws them on the window.
    """
    randx = random.randrange(WINDOW_WIDTH)
    randy = random.randrange(-10, 0)
    minion = Minion(randx, randy, speed, filename)
    minion.draw(win)
    return minion
    
def gameLoop(win, missed, listy):
    """
    This fucntion adds the animation to the window to make the minions fall
    and checks if any minion is missed and returns the count of missed minions.
    """
    for minion in listy:
        minion.move()
    for minion in listy:
        p = minion.point()
        if p.getY() > WINDOW_HEIGHT:
            minion.undraw()
            listy.remove(minion)
            missed = missed - 1
    return missed

def main():
    #draw window for the game
    win = GraphWin("Sample Game", WINDOW_WIDTH, WINDOW_HEIGHT, autoflush = False)
    win.setBackground("black")
    
    #add background to the window
    bg = Image(Point(400, 400), "bg.gif")
    bg.draw(win)
    
    #add instructions text for the game
    inst = Text(Point(400, 790), 'Use the left click to move the plane.')
    inst.setTextColor('yellow')
    inst.draw(win)
    
    #draw the plane and bullet in the window
    plane = Airplane(400, 710, 'airplane.gif')
    plane.draw(win)
    bullet = Image(Point(400, 400), 'bullet.gif')
    bullet.draw(win)
    
    listy = []
    missed = 0
    
    #draw a score label where score will be updated
    scoreLabel = Text(Point(700, 50), '0')
    scoreLabel.setTextColor('white')
    scoreLabel.draw(win)
    
    #keeping the loop true for the sake of checkpoint
    stance = True
    
    #loop to run the game
    while stance is True:
        
        #call the fucntion to move plane while the game is running
        planemovement(plane, win)
        
        #making a loop to control the drawing of minons by setting the probability to 5% per 0.1s
        if random.randrange(100) < 6:
            minion = setupMinions(win, SPEED, 'minion.gif')
            listy.append(minion)
        
        #calling the game loop fucntion to move the minions and check the score
        missed = gameLoop(win, missed, listy)
        
        #update score
        scoreLabel.setText(str(missed))
        time.sleep(.1)
    

main()