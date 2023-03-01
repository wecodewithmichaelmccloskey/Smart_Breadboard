# Display modules
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import hx8357

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

#Matrix driver imports + global variables
import board
import busio
from adafruit_is31fl3731.matrix import Matrix as Display

i2c = busio.I2C(board.SCL, board.SDA)
display = Display(i2c)

#Matrix and Matrix A LED Control Register Address
MTRX_DRV_ADDR = 0x74
CA1 = 0x00
CA2 = 0x02
CA3 = 0x04
CA4 = 0x06
CA5 = 0x08
CA6 = 0x0A
CA7 = 0x0C
CA8 = 0x0E
CA9 = 0x10
def info():  
    '''Prints a basic library description'''
    print("Software library for the Smart Breadboard project.")

# LCD Touchscreen Display functions
# initializes display settings
def setupDisplay():
    # Create the display ( values are for 3.5" HX8357):
    disp = hx8357.HX8357(
        spi,
        rotation=180,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
    )

    return disp

def createNew(disp):
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height

    return Image.new("RGB", (width, height))

def createDrawing(image):
    return ImageDraw.Draw(image)

def drawRectangle(draw, x, y, height, width, color):
    # Draw a rectangle
    draw.rectangle((x, y, width, height), fill=color)

# clears the display so that the screen only shows a white background
def clearDisplay(disp):
    disp.fill(0xffff)

# sends text to the display at a specified location
def createText(draw, text, fontsize, x, y, color):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

    (font_width, font_height) = font.getsize(text)
    draw.text(
        (x, y),
        text,
        font=font,
        fill=color,
    )

# sends an image to the display at a specified location
def createImage(image_name, width, height, x, y):
    image = Image.open(image_name)

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    new_ratio = width / height
    if new_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height))

    # Crop and center the image
    #x = scaled_width // 2 - width // 2
    #y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    return image

def sendToDisplay(disp, image):
    disp.image(image)

# Matrix Driver functions
#takes a "node" number on the physical circuit and returns the address of the port on the matrix driver that will be used to turn on/off the corresponding LED
def nodeToLED(LEDID):
   if LEDID == 1:
      return CA1
   elif LEDID == 2:
      return CA2
   elif LEDID == 3:
       return CA3
   elif LEDID == 4:             
      return CA4
   elif LEDID == 5:
       return CA5
   elif LEDID == 6:
       return CA6
   elif LEDID == 7:
        return CA7
   elif LEDID == 8:
        return CA8
   elif LEDID == 9:
        return CA9
   else:
        return "Value not in Matrix range" 

# turn off LED by sending byte to port address
def turnOnLED (portAdd):
      display.pixel(pix, 0, 127)

#turn on LED by sending byte to port address
def turnOffLED (portAdd):
     display.pixel(pix, 0, 0)

#turns off all LEDs in the matrix
def turnOffAll():
  display.fill(0)

 # takes in an array of LEDs identfied to be turned on, and another array of LEDs identified to be turned off and performs on/off
def runLEDDebug(turnOnArr, turnOffArr):
  for i in turnOnArr:
    turnOnLED(nodeToLED(i))
  for j in turnOffArr:
    turnOffLED(nodeToLED(j))

#Current Sensor functions
#reading current given proper parameters

#initializing connections from current sensor to Pi
def setupCurrentSensor():
    pass

#reads in input values of voltage and resistance; returns current value
def readCurrent():
    pass
