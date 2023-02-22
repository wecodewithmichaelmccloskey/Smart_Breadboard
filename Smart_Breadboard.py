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
    pass

# clears the display so that the screen only shows a white background
def clearDisplay():
    pass

# sends text to the display at a specified location
def sendTextToDisplay():
    pass

# sends an image to the display at a specified location
def sendImageToDisplay():
    pass

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
