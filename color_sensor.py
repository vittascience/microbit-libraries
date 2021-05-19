from microbit import i2c,sleep
import time
import math
class GroveI2CColorSensor:
  COLORS={"Red":{"x":0.64,"y":0.33,"r":255,"g":0,"b":0},
    "Green":{"x":0.3,"y":0.6,"r":0,"g":255,"b":0},
    "Blue":{"x":0.15,"y":0.06,"r":0,"g":0,"b":255},
    "Yellow":{"x":0.419,"y":0.505,"r":255,"g":255,"b":0},
    "Magenta":{"x":0.321,"y":0.154,"r":255,"g":0,"b":255},
    "Cyan":{"x":0.225,"y":0.329,"r":0,"g":255,"b":255},
    "Deep pink":{"x":0.466,"y":0.238,"r":255,"g":20,"b":147},
    "Orange":{"x":0.5,"y":0.441,"r":255,"g":165,"b":0},
    "Saddle brown":{"x":0.526,"y":0.399,"r":139,"g":69,"b":19},
    "Grey/White":{"x":0.313,"y":0.329,"r":255,"g":255,"b":255},
    "Black":{"x":0,"y":0,"r":0,"g":0,"b":0}}
  def __init__(self):
    self.use_continuous_integration()
    self.set_gain_and_prescaler(1,1)
  def use_continuous_integration(self,inte_t_ms=12):
    assert inte_t_ms==12 or inte_t_ms==100 or inte_t_ms==400,"Continuous integration supports only 12ms,100ms or 400ms integration durations"
    if inte_t_ms==100:inte_t_reg=0x01
    elif inte_t_ms==400:inte_t_reg=0x02
    else:inte_t_reg=0x00
    i2c.write(0x39,bytearray([0x80|0x01,0x00|inte_t_reg]))
    sleep(50)
  def use_manual_integration(self):
    i2c.write(0x39,bytearray([0x80|0x01,0x10]))
    sleep(50)
  def set_gain_and_prescaler(self,g_mult=1,prsc_div=1):
    assert g_mult==1 or g_mult==4 or g_mult==16 or g_mult==64,"Supported gain multipliers:1,4,16 and 64"
    assert prsc_div==1 or prsc_div==2 or prsc_div==4 or prsc_div==8 or prsc_div==16 or prsc_div==32 or prsc_div==64,"Supported prescaler dividers:1,2,4,8,16,32 and 64"
    if g_mult==4:gain_reg=0x10
    elif g_mult==16:gain_reg=0x20
    elif g_mult==64:gain_reg=0x30
    else:gain_reg=0x00
    if prsc_div==2:presc_reg=0x01
    elif prsc_div==4:presc_reg=0x02
    elif prsc_div==8:presc_reg=0x03
    elif prsc_div==16:presc_reg=0x04
    elif prsc_div==32:presc_reg=0x05
    elif prsc_div==64:presc_reg=0x06
    else:presc_reg=0x00
    i2c.write(0x39,bytearray([0x80|0x07,gain_reg|presc_reg]))
    sleep(50)
  def start_integration(self):i2c.write(0x39,bytearray([0x80|0X00,0x02|0x01]))
  def stop_integration(self):i2c.write(0x39,bytearray([0x80|0X00,0x00|0x01]))
  def is_integration_complete(self):return i2c.read(0x39,0x80|0X00,1)[0]&0x10==0x10
  def read_rgb(self):
    i2c.write(0x39,bytearray([0x80|0x10]))
    return i2c.read(0x39,8)
  def read_rgbc_word(self):
    rc=self.read_rgb()
    return (rc[2]+rc[3]*256,rc[0]+rc[1]*256,rc[4]+rc[5]*256,rc[6]+rc[7]*256)
  def read_rgbc(self):
    rc=self.read_rgb()
    return (rc[3],rc[1],rc[5],rc[7])
  def read_xy(self):
    rgbc=self.read_rgbc_word()
    x_bar=-0.14282*rgbc[0]+1.54924*rgbc[1]+-0.95641*rgbc[2]
    y_bar=-0.32466*rgbc[0]+1.57837*rgbc[1]+-0.73191*rgbc[2]
    z_bar=-0.68202*rgbc[0]+0.77073*rgbc[1]+0.563320*rgbc[2]
    return [x_bar/(x_bar+y_bar+z_bar),y_bar/(x_bar+y_bar+z_bar)]
  def read_color_name(self):
    xy=self.read_xy()
    cc=None
    cd=1
    for c_color in self.COLORS:
      c_coord=self.COLORS[c_color]
      c_dist=math.sqrt((c_coord["y"]-xy[1])**2+(c_coord["x"]-xy[0])**2)
      if c_dist<cd:
        cc=c_color
        cd=c_dist
    return cc
