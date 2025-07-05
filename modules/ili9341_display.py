from machine import Pin, SPI

import time



# Comandos do ILI9341

SWRESET = 0x01

SLPOUT  = 0x11

DISPON  = 0x29

CASET   = 0x2A

PASET   = 0x2B

RAMWR   = 0x2C

MADCTL  = 0x36

COLMOD  = 0x3A



def color565(r, g, b):

    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)



FONT8x8 = {

    'A': [0x18,0x24,0x42,0x7E,0x42,0x42,0x42,0x00],

    'B': [0x7C,0x42,0x42,0x7C,0x42,0x42,0x7C,0x00],

    'C': [0x3C,0x42,0x40,0x40,0x40,0x42,0x3C,0x00],

    'D': [0x78,0x44,0x42,0x42,0x42,0x44,0x78,0x00],

    'E': [0x7E,0x40,0x40,0x7C,0x40,0x40,0x7E,0x00],

    'F': [0x7E,0x40,0x40,0x7C,0x40,0x40,0x40,0x00],

    'G': [0x3C,0x42,0x40,0x4E,0x42,0x42,0x3C,0x00],

    'H': [0x42,0x42,0x42,0x7E,0x42,0x42,0x42,0x00],

    'I': [0x7E,0x18,0x18,0x18,0x18,0x18,0x7E,0x00],

    'J': [0x1E,0x04,0x04,0x04,0x44,0x44,0x38,0x00],

    'K': [0x42,0x44,0x48,0x70,0x48,0x44,0x42,0x00],

    'L': [0x40,0x40,0x40,0x40,0x40,0x40,0x7E,0x00],

    'M': [0x42,0x66,0x5A,0x5A,0x42,0x42,0x42,0x00],

    'N': [0x42,0x62,0x52,0x4A,0x46,0x42,0x42,0x00],

    'O': [0x3C,0x42,0x42,0x42,0x42,0x42,0x3C,0x00],

    'P': [0x7C,0x42,0x42,0x7C,0x40,0x40,0x40,0x00],

    'Q': [0x3C,0x42,0x42,0x42,0x4A,0x44,0x3A,0x00],

    'R': [0x7C,0x42,0x42,0x7C,0x48,0x44,0x42,0x00],

    'S': [0x3C,0x42,0x40,0x3C,0x02,0x42,0x3C,0x00],

    'T': [0x7E,0x18,0x18,0x18,0x18,0x18,0x18,0x00],

    'U': [0x42,0x42,0x42,0x42,0x42,0x42,0x3C,0x00],

    'V': [0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00],

    'W': [0x42,0x42,0x42,0x5A,0x5A,0x66,0x42,0x00],

    'X': [0x42,0x42,0x24,0x18,0x24,0x42,0x42,0x00],

    'Y': [0x42,0x42,0x24,0x18,0x18,0x18,0x18,0x00],

    'Z': [0x7E,0x02,0x04,0x18,0x20,0x40,0x7E,0x00],

    ' ': [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],

    '.': [0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00],

    ':': [0x00,0x18,0x18,0x00,0x00,0x18,0x18,0x00],

    '0': [0x3C,0x66,0x6E,0x76,0x66,0x66,0x3C,0x00],

    '1': [0x18,0x38,0x18,0x18,0x18,0x18,0x7E,0x00],

    '2': [0x3C,0x66,0x06,0x0C,0x18,0x30,0x7E,0x00],

    '3': [0x3C,0x66,0x06,0x1C,0x06,0x66,0x3C,0x00],

    '4': [0x0C,0x1C,0x2C,0x4C,0x7E,0x0C,0x0C,0x00],

    '5': [0x7E,0x60,0x7C,0x06,0x06,0x66,0x3C,0x00],

    '6': [0x1C,0x30,0x60,0x7C,0x66,0x66,0x3C,0x00],

    '7': [0x7E,0x06,0x0C,0x18,0x30,0x30,0x30,0x00],

    '8': [0x3C,0x66,0x66,0x3C,0x66,0x66,0x3C,0x00],

    '9': [0x3C,0x66,0x66,0x3E,0x06,0x0C,0x38,0x00],

    '%': [0x62,0x64,0x08,0x10,0x26,0x46,0x00,0x00],

}



