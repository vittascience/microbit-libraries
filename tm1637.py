from utime import sleep_us
_SEG=bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x40')
class TM1637:
  def __init__(self,clk,dio,bright=7):
    self.clk=clk
    self.dio=dio
    if not 0<=bright<=7:raise ValueError("Brightness out of range")
    self._bright=bright
    sleep_us(10)
    self._write_data_cmd()
    self._write_dsp_ctrl()
  def _write_digital(self,pin,state):
    pin.write_digital(state)
    sleep_us(10)
  def _start(self):
    self._write_digital(self.dio,0)
    self._write_digital(self.clk,0)
  def _stop(self):
    self._write_digital(self.dio,0)
    self._write_digital(self.clk,1)
    self._write_digital(self.dio,1)
  def _write_data_cmd(self):
    self._start()
    self._write_byte(0x40)
    self._stop()
  def _write_dsp_ctrl(self):
    self._start()
    self._write_byte(0x80|0x08|self._bright)
    self._stop()
  def _write_byte(self,b):
    for i in range(8):
      self._write_digital(self.dio,(b>>i)&1)
      self._write_digital(self.clk,1)
      self._write_digital(self.clk,0)
    self._write_digital(self.clk,0)
    self._write_digital(self.clk,1)
    self._write_digital(self.clk,0)
  def brightness(self,val=None):
    if val is None:return self._bright
    if not 0<=val<=7:raise ValueError("Brightness out of range")
    self._bright=val
    self._write_data_cmd()
    self._write_dsp_ctrl()
  def write(self,segs,pos=0):
    if not 0<=pos<=5:raise ValueError("Position out of range")
    self._write_data_cmd()
    self._start()
    self._write_byte(0xC0|pos)
    for seg in segs:self._write_byte(seg)
    self._stop()
    self._write_dsp_ctrl()
  def encode_str(self,str):
    segs=bytearray(len(str))
    for i in range(len(str)):segs[i]=self.encode_char(str[i])
    return segs
  def encode_char(self,char):
    o=ord(char)
    if o==45:return _SEG[10]
    if o>=48 and o<=57:return _SEG[o-48]
    raise ValueError("Character out of range: {:d} '{:s}'".format(o,chr(o)))
  def number(self,num):
    num=max(-999,min(num,9999))
    self.write(self.encode_str('{0: >4d}'.format(num)))
  def numbers(self,num1,num2,colon=True):
    num1=max(-9,min(num1,99))
    num2=max(-9,min(num2,99))
    segs=self.encode_str('{0:0>2d}{1:0>2d}'.format(num1,num2))
    if colon:segs[1]|=0x80
    self.write(segs)
  def temperature(self,num):
    if num<-9:self.show('-9')
    elif num>99:self.show('99')
    else:self.write(self.encode_str('{0: >2d}'.format(num)))
    self.write(b'\x63\x39',2)
  def show(self,str,colon=False):
    segs=self.encode_str(str)
    if len(segs)>1 and colon:segs[1]|=128
    self.write(segs[:4])
  def clock(self,time,colon=True):
    h,mn=time
    segs=self.encode_str('{0:0>2d}{1:0>2d}'.format(h,mn))
    if colon:segs[1]|=128
    self.write(segs)
