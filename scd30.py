from microbit import i2c
import ustruct
import time

SCD30_DEFAULT_I2C_ADDR=0x61
SCD30_POLYNOMIAL=0x31
CMD_CONTINUOUS_MEASUREMENT=0x0010
CMD_SET_MEASUREMENT_INTERVAL=0x4600
CMD_GET_DATA_READY=0x0202
CMD_READ_MEASUREMENT=0x0300
CMD_AUTOMATIC_SELF_CALIBRATION=0x5306
CMD_SET_FORCED_RECALIBRATION_FACTOR=0x5204
CMD_SET_TEMPERATURE_OFFSET=0x5403
CMD_SET_ALTITUDE_COMPENSATION=0x5102

class SCD30:
  
  def __init__(self,addr=SCD30_DEFAULT_I2C_ADDR):
    self.addr=addr
    
  def sendCommand(self,command,argument=None):
    if argument is None:
      buffer=bytearray(2)
      buffer[0]=command>>8
      buffer[1]=command&0xff
    else:
      buffer=bytearray(5)
      buffer[0]=command>>8
      buffer[1]=command&0xff
      buffer[2]=argument>>8
      buffer[3]=argument&0xff
      checkSum=self.calculateCrc(buffer[2],2)
      buffer[4]=checkSum
    return i2c.write(self.addr,buffer)
  
  def read_n_bytes(self,n_bytes):
    return i2c.read(self.addr,n_bytes)
  
  def readMeasurement(self, arg=0):
    self.sendCommand(CMD_READ_MEASUREMENT)
    data=i2c.read(self.addr,18)
    if arg==0:
      struct_co2=ustruct.pack('>BBBB',data[0],data[1],data[3],data[4])
      co2=ustruct.unpack('>f',struct_co2)
      return co2[0]
    elif arg==1:
      struct_T=ustruct.pack('>BBBB',data[6],data[7],data[9],data[10])
      T=ustruct.unpack('>f',struct_T)
      return T[0]
    elif arg==2:
      struct_rH=ustruct.pack('>BBBB',data[12],data[13],data[15],data[16])
      rH=ustruct.unpack('>f',struct_rH)
      return rH[0]
    else:
      return None
    
  def calculateCrc(self,data,len):
    crc=0xff
    # calculates 8-Bit checksum with given polynomial
    for byteCtr in range(len):
      crc^=data[byteCtr]
      for bit in range(8,0,-1):
        if crc and 0x80:crc=(crc<<1)^SCD30_POLYNOMIAL
        else:crc=(crc<<1)
    return crc
