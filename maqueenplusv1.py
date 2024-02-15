import microbit as mb
import struct
from micropython import const

I2C_ADDR = const(0x10)

LEFT_LED_I2C_ADDR = const(0x0B)
RIGHT_LED_I2C_ADDR = const(0x0C)
LEFT = const(0)
RIGHT = const(1)

# Définition des constantes pour les moteurs
MT_L = 0
MT_R = 1

# Définition des constantes pour les servomoteurs
S1 = 1
S2 = 2
S3 = 3

# Définition des constantes pour la LED RVB
RGB_L = 1
RGB_R = 2
RGB_ALL = 3
RED = 1
GREEN = 2
BLUE = 4
YELLOW = 3
PINK = 5
CYAN = 6
WHITE = 7
OFF = 8

# Définition des constantes pour les capteurs de suivi de ligne
patrol = {
  "L1": 0x04,
  "L2": 0x02,
  "L3": 0x01,
  "R1": 0x08,
  "R2": 0x10,
  "R3": 0x20
}

mb.i2c.init(freq=100000, sda=mb.pin20, scl=mb.pin19)

def motorControl(mot, dir, spd):
  buf = bytearray(3)
  if mot == MT_L:
      buf[0] = 0x00
  else:
      buf[0] = 0x02
  buf[1] = dir
  buf[2] = spd
  mb.i2c.write(I2C_ADDR, buf)

def go(dL, sL, dR, sR):
  motorControl(MT_L, dL, sL)
  motorControl(MT_R, dR, sR)

def set_servo_angle(num, angle):
  buf = bytearray(3)
  if num == S1:
    buf[0] = 0x14
  elif num == S2:
    buf[0] = 0x15
  else:
    buf[0] = 0x16
  buf[1] = angle
  mb.i2c.write(I2C_ADDR, buf)

def RGBLight(rgbshow, color):
  buf = bytearray(3)
  buf[0] = 0x0B
  buf[1] = color
  if rgbshow == RGB_R:
    buf[0] = 0x0C
  elif rgbshow == RGB_ALL:
    buf[2] = color
  mb.i2c.write(I2C_ADDR, buf)

def stop():
  go(1, 0, 1, 0)

def move(dir, spd):
  if dir == "F":
    go(1, spd, 1, spd)
  elif dir == "L":
    go(1, 0, 1, spd)
  elif dir == "R":
    go(1, spd, 1, 0)
  elif dir == "B":
    go(2, spd, 2, spd)
  elif dir == "RL": #rotate
    go(2, spd, 1, spd)
  elif dir == "RR": #rotate
    go(1, spd, 2, spd)
  elif dir == "BL":
    go(1, 0, 2, spd)
  elif dir == "BR":
    go(2, spd, 1, 0)

def goto(dir, spd, dst):
  en = getEncoders()
  goal = dst
  if dir == "F":
    goal += en[0]
    while en[0] < goal:
      go(1, spd, 1, spd)
      en = getEncoders()
  if dir == "L":
    goal += en[1]
    while en[1] < goal:
      go(1, 0, 1, spd)
      en = getEncoders()
  elif dir == "R":
    goal += en[0]
    while en[0] < goal:
      go(1, spd, 1, 0)
      en = getEncoders()
  stop()

def sensor_on_line(sensor):
  mb.i2c.write(I2C_ADDR, b'\x1D')
  patrol_y = mb.i2c.read(I2C_ADDR, 1)
  sens = {
    "L1": -1,
    "L2": -1,
    "L3": -1,
    "R1": -1,
    "R2": -1,
    "R3": -1
  }
  for x in patrol:
    if (patrol_y[0] & patrol[x]) == patrol[x]:
      sens[x] = 1
    else:
      sens[x] = 0
  return sens[sensor]

def getEncoders():
  buf = bytearray(1)
  buf[0] = 0x04
  mb.i2c.write(I2C_ADDR, buf)
  return struct.unpack('>HH', mb.i2c.read(I2C_ADDR, 4))

def clearEncoders():
  buf = bytearray(5)
  buf[0] = 0x04
  buf[1] = buf[2] = buf[3] = buf[4] = 0x00
  mb.i2c.write(I2C_ADDR, buf)

def headlights(select, state):
  "Turn on or off the two front headlights. LEFT, RIGHT, or BOTH."
  if select == LEFT:
    mb.i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state]))
  elif select == RIGHT:
    mb.i2c.write(I2C_ADDR, bytearray([RIGHT_LED_I2C_ADDR, state]))
  else:
    mb.i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state, state]))