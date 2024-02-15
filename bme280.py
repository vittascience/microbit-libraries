from microbit import i2c
from utime import sleep_ms
import gc
import struct
class BME280():
  def __init__(self):
    self._temp=0
    self._press=0
    self._alt=0
    self._qnh=1013.25
    self.write(0x76,0xE0,0xB6)
    sleep_ms(200)
    self.write(0x76,0xF2,0X05)
    sleep_ms(200)
    self.write(0x76,0xF4,0xB7)
    sleep_ms(200)
    self.write(0x76,0xF5,0x90)
    sleep_ms(200)
    self.comp=self.read(0x76,0x88,26)
    self.comp+=self.read(0x76,0xe1,7)
  def set_qnh(self,qnh):self._qnh=qnh
  def temperature(self):
    self.measure()
    return self._temp
  def pressure(self):
    self.measure()
    return self._press
  def humidity(self):
    self.measure()
    return self._humidity
  def altitude(self):
    self.measure()
    return self._alt
  def all(self):
    self.measure()
    return self._temp,self._press,self._humidity,self._alt
  def measure(self):
    self.update()
    gc.collect()
  def update(self):
    dig_T1,dig_T2,dig_T3,dig_P1,dig_P2,dig_P3,dig_P4,dig_P5,dig_P6,dig_P7,dig_P8,dig_P9,_,dig_H1,dig_H2,dig_H3,reg_E4,reg_E5,reg_E6,dig_H6=struct.unpack("<HhhHhhhhhhhhbBhBbBbb",self.comp)
    dig_H4=(reg_E5 & 0x0f)|(reg_E4<<4)
    dig_H5=(reg_E5>>4)|(reg_E6<<4)
    if dig_H4&(1<<12):dig_H4-=1<<12
    if dig_H5&(1<<11):dig_H5-=1<<12
    raw=self.read(0x76,0xF7,8)
    raw_temp=(raw[3]<<12)|(raw[4]<<4)|(raw[5]>>4)
    raw_press=(raw[0]<<12)|(raw[1]<<4)|(raw[2]>>4)
    raw_hum=(raw[6]<<8)|raw[7]
    var1=(raw_temp/16384.0-dig_T1/1024.0)*dig_T2
    var2=(raw_temp/131072.0-dig_T1/8192.0)*(raw_temp/131072.0-dig_T1/8192.0)*dig_T3
    temp=(var1+var2)/5120.0
    t_fine=(var1+var2)
    var1=t_fine/2.0-64000.0
    var2=var1*var1*dig_P6/32768.0
    var2=var2+var1*dig_P5*2
    var2=var2/4.0+dig_P4*65536.0
    var1=(dig_P3*var1*var1/524288.0+dig_P2*var1)/524288.0
    var1=(1.0+var1/32768.0)*dig_P1
    press=1048576.0-raw_press
    press=(press-var2/4096.0)*6250.0/var1
    var1=dig_P9*press*press/2147483648.0
    var2=press*dig_P8/32768.0
    press=press+(var1+var2+dig_P7)/16.0
    var1=t_fine-76800.0
    var2=dig_H4*64.0+(dig_H5/16384.0)*var1
    var3=raw_hum-var2
    var4=dig_H2/65536.0
    var5=1.0+(dig_H3/67108864.0)*var1
    var6=1.0+(dig_H6/67108864.0)*var1*var5
    var6=var3*var4*(var5*var6)
    h=var6*(1.0-dig_H1*var6/524288.0)
    h=max(0,min(100,h))
    self._temp=temp
    self._press=press/100.0
    self._humidity=h
    self._alt=44330.0*(1.0-pow(self._press/self._qnh,(1.0/5.255)))
  def read(self,address,reg,length=1):
    i2c.write(address,bytes([reg]),repeat=True)
    return i2c.read(address,length)
  def write(self,address,reg,value):i2c.write(address,bytes([reg,value]))