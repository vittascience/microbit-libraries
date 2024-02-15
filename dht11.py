#
# dht11.py - a microbit implementation of dht11
# author - Phil Hall (rhubarbdog), copyright (c) November 2018
#
# this began life as raspberry pi code initial author
# https://github.com/szazo
#
# License - MIT

from microbit import *
import utime
class DHT11:
  def __init__(self,pin):
    self._p=pin
    self.t,self.h=0,0
  def read(self):
    p2bit=self._p2bit()
    buf=bytearray(320)
    l=(len(buf)//4)*4
    for i in range(l,len(buf)):buf[i]=1
    self._p.write_digital(1)
    sleep(50)
    self._birq()
    self._p.write_digital(0)
    sleep(20)
    self._p.set_pull(self._p.PULL_UP)
    if self._gb(p2bit,buf,l)!=l:
      self._ubirq()
      raise Exception("Grab bits failed.")
    else:self._ubirq()
    dt=self._parse_dta(buf)
    del buf
    if dt is None or len(dt)!=40:
      if dt is None:b=0
      else:b=len(dt)
      return
    dt=self._cb(dt)
    if dt[4]!=self._ccs(dt):return
    self.t,self.h=dt[2]+(dt[3]/10),dt[0]+(dt[1]/10)
  def _p2bit(self):
    p=self._p
    if p==pin0:s=3
    elif p==pin1:s=2
    elif p==pin2:s=1
    elif p==pin3:s=4
    elif p==pin4:s=5
    elif p==pin6:s=12
    elif p==pin7:s=11
    elif p==pin8:s=18
    elif p==pin9:s=10
    elif p==pin10:s=6
    elif p==pin12:s=20
    elif p==pin13:s=23
    elif p==pin14:s=22
    elif p==pin15:s=21
    elif p==pin16:s=16
    else:raise ValueError('function not suitable for this pin')
    return s
  @staticmethod
  @micropython.asm_thumb
  def _birq():cpsid('i')
  @staticmethod
  @micropython.asm_thumb
  def _ubirq():cpsie('i')
  @staticmethod
  @micropython.asm_thumb
  def _gb(r0,r1,r2):
    b(START)
    label(DELAY)
    mov(r7,0x2d)
    label(delay_loop)
    sub(r7,1)
    bne(delay_loop)
    bx(lr)
    label(READ_PIN)
    mov(r3,0x50)
    lsl(r3,r3,16)
    add(r3,0x05)
    lsl(r3,r3,8)
    add(r3,0x10)
    ldr(r4,[r3,0])
    mov(r3,0x01)
    lsl(r3,r0)
    and_(r4,r3)
    lsr(r4,r0)
    bx(lr)
    label(START)
    mov(r5,0x00)
    label(again)
    mov(r6,0x00)
    bl(READ_PIN)
    orr(r6,r4)
    bl(DELAY)
    bl(READ_PIN)
    lsl(r4,r4,8)
    orr(r6,r4)
    bl(DELAY)
    bl(READ_PIN)
    lsl(r4,r4,16)
    orr(r6,r4)
    bl(DELAY)
    bl(READ_PIN)
    lsl(r4,r4,24)
    orr(r6,r4)
    bl(DELAY)
    add(r1,r1,r5)
    str(r6,[r1,0])
    sub(r1,r1,r5)
    add(r5,r5,4)
    sub(r4,r2,r5)
    bne(again)
    label(RETURN)
    mov(r0,r5)
  def _parse_dta(self,buf):
    s,mb=2,50
    b,l,bit_=bytearray(mb),0,0
    for i in range(len(buf)):
      c=buf[i]
      l+=1
      if s==1:
        if c==0:
          s=2
          continue
        else:continue
      if s==2:
        if c==1:
          s=3
          continue
        else:continue
      if s==3:
        if c==0:
          s=4
          continue
        else:continue
      if s==4:
        if c==1:
          l,s=0,5
          continue
        else:continue
      if s==5:
        if c==0:
          b[bit_]=l
          bit_+=1
          s=4
          continue
        else:continue
      if bit_>=mb:break
    if bit_==0:return None
    r=bytearray(bit_)
    for i in range(bit_):r[i]=b[i]
    return r
  def _cb(self,pul):
    st,lgt=1000,0
    for i in range(len(pul)):
      l=pul[i]
      if l<st:st=l
      if l>lgt:lgt=l
    h,dt,did,b=st+(lgt-st)/2,bytearray(5),0,0
    for i in range(len(pul)):
      b=b<<1
      if pul[i]>h:b=b|1
      if ((i+1)%8==0):
        dt[did]=b
        did+=1
        b=0
    return dt
  def _ccs(self,dt):return dt[0]+dt[1]+dt[2]+dt[3]&0xff
  def getData(self,d=1):
    self.read()
    sleep(1000)
    if d==1:return self.t
    elif d==2:return self.h
    else: raise ValueError("DHT error: '" + d + "' is not a data option")
