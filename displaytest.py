from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw
from time import monotonic, sleep

class Display:
  def __init__(self):
    self.device = sh1106(port=1, address=0x3C)
    self.font = ImageFont.truetype('/usr/share/fonts/truetype/coders_crux.ttf', 32)
    self.resistance = None
    self.update_time = monotonic()
    self.draw_pretty_things()

  def draw_pretty_things(self):
    # for border and name
    with canvas(self.device) as draw:
      draw.ellipse([0, 0, 5, 5], outline=0, fill=255)
  def 

  def draw_resistance(self, new_resistance):
    # clears screen
    draw.rectangle((0, 0, self.device.width, self.device.height), outline=0, fill=0)
    self.draw_pretty_things()

    time_elapsed = monotonic() - self.update_time
    if (new_resistance == None and time_elapsed > 5)
      with canvas(self.device) as draw:
        draw.text((10, 20), "Resistor not found", fill=255, font=self.font)
    elif (new_resistance != None)
      with canvas(self.device) as draw:
        draw.text((10, 20), str(self.new_resistance), fill=255, font=self.font)
        self.resistance = new_resistance
        self.update_time = monotonic()

#\u2126

d = Display()
sleep(5)
d.draw_resistance(15)
sleep(10)
d.draw_resistance(12300)
sleep(2)
d.draw_resistance(None)
sleep(3)
d.draw_resistance(None)
sleep(3)
d.draw_resistance(434000)
