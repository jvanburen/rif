from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw, Image
from time import monotonic, sleep
from symbols import OMEGA, RESISTOR

__all__ = ['display', 'Display']

class Display:
  HOLD_TIME = 5.0 # seconds
  def __init__(self):
    self.device = sh1106(port=1, address=0x3C)
    self.font = ImageFont.truetype('/usr/share/fonts/truetype/coders_crux.ttf', 32)
    self.resistance = None
    self.update_time = 0
    self.ohm = Image.new("1", (16, 16), None)
    self.ohm.putdata(OMEGA)
    self.resistor = Image.new("1", (25, 10), None)
    self.resistor.putdata(RESISTOR)
    self.loading_screen()

  def loading_screen(self):
    with canvas(self.device) as draw:
      draw.rectangle((0, 0, self.device.width, self.device.height), outline=0, fill=0)
      draw.text((20, 23), "Loading...", fill=255, font=self.font)

  def welcome_screen(self):
    with canvas(self.device) as draw:
      draw.rectangle((0, 0, self.device.width, self.device.height), outline=0, fill=0)
      draw.text((20, 20), "Insert", fill=255, font=self.font)
      draw.text((20, 35), "Resistor", fill=255, font=self.font)

  def draw_border(self, draw):
    # for border
    # clears screen
    draw.rectangle((0, 0, self.device.width, self.device.height), outline=0, fill=0)

    nameFont = ImageFont.truetype('/usr/share/fonts/truetype/coders_crux.ttf', 16)

    draw.text((5, 3), "Resistance is Futile", fill=255, font=nameFont)
    # draws border
#    draw.ellipse([0, 0, 5, 5], outline=1, fill=255)
#    draw.ellipse([self.device.width-5, self.device.height-5, self.device.width, self.device.height], outline = 1, fill = 255)

  def draw_resistance(self, new_resistance):
    with canvas(self.device) as draw:
      self.draw_border(draw)
      if new_resistance is None:
        if self.update_time + self.HOLD_TIME < monotonic():
          draw.text((20, 25), "Resistor", fill=255, font=self.font)
          draw.text((15, 40), "not found", fill=255, font=self.font)
        else:
          res_text = Display.format_resistance(self.resistance)
          width, height = draw.textsize(res_text, font=self.font)
          totalWidth = width+20
          draw.text(((128-totalWidth)/2, (64-height)/2), res_text, fill=255, font=self.font)
          draw.bitmap(((128-totalWidth)/2 + width, (64-height)/2-2), self.ohm, fill=255)
      else:
        draw.bitmap((128-28, 50), self.resistor, fill=255)
        res_text = Display.format_resistance(new_resistance)
        width, height = draw.textsize(res_text, font=self.font)
        totalWidth = width+20
        draw.text(((128-totalWidth)/2, (64-height)/2), res_text, fill=255, font=self.font)
        draw.bitmap(((128-totalWidth)/2 + width, (64-height)/2-2), self.ohm, fill=255)
        self.resistance = new_resistance
        self.update_time = monotonic()

  @classmethod
  def format_resistance(cls, resistance):
    if resistance is None: return None
    suffixes = ["", "K", "M", "G"]
    suffix = 0
    while resistance // 1000 > 0:
      resistance //= 1000
      suffix += 1
    return str(resistance) + suffixes[suffix]

#\u2126

display = Display()
# sleep(5)
# display.draw_resistance(15)
# sleep(3)
# display.draw_resistance(12300)
# sleep(2)
# display.draw_resistance(None)
# sleep(3)
# display.draw_resistance(None)
# sleep(3)
# display.draw_resistance(434000)
