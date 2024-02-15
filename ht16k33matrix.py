from microbit import i2c
from ht16k33 import HT16K33

class HT16K33Matrix(HT16K33):
    width = 8
    height = 8
    def_chars = None
    rotation_angle = 0
    is_rotated = False
    is_inverse = False

    def __init__(self, i2c_address=0x70):
        self.buffer = bytearray(self.width)
        self.def_chars = []
        for i in range(32):
            self.def_chars.append(b"\x00")
        super().__init__(i2c_address)

    def set_icon(self, glyph, centre=False):
        length = len(glyph)
        assert 0 < length <= self.width, "ERROR - Invalid glyph set in set_icon()"
        for i in range(length):
            a = i
            if centre:
                a = i + ((8 - length) >> 1)
            self.buffer[a] = glyph[i] if not self.is_inverse else ((~glyph[i]) & 0xFF)
        return self
    
    def draw(self):
        if self.is_rotated:
            new_buffer = self._rotate_matrix(self.buffer, self.rotation_angle)
        else:
            new_buffer = bytearray(len(self.buffer))
            for i in range(8):
                new_buffer[i] = self.buffer[i]
        draw_buffer = bytearray(17)
        for i in range(len(new_buffer)):
            draw_buffer[i * 2 + 1] = (new_buffer[i] >> 1) | ((new_buffer[i] << 7) & 0xFF)
        i2c.write(self.address, draw_buffer)
    
     # ********** PRIVATE METHODS **********

    def _rotate_matrix(self, input_matrix, angle=0):
        """
        Rotate an 8-integer matrix through the specified angle in 90-degree increments:
           0 = none, 1 = 90 clockwise, 2 = 180, 3 = 90 anti-clockwise
        """
        assert angle in (0, 1, 2, 3), "ERROR - Invalid angle in _rotate_matrix()"
        if angle is 0: return input_matrix

        a = 0
        line_value = 0
        output_matrix = bytearray(self.width)

        # NOTE It's quicker to have three case-specific
        #      code blocks than a single, generic block
        for y in range(self.height):
            line_value = input_matrix[y]
            for x in range(7, -1, -1):
                a = line_value & (1 << x)
                if a is not 0:
                    if angle is 1:
                        output_matrix[7 - x] = output_matrix[7 - x] + (1 << y)
                    elif angle is 2:
                        output_matrix[7 - y] += (1 << (7 - x))
                    else:
                        output_matrix[x] = output_matrix[x] + (1 << (7 - y))
        return output_matrix
