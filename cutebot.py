from machine import time_pulse_us
from utime import sleep_us
from micropython import const
from microbit import i2c, pin8, pin12, pin13, pin14

I2C_ADDRESS = const(16)

# MOTOR POSITION
MOTOR_LEFT = const(1)
MOTOR_RIGHT = const(2)

# MOTOR DIRECTION
MOTOR_BACKWARD = const(1)
MOTOR_FORWARD = const(2)

# SPEED CONSTANTS
MAX_SPEED = const(100)
MIN_SPEED = const(-100)

# SONAR UNITS
SONAR_CM = const(10)
SONAR_IN = const(20)

# RGB LEDS
RGB_LEFT = const(4)
RGB_RIGHT = const(8)
RGB_MIN = const(0)
RGB_MAX = const(255)

# SERVOS
SERVO_1 = const(5)
SERVO_2 = const(6)
SERVO_ANGLE_MIN = const(0)
SERVO_ANGLE_MAX = const(180)


def _set_motor_speed(motor_position, speed):
    """
    Sets a single motor speed via I2C bus. If the speed is negative, the direction is set to backward.

    I2C motor buffer
    [MOTOR POSITION, MOTOR DIRECTION, abs(SPEED), 0]
    """

    buf = bytearray(4)
    buf[0] = motor_position

    if speed > MAX_SPEED:
        speed = MAX_SPEED
    elif speed < MIN_SPEED:
        speed = MIN_SPEED

    if speed >= 0:
        buf[1] = MOTOR_FORWARD
    else:
        speed *= -1
        buf[1] = MOTOR_BACKWARD

    buf[2] = speed
    buf[3] = 0

    i2c.write(I2C_ADDRESS, buf)

def set_motors_speed(left_speed, right_speed):
    """
    Sets speeds for both motors.
    """
    _set_motor_speed(MOTOR_LEFT, left_speed)
    _set_motor_speed(MOTOR_RIGHT, right_speed)

def go_forward():
    """
    Sets both motor to run forward with full speed
    """
    set_motors_speed(MAX_SPEED / 2, MAX_SPEED / 2)

def go_backward():
    """
    Sets both motor to run backward with full speed
    """
    set_motors_speed(-MAX_SPEED / 2, -MAX_SPEED / 2)

def turn_left():
    """
    Sets the motors to run with full speed but with opposite direction. The Cutebot will turn in place anticlockwise.
    """
    set_motors_speed(-MAX_SPEED / 2, MAX_SPEED / 2)

def turn_right():
    """
    Sets the motors to run with full speed but with opposite direction. The Cutebot will turn in place clockwise.
    """
    set_motors_speed(MAX_SPEED / 2, -MAX_SPEED / 2)

def stop():
    """
    Sets speed of both motors to 0. The Cutebot will stop immediately.
    """
    set_motors_speed(0, 0)

def get_sonar_distance(unit = SONAR_CM, timeout_us = 30000):
    """
    Returns object distance from sonar module in given unit.
    If negative number is returned, the timeout was reached during waiting for echo.
    """
    # trigger
    pin8.write_digital(0)
    sleep_us(5)
    pin8.write_digital(1)
    sleep_us(10)
    pin8.write_digital(0)

    # catch echo
    echo_time = time_pulse_us(pin12, 1, timeout_us)
    if echo_time < 0:
        return echo_time
    if unit == SONAR_CM:
        return (echo_time / 2) / 29.1
    elif unit == SONAR_IN:
        return float((echo_time / 2) / 74)
    return -1.0

def _set_rgb_led(led, r, g, b):
    """
    Sets a color of a single RGB led.

    I2C RGB buffer
    [LED_POSITION, R, G, B]
    """

    buf = bytearray(4)

    buf[0] = led
    buf[1] = r if RGB_MIN <= r <= RGB_MAX else RGB_MIN
    buf[2] = g if RGB_MIN <= g <= RGB_MAX else RGB_MIN
    buf[3] = b if RGB_MIN <= b <= RGB_MAX else RGB_MIN

    i2c.write(I2C_ADDRESS, buf)

def set_left_rgb_led(r = 0, g = 0, b = 0):
    """
    Sets color of the left RGB led
    """
    _set_rgb_led(RGB_LEFT, r, g, b)

def set_right_rgb_led(r = 0, g = 0, b = 0):
    """
    Sets color of the right RGB led
    """
    _set_rgb_led(RGB_RIGHT, r, g, b)

def has_left_track():
    """
    Returns True whenever left tracker is on the black track. Otherwise returns False.
    """
    left_value = bool(pin13.read_digital())
    return not left_value

def has_right_track():
    """
    Returns True whenever right tracker is on the black track. Otherwise returns False.
    """
    right_value = bool(pin14.read_digital())
    return not right_value

def _set_servo_angle(servo, angle):
    """
    Sets angle of a servo connected to cutebot.

    I2C SERVO buffer
    [SERVO, ANGLE, 0, 0]
    """
    buf = bytearray(4)

    buf[0] = servo

    if angle < SERVO_ANGLE_MIN:
        angle = SERVO_ANGLE_MIN
    elif angle > SERVO_ANGLE_MAX:
        angle = SERVO_ANGLE_MAX

    buf[1] = angle
    buf[2] = buf[3] = 0

    i2c.write(I2C_ADDRESS, buf)

def set_servo_1_angle(angle):
    """
    Sets angle of S1 servo.
    """
    _set_servo_angle(SERVO_1, angle)

def set_servo_2_angle(angle):
    """
    Sets angle of S2 servo.
    """
    _set_servo_angle(SERVO_2, angle)