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
def nodeToLED (): 
    pass

# configures command register in order to select for LED control register
def configureCommandRegister ():
    pass 

# turn off LED by sending byte to port address
def turnOnLED (portAdd):
    pass

#turn on LED by sending byte to port address
def turnOffLED (portAdd):
    pass

#Current Sensor functions
#reading current given proper parameters

#initializing connections from current sensor to Pi
def setupCurrentSensor();
    pass

#reads in input values of voltage and resistance; returns current value
def readCurrent();
    pass