class ILI9341:

    def __init__(self, spi, cs, dc, rst, width=240, height=320):

        self.spi = spi

        self.cs = cs

        self.dc = dc

        self.rst = rst

        self.width = width

        self.height = height

        self._init_pins()

        self._init_display()



    def _init_pins(self):

        self.cs.init(Pin.OUT, value=1)

        self.dc.init(Pin.OUT, value=0)

        self.rst.init(Pin.OUT, value=1)



    def _write_cmd(self, cmd):

        self.dc.value(0)

        self.cs.value(0)

        self.spi.write(bytes([cmd]))

        self.cs.value(1)



    def _write_data(self, data):

        self.dc.value(1)

        self.cs.value(0)

        self.spi.write(data if isinstance(data, bytes) else bytes(data))

        self.cs.value(1)



    def _reset(self):

        self.rst.value(0)

        time.sleep_ms(100)

        self.rst.value(1)

        time.sleep_ms(100)



    def _init_display(self):

        self._reset()

        self._write_cmd(SWRESET)

        time.sleep_ms(150)

        self._write_cmd(SLPOUT)

        time.sleep_ms(150)

        self._write_cmd(COLMOD)

        self._write_data([0x55])

        self._write_cmd(MADCTL)

        self._write_data([0x08])

        self._write_cmd(DISPON)

        time.sleep_ms(150)



    def set_window(self, x0, y0, x1, y1):

        self._write_cmd(CASET)

        self._write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])

        self._write_cmd(PASET)

        self._write_data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])

        self._write_cmd(RAMWR)



    def draw_pixel(self, x, y, color):

        if 0 <= x < self.width and 0 <= y < self.height:

            self.set_window(x, y, x, y)

            self._write_data(bytes([color >> 8, color & 0xFF]))



    def fill_screen(self, color):

        self.draw_rect(0, 0, self.width, self.height, color)



    def draw_char(self, x, y, char, color, scale=1):

        font = FONT8x8.get(char.upper(), [0]*8)

        for row in range(8):

            line = font[row]

            for col in range(8):

                if line & (1 << col):

                    px = x + col * scale

                    py = y + row * scale

                    for dx in range(scale):

                        for dy in range(scale):

                            self.draw_pixel(px + dx, py + dy, color)



    def percent_to_pixel(self, x_pct, y_pct):

        return int(self.width * x_pct), int(self.height * y_pct)



    def draw_text(self, x_pct, y_pct, text, color, scale=1):

        x, y = self.percent_to_pixel(x_pct, y_pct)

        x -= len(text) * 4 * scale

        for i, ch in enumerate(reversed(text)):

            self.draw_char(x + i * 8 * scale, y, ch, color, scale)



    def draw_rect(self, x, y, w, h, color):

        x1 = min(x + w - 1, self.width - 1)

        y1 = min(y + h - 1, self.height - 1)

        x0 = max(x, 0)

        y0 = max(y, 0)

        if x0 > x1 or y0 > y1:

            return

        self.set_window(x0, y0, x1, y1)

        pixels = (x1 - x0 + 1) * (y1 - y0 + 1)

        color_hi = color >> 8

        color_lo = color & 0xFF

        chunk = 1024

        buf = bytearray([color_hi, color_lo] * chunk)

        for _ in range(pixels // chunk):

            self._write_data(buf)

        if pixels % chunk:

            self._write_data(buf[:(pixels % chunk) * 2])



    def draw_rect_percent(self, x_pct, y_pct, w_pct, h_pct, color):

        x, y = self.percent_to_pixel(x_pct, y_pct)

        w = int(self.width * w_pct)

        h = int(self.height * h_pct)

        self.draw_rect(x, y, w, h, color)



class TextLineLayout:

    def __init__(self, display, text_fixo, x_pct, y_pct, color_fixo, color_var, bg_color, scale=1):

        self.display = display

        self.text_fixo = text_fixo

        self.x_pct = x_pct

        self.y_pct = y_pct

        self.color_fixo = color_fixo

        self.color_var = color_var

        self.bg_color = bg_color

        self.scale = scale

        self.current_var = ""

        self._draw_fixed_text()



    def _draw_fixed_text(self):

        x, y = self.display.percent_to_pixel(self.x_pct, self.y_pct)

        total_w = len(self.text_fixo + self.current_var) * 8 * self.scale

        x_text = x - total_w // 2

        for i, c in enumerate(reversed(self.text_fixo)):

            self.display.draw_char(x_text + i * 8 * self.scale, y, c, self.color_fixo, self.scale)

        self.x_var, self.y_var = x_text + (len(self.text_fixo) - 7) * 8 * self.scale, y



    def update_var_text(self, new_text, color=None):

        if new_text != self.current_var:

            width = len(self.current_var) * 8 * self.scale

            self.display.draw_rect(self.x_var - width, self.y_var, width, 8 * self.scale, self.bg_color)

            draw_color = color if color is not None else self.color_var

            for i, c in enumerate(new_text):

                self.display.draw_char(self.x_var - (i + 1) * 8 * self.scale, self.y_var, c, draw_color, self.scale)

            self.current_var = new_text
