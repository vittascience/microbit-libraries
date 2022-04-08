from microbit import i2c
import ustruct
class SCD30:
  def __init__(self,addr=0x61):
    self.addr,self.co2,self.t,self.h=addr,0,0,0
  def sendCommand(self,command,argument=None):
    if argument is None:buffer=bytearray([command>>8,command&0xff])
    else:
      buffer=bytearray(5)
      buffer[0]=command>>8
      buffer[1]=command&0xff
      buffer[2]=argument>>8
      buffer[3]=argument&0xff
      buffer[4]=self.calculateCrc(buffer,2)
    return i2c.write(self.addr,buffer)
  def read_n_bytes(self,n_bytes):return i2c.read(self.addr,n_bytes)
  def parseData(self,data):return ustruct.unpack('>f',ustruct.pack('>BBBB',data[0],data[1],data[2],data[3]))[0]
  def readMeasurement(self):
    self.sendCommand(0x0300)
    data=i2c.read(self.addr,18)    
    self.co2,self.t,self.h=self.parseData(data[:6]),self.parseData(data[6:12]),self.parseData(data[12:18])
  def setForcedRecalibration(self,co2ppm):
    if co2ppm!=None:self.sendCommand(0x5204,co2ppm)
    else:print('Please enter a valid calibration reference')
  def calculateCrc(self,data,len):
    crc=0xff
    for byteCtr in range(len):
      crc^=data[byteCtr]
      for bit in range(8,0,-1):
        if crc and 0x80:crc=(crc<<1)^0x31
        else:crc=(crc<<1)
    return crc
