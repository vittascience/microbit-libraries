from microbit import i2c,sleep
G={0x01:'right',0x02:'left',0x04:'up',0x08:'down',0x10:'forward',0x20:'backward',0x40:'clockwise',0x80:'anticlockwise'}
class GESTURE:
  def __init__(self,R):
    i2c.init()
    sleep(1)
    self._sbank(0)
    t=self._rreg(0)
    if t==0x20:self._init_reg()
    self._sbank(0)
  def _init_reg(self):
    for i in range(0, len(R),2):self._wreg(ord(R[i]),ord(R[i+1]))
  def _wreg(self,a,c):
    b=bytearray([a,c])
    i2c.write(0x73,b,False)
  def _rreg(self,a):
    b=bytearray([a])
    i2c.write(0x73,b,False)
    r=i2c.read(0x73,1,False)
    return ord(r)
  def _sbank(self,b):
    if b==0:self._wreg(0xEF,0)
    elif b==1:self._wreg(0xEF,1)
  def readGesture(self):
    d=self._rreg(0x43)
    if d in G:return G[d]
    else:
      d=self._rreg(0x44)
      if d==0x01:return 'wave'
    return 'none'