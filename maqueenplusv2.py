from microbit import i2c
from micropython import const

# i2c bus location on the micro:bit.
# NAME_I2C_ADDR are adresses for robot components on the i2c bus.
I2C_ADDR = const(0x10)

# robot version length and location
VERSION_COUNT_I2C_ADDR = const(0x32)
VERSION_DATA_I2C_ADDR = const(0x33)

# Motor constants
LEFT_MOTOR_I2C_ADDR = const(0x00)
RIGHT_MOTOR_I2C_ADDR = const(0x02)

AXLE_WIDTH = 0.095

FORWARD = const(0)
BACKWARD = const(1)

# IR sensor constants for version 2.1
LINE_SENSOR_I2C_ADDR = const(0x1D)
ANALOG_L2_I2C_ADDR = const(0x26)
ANALOG_L1_I2C_ADDR = const(0x24)
ANALOG_M_I2C_ADDR = const(0x22)
ANALOG_R1_I2C_ADDR = const(0x20)
ANALOG_R2_I2C_ADDR = const(0x1E)

ALL_ANALOG_SENSOR_I2C_ADDRS = [
    ANALOG_L2_I2C_ADDR,
    ANALOG_L1_I2C_ADDR,
    ANALOG_M_I2C_ADDR,
    ANALOG_R1_I2C_ADDR,
    ANALOG_R2_I2C_ADDR,
]

sensor_index = [0, 1, 2, 3, 4]

L2 = const(0)
L1 = const(1)
M = const(2)
R1 = const(3)
R2 = const(4)

DIGITAL_SENSOR_STATUS_I2C_ADDR = const(0x1D)
DIGITAL_SENSOR_MASK = [16, 8, 4, 2, 1]
DIGITAL_SENSOR_SHIFT = [4, 3, 2, 1, 0]

# LED constants
LEFT_LED_I2C_ADDR = const(0x0B)
RIGHT_LED_I2C_ADDR = const(0x0C)
LEFT = const(0)
RIGHT = const(1)
BOTH = const(2)
ON = const(1)
OFF = const(0)

# Servos
SERVO_1 = const(0x14)
SERVO_2 = const(0x15)
SERVO_3 = const(0x16)

# NeoPixel constatnts
RED = const(0xFF0000)
ORANGE = const(0xFFA500)
YELLOW = const(0xFFFF00)
GREEN = const(0x00FF00)
BLUE = const(0x0000FF)
INDIGO = const(0x4B0082)
VIOLET = const(0x8A2BE2)
PURPLE = const(0xFF00FF)
WHITE = const(0xFF9070)
# OFF = const(0x000000) use the other OFF zero is zero

# General purpose functions
def init_maqueen():
    global sensor_index
    stop()
    version = maqueen_version()
    if version[-3:] == "2.0":
        pass
    elif version[-3:] == "2.1":
        sensor_index = [4, 3, 2, 1, 0]

def eight_bits(n):
    return max(min(n, 255), 0)

def one_bit(n):
    return max(min(n, 1), 0)

def maqueen_version():
    "Return the Maqueen board version as a string. The last 3 characters are the version."
    i2c.write(I2C_ADDR, bytes([VERSION_COUNT_I2C_ADDR]))
    count = int.from_bytes(i2c.read(I2C_ADDR, 1), "big")
    i2c.write(I2C_ADDR, bytes([VERSION_DATA_I2C_ADDR]))
    version = i2c.read(I2C_ADDR, count).decode("ascii")
    return version

# Motor functions
def stop():
    "Stop the robot's motors"
    drive(0)

def motorControlLeft(dir,spd):
  buf=bytearray(3)
  buf[0]=0x00
  buf[1]=dir
  buf[2]=spd
  i2c.write(I2C_ADDR,buf)

def motorControlRight(dir,spd):
  buf=bytearray(3)
  buf[0]=0x02
  buf[1]=dir
  buf[2]=spd
  i2c.write(I2C_ADDR,buf)        

def drive(speed_left, speed_right=None):
    "Drive forward at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, FORWARD, speed_right, FORWARD)

def backup(speed_left, speed_right=None):
    "Drive backwards at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, BACKWARD, speed_right, BACKWARD)

def spin_left(speed_left, speed_right=None):
    "Spin the robot left at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, BACKWARD, speed_right, FORWARD)

def spin_right(speed_left, speed_right=None):
    "Spin the robot right at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, FORWARD, speed_right, BACKWARD)

def motors(l_speed, l_direction, r_speed, r_direction):
    "Set both motor speeds 0-255 and directions (FORWARD, BACKWARD) left then right."
    buf = bytearray(5)
    buf[0] = LEFT_MOTOR_I2C_ADDR
    buf[1] = one_bit(l_direction)
    buf[2] = eight_bits(round(l_speed))
    buf[3] = one_bit(r_direction)
    buf[4] = eight_bits(round(r_speed))
    i2c.write(I2C_ADDR, buf)

# IR line sensor functions
def read_all_line_sensors():
    "Return an array of line sensor readings. Left to right."
    values = []
    for index in sensor_index:
        i2c.write(I2C_ADDR, bytes([ALL_ANALOG_SENSOR_I2C_ADDRS[index]]))
        buffer = i2c.read(I2C_ADDR, 2)
        values.append(buffer[1] << 8 | buffer[0])
    return values

def read_line_sensor(sensor):
    "Return a line sensor reading. On a line is about 240. Off line is about 70."
    i2c.write(I2C_ADDR, bytes([ALL_ANALOG_SENSOR_I2C_ADDRS[sensor_index[sensor]]]))
    buffer = i2c.read(I2C_ADDR, 2)
    return buffer[1] << 8 | buffer[0]

def sensor_on_line(sensor):
    "Return True if the line sensor sees a line."
    i2c.write(I2C_ADDR, bytes([DIGITAL_SENSOR_STATUS_I2C_ADDR]))
    sensor_state = int.from_bytes(i2c.read(I2C_ADDR, 1), "big")
    return (sensor_state & DIGITAL_SENSOR_MASK[sensor]) >> DIGITAL_SENSOR_SHIFT[sensor] == 1

# Servo functions
def set_servo_angle(servo, angle):
    "Set a servo to a specific angle."
    i2c.write(I2C_ADDR, bytes([servo, angle]))

# LED head light functions
def headlights(select, state):
    "Turn on or off the two front headlights. LEFT, RIGHT, or BOTH."
    if select == LEFT:
        i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state]))
    elif select == RIGHT:
        i2c.write(I2C_ADDR, bytearray([RIGHT_LED_I2C_ADDR, state]))
    else:
        i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state, state]))