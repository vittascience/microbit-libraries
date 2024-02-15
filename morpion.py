"""
MicroPython for micro:bit game on display
https://github.com/vittascience/microbit-libraries

MIT License
Copyright (c) 2020 Léo Meillier (leomlr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from oled_mp import OLEDM
class MORPION(OLEDM):
  def __init__(self,s):
    self._s=s
    self.x,self.y,self.T=0,0,[[0,0,0],[0,0,0],[0,0,0]]
    self.clear()
    self.setTitle()
    self.setGrid()
    self.setCursor()
  def setGrid(self):
    for i in range(16,48):
      for j in range(1,31):
        if i==26 or i==37 or j==10 or j==21:self.set_px(i,j,1)
  def setCursor(self,d=1):
    for i in range(2):
      for j in range(1,-1,-1):self.set_px(20+self.y*11+i,26-self.x*11+j,d)
  def mvCursor(self):
    if self.T[self.x][self.y]!='X':self.setCursor(d=0)
    if self.x!=2:self.x+=1
    else:
      self.x=0
      if self.y!=2:self.y+=1
      else:self.y=0
    self.setCursor()
  def addCross(self):
    if self.T[self.x][self.y]==0:
      for n in range(8):self.set_px(24+self.y*11-n,23-self.x*11+n,1)
      for n in range(8):self.set_px(17+self.y*11+n,23-self.x*11+n,1)
      self.T[self.x][self.y]='X'
  def addCircle(self):
    C=[[-4,-1],[-4,0],[-4,1],[-4,2],[-3,3],[-2,4],[-1,4],[0,4],[1,4],[2,3],[3,2],[3,1],[3,0],[3,-1],[2,-2],[1,-3],[0,-3],[-1,-3],[-2,-3],[-3,-2]]
    if self.T[self.x][self.y]==0:
      for n in range(len(C)):self.set_px(21+self.y*11+C[n][0],26-self.x*11+C[n][1],1)
      self.T[self.x][self.y]='O'
  def newGame(self):
    self.x,self.y,self.T=0,0,[[0,0,0],[0,0,0],[0,0,0]]
    self.clear()
    self.setTitle()
    self.setGrid()
    self.setCursor()
  def endGame(self):
    for p in ['X','O']:
      for i in range(3):
        if self.T[i]==[p,p,p]:return self.setEnd()
        if self.T[0][i]==p and self.T[1][i]==p and self.T[2][i]==p:return self.setEnd()
      if self.T[0][0]==p and self.T[1][1]==p and self.T[2][2]==p:return self.setEnd()
      if self.T[0][2]==p and self.T[1][1]==p and self.T[2][0]==p:return self.setEnd()
      if 0 not in self.T[0] and 0 not in self.T[1] and 0 not in self.T[2]:return self.setEnd()
    return False
  def setTitle(self):
    l,n,v=[0,1,2,3],[0],[]
    C=[l,n,[0,1,2],n,l,v,l,[0,3],l,v,l,n,n,v,l,[0,2],[0,1,2],v,[0,2,3],v,l,[0,3],l,v,l,n,l]
    for i in range(len(C)):
      for j in range(len(C[i])):self.set_px(5+C[i][j],29-i,1)
    for i in range(30,1,-2):self.set_px(3,i,1)
    for i in range(2,31,2):self.set_px(10,i,1)
  def setEnd(self):
    l,v=[0,1,2,3,4],[]
    C=[l,[0,2,4],[0,4],v,l,[0],l,v,l,[0,4],[0,4],[1,2,3],v,v,[0,1,2,4]]
    for i in range(len(C)):
      for j in range(len(C[i])):self.set_px(53+C[i][j],22-i,1)
    return True
