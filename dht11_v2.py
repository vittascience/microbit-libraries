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
    self._set_wc(p2bit*4)
    self._birq()
    self._wd_high(1<<p2bit)
    utime.sleep_ms(50)
    self._wd_low(1<<p2bit)
    utime.sleep_ms(15)
    self._set_rc(p2bit*4)
    self._gb(p2bit,buf,l)
    self._ubirq()
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
    if p==pin0:s=2
    elif p==pin1:s=3
    elif p==pin2:s=4
    elif p==pin5:s=14
    elif p==pin8:s=10
    elif p==pin9:s=9
    elif p==pin11:s=23
    elif p==pin12:s=12
    elif p==pin13:s=17
    elif p==pin14:s=1
    elif p==pin15:s=13
    else:raise ValueError('function not suitable for this pin')
    return s
  @staticmethod
  @micropython.asm_thumb
  def _set_wc(r0):
    mov(r1,0x50)
    lsl(r1,r1,16)
    add(r1,0x07)
    lsl(r1,r1,8)
    add(r1,r1,r0)
    mov(r0,0b0001)
    str(r0,[r1,0])
  @staticmethod
  @micropython.asm_thumb
  def _set_rc(r0):
    mov(r1,0x50)
    lsl(r1,r1,16)
    add(r1,0x07)
    lsl(r1,r1,8)
    add(r1,r1,r0)
    mov(r0,0b1100)
    str(r0,[r1,0])
  @staticmethod
  @micropython.asm_thumb
  def _wd_high(r0):
    mov(r1,0x50)
    lsl(r1,r1,16)
    add(r1,0x05)
    lsl(r1,r1,8)
    add(r1,0x08)
    str(r0,[r1,0])
  @staticmethod
  @micropython.asm_thumb
  def _wd_low(r0):
    mov(r1,0x50)
    lsl(r1,r1,16)
    add(r1,0x05)
    lsl(r1,r1,8)
    add(r1,0x0C)
    str(r0,[r1,0])
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
    mov(r7,0xa7)
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
  @staticmethod
  def _parse_dta(buf):
    b,l,bit_=bytearray(50),0,0
    init=True
    for i in buf:
      if i==1:l+=1
      elif bit_==0 and l==0:pass
      elif init:
        l=0
        init=False
      elif bit_>=50:pass  
      elif l > 0:
        b[bit_]=l
        l=0
        bit_+=1 
    if bit_==0:return None
    r=bytearray(bit_)
    for i in range(bit_):r[i]=b[i]
    return r
  @staticmethod
  def _cb(pul):
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
  @staticmethod
  def _ccs(dt):return dt[0]+dt[1]+dt[2]+dt[3]&0xff
  def getData(self,d=1):
    self.read()
    utime.sleep(1)
    if d==1:return self.t
    elif d==2:return self.h
    else: raise ValueError("DHT error: '" + d + "' is not a data option")
