import Smart_Breadboard

portAdd = None

Smart_Breadboard.info()

# LCD Touchscreen Display functions
# initializes display settings
Smart_Breadboard.setupDisplay()

# clears the display so that the screen only shows a white background
Smart_Breadboard.clearDisplay()

# sends text to the display at a specified location
Smart_Breadboard.sendTextToDisplay()

# sends an image to the display at a specified location
Smart_Breadboard.sendImageToDisplay()

# Matrix Driver functions
#takes a "node" number on the physical circuit and returns the address of the port on the matrix drive>
Smart_Breadboard.nodeToLED(LEDID)

# turn off LED by sending byte to port address
Smart_Breadboard.turnOnLED(pix)
 
#turn on LED by sending byte to port address
Smart_Breadboard.turnOffLED(pix)

 #turns off all LEDs in the matrix
Smart_Breadboard.turnOffAll()

 # takes in an array of LEDs identfied to be turned on, and another array of LEDs identified to be turned off and performs on/off
Smart_Breadboard.runLEDDebug(turnOnArr, turnOffArr)

#Current Sensor functions
#reading current given proper parameters

#initializing connections from current sensor to Pi
Smart_Breadboard.setupCurrentSensor()

#reads in input values of voltage and resistance; returns current value
Smart_Breadboard.readCurrent()
