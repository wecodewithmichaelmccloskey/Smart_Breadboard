import Smart_Breadboard as sbb

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
NYU_PURPLE = (86, 1, 141)
WHITE = (255, 255, 255)
PICTURE_NAME = "Resistor.jpg"
EXAMPLE_TEXT = "This is an example of what instructions could look like when being displayed."

portAdd = None
LEDID = None
pix = None
turnOnArr = None
turnOffArr = None

sbb.info()

# LCD Touchscreen Display functions
# initializes display settings
disp = sbb.setupDisplay()

# Clears the display so that the screen only shows a white background
sbb.clearDisplay(disp)

# Create blank image for drawings and pictures
image = sbb.createNewImage(disp)

# Create a blank drawing to add shapes and text
draw = sbb.createDrawing(image)

# Draw a rectangle at of a specified location, size, and color
sbb.drawRectangle(draw, x = 0, y = 0, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, color = NYU_PURPLE)

# Adds text to a drawing at a specified location, size, and color
sbb.addText(draw, text = EXAMPLE_TEXT, x = 40, y = 220, fontsize = 28, length = 400, color = WHITE)

# Adds a picture to the image at a specified location, and size
# Picture size is scaled based on specified height
# x and y start from top left of the screen and specify the top left point of the picture
sbb.addPicture(image, picture_name = PICTURE_NAME, x = 135, y = 0, height = 210)

# Sends an image to the display
sbb.sendToDisplay(disp, image)

# Matrix Driver functions
#takes a "node" number on the physical circuit and returns the address of the port on the matrix drive>
sbb.nodeToLED(LEDID)

# turn off LED by sending byte to port address
sbb.turnOnLED(pix)
 
#turn on LED by sending byte to port address
sbb.turnOffLED(pix)

#turns off all LEDs in the matrix
sbb.turnOffAll()

# takes in an array of LEDs identfied to be turned on, and another array of LEDs identified to be turned off and performs on/off
sbb.runLEDDebug(turnOnArr, turnOffArr)

#Current Sensor functions
#reading current given proper parameters

#initializing connections from current sensor to Pi
sbb.setupCurrentSensor()

#reads in input values of voltage and resistance; returns current value
sbb.readCurrent()
