from microbit import display,sleep
class GAME:
  def __init__(self):
    self.score=0
    self.endGame=True
    self.startGame()
  def startGame(self):
    self.score=0
    self.endGame=False
    display.clear()
    X=[2,2,2,2,3,4,4,4,3,1,0,0,0,1]
    Y=[0,1,2,4,4,3,2,1,0,0,1,2,3,4]
    for i in range(4):
      display.set_pixel(X[i],Y[i],9)
      sleep(200)
    for i in range(4,14):
      display.set_pixel(X[i],Y[i],9)
      sleep(50)
    sleep(1000)
    display.clear()
  def createSprite(self,x,y):return SPRITE(x,y)
  def stopGame(self):
    display.clear()
    display.scroll("GAME OVER")
    self.endGame=True
  def changeScore(self,n):
    self.score+=n
class SPRITE:
  def __init__(self,x,y):
    self.x=x
    self.y=y
    self.deleted=False
    self.display(True)
  def display(self,state):
    if self.x>=0 and self.x<=4:
      if state:display.set_pixel(self.x,self.y,9)
      else:display.set_pixel(self.x,self.y,0)
  def delete(self):
    self.display(False)
    self.deleted=True
  def move(self,direction,step):
    if not self.deleted:
      if direction=='left':
        self.display(False)
        self.x-=step
        if self.x<0:self.x+=5
        self.display(True)
      if direction=='right':
        self.display(False)
        self.x+=step
        if self.x>4:self.x-=5
        self.display(True)
      if direction=='up':
        self.display(False)
        self.y-=step
        if self.y<0:self.y+=5
        self.display(True)
      if direction=='down':
        self.display(False)
        self.y+=step
        if self.y>4:self.y-=5
        self.display(True)
