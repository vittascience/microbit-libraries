from microbit import i2c,sleep
class SGP30:
  def __init__(self):
    self.serial=self.read([0x36, 0x82],10,3)
    if self.read([0x20,0x2f],0.01,1)[0]&0xf0!=0x0020:raise RuntimeError('SGP30 Not detected')
    self.iaq_init()
  def TVOC(self):return self.iaq_measure()[1]
  def baseline_TVOC(self):return self.get_iaq_baseline()[1]
  def eCO2(self):return self.iaq_measure()[0]
  def baseline_eCO2(self):return self.get_iaq_baseline()[0]
  def iaq_init(self):self.run(['iaq_init',[0x20,0x03],0,10])
  def iaq_measure(self):return self.run(['iaq_measure',[0x20,0x08],2,50])
  def get_iaq_baseline(self):return self.run(['iaq_get_baseline',[0x20,0x15],2,10])
  def set_iaq_baseline(self,eCO2,TVOC):
    if eCO2==0 and TVOC==0:raise RuntimeError('Invalid baseline')
    b=[]
    for i in [TVOC,eCO2]:
      a=[i>>8,i&0xFF]
      a.append(self.g_crc(a))
      b+=a
    self.run(['iaq_set_baseline',[0x20,0x1e]+b,0,10])
  def set_iaq_humidity(self,PM3):
    b=[]
    for i in [int(PM3*256)]:
      a=[i>>8,i&0xFF]
      a.append(self.g_crc(a))
      b+=a
    self.run(['iaq_set_humidity',[0x20,0x61]+b,0,10])
  def run(self,profile):
    n,cmd,s,d=profile
    return self.read(cmd,d,s)
  def read(self,cmd,d,rs):
    i2c.write(0x58,bytearray(cmd))
    sleep(d)
    if not rs:return None
    cr=i2c.read(0x58,rs*3)
    o=[]
    for i in range(rs):
      w=[cr[3*i],cr[3*i+1]]
      c=cr[3*i+2]
      if self.g_crc(w)!=c:raise RuntimeError('CRC Error')
      o.append(w[0]<<8|w[1])
    return o
  def g_crc(self,data):
    c=0xFF
    for byte in data:
      c^=byte
      for _ in range(8):
        if c&0x80:c=(c<<1)^0x31
        else:c<<=1
    return c&0xFF