from microbit import i2c,sleep
class GAS_GMXXX:
  def __init__(self,addr):
    self.addr=addr
    self.preheated()
  def preheated(self):
    i2c.write(self.addr,b'\xfe')
    sleep(10)
    self.isPreheated=True
  def unPreheated(self):
    i2c.write(self.addr,b'\xff')
    self.isPreheated=False
  def measure(self,cmd):
    value=0
    if not self.isPreheated:self.preheated()
    i2c.write(self.addr,cmd)
    sleep(10)
    data=i2c.read(self.addr,4)
    for i in range(4):value+=data[i]<<(8*i)
    return value
  def measure_NO2(self):return self.measure(b'\x01')
  def measure_C2H5OH(self):return self.measure(b'\x03')
  def measure_VOC(self):return self.measure(b'\x05')
  def measure_CO(self):return self.measure(b'\x07')
  def changeAddr(self,addr=0x08):
    if addr==0 or addr>127:addr=0x08
    i2c.write(self.addr,[0x55,addr])
    self.addr=addr
  def calcVol(self,adc):return (adc*3.3)/1023