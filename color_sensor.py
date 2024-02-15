from microbit import i2c
from utime import sleep_us
_GAINS=(1,4,16,60)
class GroveI2cColorSensorV2:
  def __init__(self):
    self.awake=False
    self.set_integration_time(24)
    self.set_gain(1)
  def wakeup(self):
    enable=self._read_byte(0x00)
    self._write_byte(0x00,enable|0x01|0x02)
    sleep_us(2400)
    self.awake=True
  def sleep(self):
    enable=self._read_byte(0x00)
    self._write_byte(0x00,enable&~0x01)
    self.awake=False
  def is_awake(self):return self._read_byte(0x00)&0x01
  def integration_time(self):return (256-self._read_byte(0x01))*2.4
  def set_integration_time(self,t):
    if t<2.4:t=2.4
    elif t>614.4:t=614.4
    self._integration_time=int(t/2.4)*2.4
    self._write_byte(0x01,256-int(t/2.4))
  def gain(self):return _GAINS[self._read_byte(0x0f)]
  def set_gain(self,gain):
    if gain in _GAINS:self._write_byte(0x0f,_GAINS.index(gain))
  def raw(self):
    if not self.awake:self.wakeup()
    while not self._valid():sleep_us(2400)
    return tuple(self._read_word(reg) for reg in (0x16,0x18,0x1a,0x14))
  def rgb(self):
    r,g,b,clear=self.raw()
    if clear:
      r=int(255*r/clear)
      g=int(255*g/clear)
      b=int(255*b/clear)
    else:r,g,b=0,0,0
    return r,g,b
  def _valid(self):return self._read_byte(0x13)&0x01
  def _read_byte(self,address):
    i2c.write(0x29,bytearray([0x80|address]))
    return i2c.read(0x29,1)[0]
  def _read_word(self,address):
    i2c.write(0x29,bytearray([0x80|0x20|address]))
    data=i2c.read(0x29,2)
    return data[0]+data[1]<<8
  def _write_byte(self,address,data):i2c.write(0x29,bytearray([0x80|address,data]))
  def _write_word(self,address,data):i2c.write(0x29,bytearray([0x80|0x20|address,(data>>8)&0xFF,data&0xFF]))