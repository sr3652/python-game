"""
Names: Soban and Sampada
CSC 201
Programming Project 3

This progrsm runs a game where user has to move the airplane with mouse clicks and shoot the minions by firing with right clicks.
If a minion hits the plane or a certain number of minions are missed, the program ends. The user wins if destroyed a certain number
of minions.

Assistance:
    Our pair gave and received no assistance on this project.
"""

from graphics import *
import time
import random
import sys
import math

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SPEED = 5
BULLET_SPEED = 20
NUM_WIN = 20

class Air:
    def __init__(self, x1, y1, x2, y2, speed):
        self.dx1 = x1
        self.dy1 = y1
        self.dx2 = x2
        self.dy2 = y2
        self.rect = Rectangle(Point(self.dx1, self.dy1), Point(self.dx2, self.dy2))
        self.rect.setFill('gray')
        self.speed = speed

    def draw(self, win):
        
        self.rect.draw(win)
        
    def move(self):
        if self.rect.getCenter().getY() > WINDOW_HEIGHT:
            self.dy = -WINDOW_HEIGHT
        else:
            self.dy = self.speed
        self.rect.move(0, self.dy)

class Bullet:
    def __init__(self, speed, point, filename):
        self.dx = point.getX()
        self.dy = point.getY()
        self.speed = speed
        self.filename = filename
        self.bullet = Image(Point(self.dx, self.dy - 90), filename)
    
    def draw(self, win):
        self.bullet.draw(win)
        
    def move(self):
        self.bullet.move(0, -self.speed)
        
    def center(self):
        return self.bullet.getAnchor()
    
    def width(self):
        return self.bullet.getWidth()
    
    def undraw(self):
        self.bullet.undraw()


class Minion:
    
    def __init__(self, x, speed, filename):
        
        self.dx = x
        self.dy = -10
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
    
    def center(self):
        return self.minion.getAnchor()
    
    def width(self):
        return self.minion.getWidth()
        
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
        
    def center(self):
        return self.plane.getAnchor()
    
    def width(self):
        return self.plane.getWidth()

def drawImg(x, y, filename, win):
    '''
    Draws Image object on the Graphwin window
    and returns it to the variable.
    '''
    img = Image(Point(x, y), filename)
    img.draw(win)
    return img

def drawText(x, y, string, color, win, size = 12):
    '''
    Draws text object on the Graphwin window
    and returns it to the variable.
    '''

    text = Text(Point(x, y), string)
    text.setTextColor(color)
    text.setSize(size)
    text.draw(win)
    return text
    
def distanceBetweenPoints(point1, point2):
    '''
    Calculates the distance between two points
    
    Params:
    point1 (Point): the first point
    point2 (Point): the second point
    
    Returns:
    the distance between the two points
    '''
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x)*(p1x - p2x) + (p1y - p2y) * (p1y - p2y))

def isCloseEnough(obj1, obj2):
    '''
    Determines if the bullet/plane and minion are close enough to say the plane shot the minion or
    minion attacked the plane
    
    Params:
    obj1: the image of the bullet or plane
    obj2: the image of one particular minion
    
    Returns:
    True if distance between the center of the bullet/plane and the center of the minion is less than a
    threshold to say the minion was shot or the plane got attacked. Otherwise, it returns False.
    '''
    threshold = obj1.width() * 0.5 + obj2.width() * 0.5
    distance = distanceBetweenPoints(obj1.center(), obj2.center())
    return distance < threshold

def planemovement(plane, win):
    """
    This function controls the movement of plane left or right
    based on the coordinates of the mouse click.
    """
    point = win.checkMouse()
    if point != None:
        plane.move(point)
    
def setupMinions(win, speed, filename):
    """
    This function sets up minions and draws them on the window.
    """
    randx = random.randrange(WINDOW_WIDTH)
    minion = Minion(randx, speed, filename)
    minion.draw(win)
    return minion

def setupBullet(win, speed, point, filename):
    """
    This function sets up bullets and draws them on the window.
    Returns the bullet object to the variable.
    """
    
    bullet = Bullet(speed, point, filename)
    bullet.draw(win)
    return bullet

def setupAir():
    """
    This function sets up fire and draws them on the window
    Returns a list of all the air objects.
    """
    airList = []
    for i in range(30):
        x1 = random.randrange(WINDOW_WIDTH)
        y1 = random.randrange(WINDOW_HEIGHT)
        x2 = x1 + 3
        y2 = y1 + 20
        air = Air(x1, y1, x2, y2, 50)
        airList.append(air)
    return airList
    
