from microbit import i2c
class TH02:
  def ReadTemperature(self):
    self.writeReg(0x03,0x11)
    while not self.isAvailable():pass
    value=self.readData()>>2
    return value/32.0-50
  def ReadHumidity(self):
    self.writeReg(0x03,0x01)
    while not self.isAvailable():pass
    value=self.readData()>>4
    return value/16.0-24
  def isAvailable(self):
    status=self.readReg(0x00)
    if status and 0x01:return 0
    else:return 1
  def writeCmd(self,u8Cmd):i2c.write(0x40,u8Cmd)
  def readReg8(self,u8Reg):
    i2c.write(0x40,u8Reg)
    return i2c.read(0x40,1)
  def writeReg(self,u8Reg,u8Data):i2c.write(0x40,bytearray([u8Reg,u8Data]))
  def readReg16(self):
    self.writeCmd(0x01)
    data=i2c.read(0x40,3)
    temp=data[1]<<8|data[2]
    return temp