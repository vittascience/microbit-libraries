from microbit import i2c, sleep
import math
CHIP_ADDR=0x62
MODE_1_REG_ADDR=0x00
MODE_2_REG_ADDR=0x01
MOTOR_OUT_ADDR=0x08
MODE_1_REG_VALUE=0x00
MODE_2_REG_VALUE=0x04
MOTOR_OUT_VALUE=0xAA
LEFT_MOTOR=0x04
RIGHT_MOTOR=0x02
class MOVEMotor:
  def __init__(self):
    buffer=bytearray(2)
    buffer[0]=MODE_1_REG_ADDR
    buffer[1]=MODE_1_REG_VALUE
    i2c.write(CHIP_ADDR,buffer,False)
    buffer[0]=MODE_2_REG_ADDR
    buffer[1]=MODE_2_REG_VALUE
    i2c.write(CHIP_ADDR,buffer,False)
    buffer[0]=MOTOR_OUT_ADDR
    buffer[1]=MOTOR_OUT_VALUE
    i2c.write(CHIP_ADDR,buffer,False)
  def setLeftMotorSpeed(self,speed):
    motorBuffer=bytearray(2)
    gndPinBuffer=bytearray(2)
    if math.fabs(speed)>255: motorBuffer[1]=255
    else: motorBuffer[1]=int(math.fabs(speed))
    gndPinBuffer[1]=0x00
    if speed>0:
      motorBuffer[0]=LEFT_MOTOR
      gndPinBuffer[0]=LEFT_MOTOR +1
    else:
      motorBuffer[0]=LEFT_MOTOR +1
      gndPinBuffer[0]=LEFT_MOTOR
    i2c.write(CHIP_ADDR,motorBuffer,False)
    i2c.write(CHIP_ADDR,gndPinBuffer,False)
  def setRightMotorSpeed(self,speed):
    motorBuffer=bytearray(2)
    gndPinBuffer=bytearray(2)
    if math.fabs(speed)>255: motorBuffer[1]=255
    else: motorBuffer[1]=int(math.fabs(speed))
    gndPinBuffer[1]=0x00
    if speed>0:
      motorBuffer[0]=RIGHT_MOTOR +1
      gndPinBuffer[0]=RIGHT_MOTOR
    else:
      motorBuffer[0]=RIGHT_MOTOR
      gndPinBuffer[0]=RIGHT_MOTOR +1
    i2c.write(CHIP_ADDR,motorBuffer,False)
    i2c.write(CHIP_ADDR,gndPinBuffer,False)
  def stopMotors(self):
    stopBuffer=bytearray(2)
    stopBuffer[0]=LEFT_MOTOR
    stopBuffer[1]=0x00
    i2c.write(CHIP_ADDR,stopBuffer,False)
    stopBuffer[0]=LEFT_MOTOR +1
    i2c.write(CHIP_ADDR,stopBuffer,False)
    stopBuffer[0]=RIGHT_MOTOR
    i2c.write(CHIP_ADDR,stopBuffer,False)
    stopBuffer[0]=RIGHT_MOTOR +1
    i2c.write(CHIP_ADDR,stopBuffer,False)
