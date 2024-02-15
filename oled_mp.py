from microbit import i2c
from ustruct import pack_into
class OLEDM:
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
  def set_px(self,x,y,s,d=1):
    p,sp=divmod(y,8)
    i=x*2+p*128+1
    b=self._s[i]|(1<<sp) if s else self._s[i]&~(1<<sp)
    pack_into(">BB",self._s,i,b,b)
    if d:
      self.set_pos(x,p)
      i2c.write(0x3c,bytearray([0x40,b,b]))