from microbit import sleep
class MY9221:
  def __init__(self,di,dcki,reverse=False):
    self._d=di
    self._c=dcki
    self._r=reverse
    self._d.write_digital(0)
    self._c.write_digital(0)
  def _latch(self):
    self._d.write_digital(0)
    sleep(1)
    for i in range(4):
      self._d.write_digital(1)
      self._d.write_digital(0)
    sleep(1)
  def _write16(self,data):
    state=self._c.read_digital()
    for i in range(15,-1,-1):
      self._d.write_digital((data>>i)&1)
      state=not state
      self._c.write_digital(state)
  def _end(self):
    self._write16(0)
    self._write16(0)
    self._latch()
  def reverse(self,val=None):
    if val is None:return self._r
    self._r=val
  def level(self,val,brightness=255):
    self._write16(0)
    for i in range(9,-1,-1) if self._r else range(10):self._write16(brightness if val>i else 0)
    self._end()
  def bits(self,val,brightness=255):
    val&=0x3FF
    self._write16(0)
    for i in range(9,-1,-1) if self._r else range(10):self._write16(brightness if (val>>i)&1 else 0)
    self._end()
  def bytes(self,buf):
    self._write16(0)
    for i in range(9,-1,-1) if self._r else range(10):self._write16(buf[i])
    self._end()