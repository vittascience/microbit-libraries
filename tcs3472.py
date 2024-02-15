from microbit import i2c
import struct
class TCS3472:
  def __init__(self,led_pin):
    i2c.write(0x29,b'\x80\x03')
    i2c.write(0x29,b'\x81\x2b')
    self.led_pin=led_pin
  def scaled(self):
    crgb=self.raw()
    if crgb[0]>0:return tuple(float(x)/crgb[0] for x in crgb[1:])
    return (0,0,0)
  def rgb(self):return tuple(int(x*255) for x in self.scaled())
  def light(self):return self.raw()[0]
  def brightness(self,level=65.535):return int((self.light()/level))
  def valid(self):
    i2c.write(0x29,b'\x93')
    return i2c.read(0x29,1)[0]&1
  def raw(self):
    i2c.write(0x29,b'\xb4')
    return struct.unpack("<HHHH",i2c.read(0x29,8))
  def set_leds(self,state):self.led_pin.write_digital(state)