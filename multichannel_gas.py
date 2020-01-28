from microbit import i2c,sleep
from math import pow
class GAS:
  b1=0
  b2=0
  b3=0
  def __init__(self):
    self.cmd([10,1])
    sleep(1000)
    self.cmd([10,0])
  def cmd(self,cmd,n=2):
    i2c.write(0x04,bytes(cmd))
    dta=0
    raw=i2c.read(0x04,n)
    for byte in raw:dta=dta*256+int(byte)
    if cmd==1:
      if dta>0:self.b1=dta
      else:dta=self.b1
    elif cmd==2:
      if dta>0:self.b2=dta
      else:dta=self.b2
    elif cmd==3:
      if dta>0:self.b3=dta
      else:dta=self.b3
    return dta
  def power_on(self):self.cmd([11,1])
  def power_off(self):self.cmd([11,0])
  def get_gas(self,g):
    self.cmd([10,1])
    a0=self.cmd([6,8])
    a1=self.cmd([6,10])
    a2=self.cmd([6,12])
    n0=self.cmd([1])
    n1=self.cmd([2])
    n2=self.cmd([3])
    r0=n0/a0*(1023.0-a0)/(1023.0-n0)
    r1=n1/a1*(1023.0 - a1)/(1023.0-n1)
    r2=n2/a2*(1023.0-a2)/(1023.0-n2)
    c=0.0
    if g==0:c=pow(r1,-1.179)*4.385
    elif g==1:c=pow(r2,1.007)/ 6.855
    elif g==2:c=pow(r0,-1.67)/1.47
    elif g==3:c=pow(r0,-2.518)*570.164
    elif g==4:c=pow(r0,-2.138)*398.107
    elif g==5:c=pow(r1,-4.363)*630.957
    elif g==6:c=pow(r1,-1.8)*0.73
    elif g==7:c=pow(r1,-1.552)*1.622
    self.cmd([10,0])
    return c or -3
  def calibrate(self):
    while True:
      a0=self.cmd(1)
      a1=self.cmd(2)
      a2=self.cmd(3)
      self.cmd([10,1])
      cnt = 0
      for i in range(20):
        if (a0-self.cmd(1))>2 or (self.cmd(1)-a0)>2:cnt+=1
        if (a1-self.cmd(2))>2 or (self.cmd(2)-a1)>2:cnt+=1
        if (a2-self.cmd(3))>2 or (self.cmd(3)-a2)>2:cnt+=1
        if cnt>5:break
        sleep(1000)
      self.cmd([10,0])
      if cnt<=5:break
      sleep(200)
    t=[None,None,None,None,None,None,None]
    t[0]=7
    t[1]=a0>>8
    t[2]=a0&0xFF
    t[3]=a1>>8
    t[4]=a1&0xFF
    t[5]=a2>>8
    t[6]=a2&0xFF
    self.cmd(t,n=7)