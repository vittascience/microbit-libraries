from microbit import i2c

class HT16K33:
    address = 0
    brightness = 15
    flash_rate = 0

    # *********** CONSTANTS **********

    HT16K33_GENERIC_DISPLAY_ON = 0x81
    HT16K33_GENERIC_DISPLAY_OFF = 0x80
    HT16K33_GENERIC_SYSTEM_ON = 0x21
    HT16K33_GENERIC_SYSTEM_OFF = 0x20
    HT16K33_GENERIC_DISPLAY_ADDRESS = 0x00
    HT16K33_GENERIC_CMD_BRIGHTNESS = 0xE0
    HT16K33_GENERIC_CMD_BLINK = 0x81

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c_address):
        assert 0x00 <= i2c_address < 0x80, "ERROR - Invalid I2C address in HT16K33()"
        self.address = i2c_address
        self.power_on()

    def power_on(self):
        """
        Power on the controller and display.
        """
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_ON)
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_ON)

    def _write_cmd(self, cmd):
        """
        Write a command to the HT16K33 controller.
        """
        data = bytearray(1)
        data[0] = cmd
        i2c.write(self.address, data)
