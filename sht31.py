from microbit import i2c
import time
R_HIGH = const(1)
R_MEDIUM = const(2)
R_LOW = const(3)
class SHT31:
  _map_cs_r = {
  	True: {
      R_HIGH : b'\x2c\x06',
      R_MEDIUM : b'\x2c\x0d',
      R_LOW: b'\x2c\x10'
    },
    False: {
      R_HIGH : b'\x24\x00',
      R_MEDIUM : b'\x24\x0b',
      R_LOW: b'\x24\x16'
    }
  }
  def __init__(self, addr=0x44):
    i2c.init(freq=20000)
    self._addr = addr
  def _send(self, buf):
    i2c.write(self._addr, buf)
  def _recv(self, count):
    return i2c.read(self._addr, count)
  def _raw_temp_humi(self, r=R_HIGH, cs=True):
    if r not in (R_HIGH, R_MEDIUM, R_LOW):raise ValueError('Wrong repeatabillity value given!')
    self._send(self._map_cs_r[cs][r])
    time.sleep_ms(50)
    raw = self._recv(6)
    return (raw[0] << 8) + raw[1], (raw[3] << 8) + raw[4]
  def get_temp_humi(self, resolution=R_HIGH, clock_stretch=True, celsius=True):
    t, h = self._raw_temp_humi(resolution, clock_stretch)
    if celsius:temp = -45 + (175*(t/65535))
    else:temp = -49 + (315*(t/65535))
    return temp, 100*(h/65535)
