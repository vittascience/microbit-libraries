from microbit import i2c,sleep
class LCD1602:
  def __init__(self):
    self.fct=0x04|0x08
    sleep(50)
    i2c.write(0x3e,bytearray([0x80,0x20|self.fct]))
    sleep(4500)
    i2c.write(0x3e,bytearray([0x80,0x20|self.fct]))
    sleep(150)
    i2c.write(0x3e,bytearray([0x80,0x20|self.fct]))
    i2c.write(0x3e,bytearray([0x80,0x20|self.fct]))
    self.ctrl=0x04|0x02
    i2c.write(0x3e,bytearray([0x80,self.ctrl]))
    self.clear()
    self.mod=0x02|0x00
    i2c.write(0x3e,bytearray([0x80,0x04|self.mod]))
    self.display(True)
  def write_char(self,c):i2c.write(0x3e,bytearray([0x40,c]))
  def writeTxt(self,t):
    for c in t:self.write_char(ord(c))
  def cursor(self,s):
    if s:
      self.ctrl|=0x02
      i2c.write(0x3e,bytearray([0x80,0x08|self.ctrl]))
    else:
      self.ctrl&=~0x02
      i2c.write(0x3e,bytearray([0x80,0x08|self.ctrl]))
  def setCursor(self,x,y):
    x=(x|0x80) if y==0 else (x|0xc0)
    i2c.write(0x3e,bytearray([0x80,x]))
  def display(self,s):
    if s:
      self.ctrl|=0x04
      i2c.write(0x3e,bytearray([0x80,0x08|self.ctrl]))
    else:
      self.ctrl&=~0x04
      i2c.write(0x3e,bytearray([0x80,0x08|self.ctrl]))
  def clear(self):
    i2c.write(0x3e,bytearray([0x80,0x01]))
    sleep(2)
  def home(self):
    i2c.write(0x3e,bytearray([0x80,0x02]))
    sleep(2)