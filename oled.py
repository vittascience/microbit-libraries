from microbit import i2c,Image
from ustruct import pack_into
class OLED:
  def __init__(self):
    self._s=bytearray(513)
    self._s[0]=0x40
    C=[[0xAE],[0xA4],[0xD5,0xF0],[0xA8,0x3F],[0xD3,0x00],[0|0x0],[0x8D,0x14],[0x20,0x00],[0x21,0,127],[0x22,0,63],[0xa0|0x1],[0xc8],[0xDA,0x12],[0x81,0xCF],[0xd9,0xF1],[0xDB,0x40],[0xA6],[0xd6,1],[0xaf]]
    for c in C:i2c.write(0x3C,b'\x00'+bytearray(c))
  def set_pos(self,c=0,p=0):
    i2c.write(0x3C,b'\x00'+bytearray([0xb0|p]))
    c1,c2=c*2&0x0F,c>>3
    i2c.write(0x3C,b'\x00'+bytearray([0x00|c1]))
    i2c.write(0x3C,b'\x00'+bytearray([0x10|c2]))
  def clear(self):
    for i in range(1,513):self._s[i]=0
    self.set_pos()
    i2c.write(0x3C,self._s)
  def set_px(self,x,y,s=1,d=1):
    p,sp=divmod(y,8)
    i=x*2+p*128+1
    b=self._s[i]|(1<<sp) if s else self._s[i]&~(1<<sp)
    pack_into(">BB",self._s,i,b,b)
    if d:
      self.set_pos(x,p)
      i2c.write(0x3c,bytearray([0x40,b,b]))
  def addTxt(self,x,y,t,d=1):
    if y<4:
      for i in range(0,min(len(t),12-x)):
        for c in range(0,5):
          col=0
          for r in range(1,6):
              p=Image(t[i]).get_pixel(c, r - 1)
              col=col|(1<<r) if (p!=0) else col
          ind=x*10+y*128+i*10+c*2+1
          self._s[ind],self._s[ind+1]=col,col
      if d==1:
        self.set_pos(x*5,y)
        i2c.write(0x3C,b'\x40'+self._s[x*10+y*128+1:ind+1])
  def create_stamp(self,img):
    s=bytearray(5)
    for i in range(0,5):
      c=0
      for j in range(1,6):c|=(img.get_pixel(i,j-1)!=0)<<j
      s[i]=c
    return s
  def draw_stamp(self,x,y,stp,s=1,d=1):
    p,sp=divmod(y, 8)
    ind=(x<<1)+(p<<7)+1
    if ind>0:
      for c in range(0,5):
        i=ind+(c<<1)
        b=(self._s[i]|(stp[c]<<sp))if s else (self._s[i]&~(stp[c]<<sp))
        pack_into(">BB",self._s,i,b,b)
    ind+=128
    if ind<513:
      for c in range(0,5):
        i=ind+c*2
        b=(self._s[i]|(stp[c]>>(8-sp))) if s else self._s[i]&~(stp[c]>>(8-sp))
        pack_into(">BB",self._s,i,b,b)
    if d:
      o=2 if x!=0 else 0
      self.set_pos(x-(o>>1),p)
      i2c.write(0x3C,b'\x40'+self._s[ind-128-o:ind-116])
      if p<3:
        self.set_pos(x-(o>>1),p+1)
        i2c.write(0x3C,b'\x40'+self._s[ind-o:ind+14])