def instructions(win):
    """
    Draws all the instructions on the Graphwin window.
    """
    
    button = drawImg(400, 400, 'button.gif', win)
    ins1 = drawText(400, 580, f'You need to kill {NUM_WIN} minions in order to win the game.', 'yellow', win)
    ins2 = drawText(400, 600, 'Use the left click to move the plane on the window and UP arrow key to shoot.', 'yellow', win)
    ins3 = drawText(400, 620, 'You loose if even a single minion runs into your plane. Be careful!.', 'yellow', win)
    ins4 = drawText(400, 400, 'Click to Start!', 'black', win, 30)
    win.getMouse()
    ins1.undraw()
    ins2.undraw()
    ins3.undraw()
    ins4.undraw()
    button.undraw()
    
def gameLoop(win):
    """
    This fucntion runs the animation in the window to make the minions fall and checks if
    any minion is missed or shot or the plane is attacked and calculates the score. Also
    gives the final result.
    """
    bulletList = []
    minionList = []
    score = 0
    
    #draw a score label where score will be updated
    scoreLabel = drawText(700, 50, '0', 'yellow', win, 15)
    airList = setupAir()
    for air in airList:
        air.draw(win)
    
    #drawing the plane
    plane = Airplane(400, 710, 'airplane.gif')
    plane.draw(win)
        
    planecrash = False
    
    #loop to run the game
    while score < NUM_WIN and planecrash == False:
        
        #move the air in the game
        for air in airList:
            air.move()
            
        #making a loop to control the drawing of minons by setting the probability to 5% per 0.1s
        if random.randrange(100) < 6:
            minion = setupMinions(win, SPEED, 'minion.gif')
            minionList.append(minion)
        
        
        #call the function to move plane while the game is running
        planemovement(plane, win)
        
        #check key pressed for fire
        keyPressed = win.checkKey()
        if keyPressed != '':
            if keyPressed == 'Up':
                bullet = setupBullet(win, BULLET_SPEED, plane.center(), 'bullet.gif')
                bulletList.append(bullet)
        
        #move the minion        
        for minion in minionList:
            minion.move()
        
        #move the bullet
        for bullet in bulletList:
            bullet.move()
        
        #looping through each minion
        for minion in minionList:
            p = minion.point()
            
            #checks if this minion has skipped the window
            if p.getY() > WINDOW_HEIGHT + 25:
                minion.undraw()
                minionList.remove(minion)
                score = score - 1
                scoreLabel.setText(str(score))
                
            #looping throught each bullet    
            for bullet in bulletList:
                
                #checks if this bullet hits this minion 
                if isCloseEnough(bullet, minion):
                    minion.undraw()
                    minionList.remove(minion)
                    bullet.undraw()
                    bulletList.remove(bullet)
                    score = score + 1
                    scoreLabel.setText(str(score))
                    
            #checks if this minion hits the plane  
            if isCloseEnough(plane, minion):
                planecrash = True
                
        #updates the score
        scoreLabel.setText(str(score))    
        time.sleep(.05)

    if planecrash == True:
        
        loose1 = drawImg(400, 400, 'loosemid.gif', win)
        loose2 = drawImg(300, 350, 'looseleft.gif', win)
        loose3 = drawImg(500, 350, 'looseright.gif', win)
        drawText(400, 600, "Game over, you lose!", 'yellow', win, 25)
        time.sleep(3)
        sys.exit(-1)
        
    if score == NUM_WIN:
        
        win1 = drawImg(400, 400, 'winmid.gif', win)
        win2 = drawImg(280, 400, 'winleft.gif', win)
        win3 = drawImg(520, 400, 'winright.gif', win)
        drawText(400, 600, f'You killed {NUM_WIN} minions. You win!', 'yellow', win, 25)
        
    time.sleep(3)
        
def main():
    
    #draw window for the game
    win = GraphWin("Shoot The Minions!", WINDOW_WIDTH, WINDOW_HEIGHT)
    win.setBackground("black")
    
    #add background to the window
    bg = drawImg(400, 400, "background.gif", win)
    
    #call the instructions function
    instructions(win)
    
    #call the main game function to commence the game
    gameLoop(win)
    
    #close the game
    win.close()
    
if __name__ == "__main__":
    main()