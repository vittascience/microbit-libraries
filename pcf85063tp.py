from microbit import i2c
DAYS_OF_WEEK=["MON","TUE","WED","THU","FRI","SAT","SUN"]
RTC_HP_I2C_ADDR=0x51
class RTC_HP:
  def __init__(self,addr=RTC_HP_I2C_ADDR):self._addr=addr
  def reset(self):i2c.write(self._addr,b'\x00\x58')
  def fillByHMS(self,hour,min,sec):
    self._writeReg(0x04,self._decToBcd(sec))
    self._writeReg(0x05,self._decToBcd(min))
    self._writeReg(0x06,self._decToBcd(hour))
  def fillByYMD(self,year,month,day):
    self._writeReg(0x07,self._decToBcd(day))
    self._writeReg(0x09,self._decToBcd(month))
    self._writeReg(0x0a,self._decToBcd(year-2000))
  def fillDayOfWeek(self,dow):self._writeReg(0x08,self._decToBcd(DAYS_OF_WEEK.index(dow)))
  def startClock(self):self._writeReg(0x00,i2c.read(self._addr,1)[0]&0x7f)
  def readTime(self):
    i2c.write(self._addr,b'\x04')
    rdata = i2c.read(self._addr,7)
    return (self._bcdToDec(rdata[6])+2000,self._bcdToDec(rdata[5]&0x1f),self._bcdToDec(rdata[3]&0x3f),DAYS_OF_WEEK[self._bcdToDec(rdata[4]&0x07)],self._bcdToDec(rdata[2]&0x3f),self._bcdToDec(rdata[1])&0x7f,self._bcdToDec(rdata[0]))
  def _writeReg(self,reg,data):i2c.write(self._addr,bytearray([reg,data]))
  def _decToBcd(self,val):return (val//10*16)+(val%10)
  def _bcdToDec(self,val):return (val//16*10)+(val%16)
