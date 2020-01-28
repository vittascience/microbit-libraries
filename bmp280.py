from microbit import i2c
class BMP280:
  def __init__(self,addr=0x76):
    self.addr=addr
    self.s(0xF4,0x2F)
    self.s(0xF5,0x0C)
    self.T,self.P=0,0
  def sh(self,d):
    if d>32767:return d-65536
    else:return d
  def s(self,r,d):i2c.write(self.addr,bytearray([r,d]))
  def g(self,r):
    i2c.write(self.addr,bytearray([r]))
    return i2c.read(self.addr,1)[0]
  def h(self,r):
    i2c.write(self.addr,bytearray([r]))
    t=i2c.read(self.addr,2)
    return t[0]+t[1]*256
  def get(self):
    at=(self.g(0xFA)<<12)+(self.g(0xFB)<<4)+(self.g(0xFC)>>4)
    a=(((at>>3)-(self.h(0x88)<<1))*self.sh(self.h(0x8A)))>>11
    b=(((((at>>4)-self.h(0x88))*((at>>4)-self.h(0x88)))>>12)*self.sh(self.h(0x8C)))>>14
    self.T=(((a+b)*5+128)>>8)/100
    a=((a+b)>>1)-64000
    b=(((a>>2)*(a>>2))>>11)*self.sh(self.h(0x98))
    b=b+((a*self.sh(self.h(0x96)))<<1)
    b=(b>>2)+(self.sh(self.h(0x94))<<16)
    a=(((self.sh(self.h(0x92))*((a>>2)*(a>>2))>>13)>>3)+(((self.sh(self.h(0x90)))*a)>>1))>>18
    a=((32768+a)*self.h(0x8E))>>15
    if a==0:return
    p=((1048576-((self.g(0xF7)<<12)+(self.g(0xF8)<<4)+(self.g(0xF9)>>4)))-(b>>12))*3125
    if p<0x80000000:p=(p<<1)//a
    else:p=(p//a)*2
    a=(self.sh(self.h(0x9E))*(((p>>3)*(p>>3))>>13))>>12
    b=(((p>>2))*self.sh(self.h(0x9C)))>>13
    self.P=p+((a+b+self.sh(self.h(0x9A)))>>4)
    return [self.T,self.P]
  def Temperature(self):
    self.get()
    return self.T
  def Pressure(self):
    self.get()
    return self.P
  def Altitude(self):
    self.get()
    return 44330*(1-(self.P/101325)**(1/5.255))