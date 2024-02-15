from microbit import i2c,sleep
class HM330X:
  def __init__(self):
    i2c.init(freq=20000)
    i2c.write(0x40,b'\x88')
  def read_data(self):return i2c.read(0x40,29)
  def check_crc(self,data):
    sum=0
    for i in range(29-1):sum+=data[i]
    sum=sum&0xff
    return (sum==data[28])
  def parse_data(self,data):
    std_PM1=data[4]<<8|data[5]
    std_PM2_5=data[6]<<8|data[7]
    std_PM10=data[8]<<8|data[9]
    atm_PM1=data[10]<<8|data[11]          
    atm_PM2_5=data[12]<<8|data[13]
    atm_PM10=data[14]<<8|data[15]
    return [std_PM1,std_PM2_5,std_PM10,atm_PM1,atm_PM2_5,atm_PM10]
  def getData(self,select=3):
    datas=self.read_data()
    sleep(5)
    if(self.check_crc(datas)==True):
      data_parsed=self.parse_data(datas)
      return data_parsed[select]