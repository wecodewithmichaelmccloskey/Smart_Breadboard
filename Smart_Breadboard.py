# Display modules
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import hx8357
#Current sensor libraries
import spidev
import time
#Creating instance of SPI for current sensor
spi = spidev.SpiDev()
#RFID card reader libraries 
import RPi.GPIO as GPIO
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

#Matrix driver imports + global variables
#import board
#import busio
#from adafruit_is31fl3731.matrix import Matrix as Display

#i2c = busio.I2C(board.SCL, board.SDA)
#display = Display(i2c)

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

# Clears the display so that the screen only shows a white background
def clearDisplay(disp):
    disp.fill(0xffff)

# Create blank image for drawings and pictures
# 'RGB' mode used for full color
def createNewImage(disp):
    return Image.new("RGB", (disp.width, disp.height))

# Create a blank drawing to add shapes and text
def createDrawing(image):
    return ImageDraw.Draw(image)

# Draw a rectangle at of a specified location, size, and color
def drawRectangle(draw, x, y, width, height, color):
    draw.rectangle((x, y, x + width, y + height), fill=color)

# Adds text to a drawing at a specified location, size, and color
def addText(draw, text, x, y, fontsize, length, color):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

    lines = [""]
    line_number = 0
    text_length = 0
    for word in text.split():
        if text_length + font.getlength(word) < length:
            lines[line_number] += word + " "
            text_length += font.getlength(word + " ")
        else:
            lines.append(word + " ")
            line_number += 1
            text_length = font.getlength(word + " ")
    for line in lines:
        draw.text(
            (x, y),
            line,
            font=font,
            fill=color
        )
        y += font.getsize(text)[1]

# Adds a picture to the image at a specified location, and size
# Picture size is scaled based on specified height
# x and y start from top left of the screen and specify the top left point of the picture
def addPicture(image, picture_name, x, y, height):
    picture_image = Image.open(picture_name)

    scaled_width = picture_image.width * height // picture_image.height
    scaled_height = height
    picture_image = picture_image.resize((scaled_width, scaled_height))

    Image.Image.paste(image, picture_image, (x, y))

# Sends an image to the display
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
    spi.open(0, 0) # Open the SPI device on bus 0, device 0
    spi.max_speed_hz = 1000000 # Set the maximum SPI clock speed to 1 MHz


#reads in input values of voltage and resistance; returns current value
def readCurrent():
    # Define MCP3004 channel number
    channel = 0
    # Define INA169 shunt resistor value (in ohms)
    RS = 10
    # Define reference voltage for ADC
    VOLTAGE_REF = 3.3
    # Send an SPI message to the ADC to request a conversion on the selected channel
    adc_value = spi.xfer2([1, (8 + channel) << 4, 0])
    # Extract the ADC value from the received data
    sensor_value = ((adc_value[1] & 3) << 8) + adc_value[2] 
    # Convert analog value to voltage
    sensor_value = sensor_value * VOLTAGE_REF / 1023
    # Calculate current using equation given by INA169 datasheet
    current = sensor_value / (RS * 10)    
    
    return current

#RFID card reader functions

#writes to the RFID card, will only be used initially to create the circuit card for the user
def writeToCard():
    print("Hold card near reader to write")
    time.sleep(2)
    data = input("Enter data to write:")
    reader.write(data)
    print ("Done writing")
    

#used to read the card chosen by the user to identify the circuit instructions and debugging steps to be displayed
def readCard():
    print("Select a circuit - hold card up to the reader...")
    id, text = reader.read()
    print("You've selected the ", text, "circuit to work on...")
    
