import Smart_Breadboard as sbb
import random
import time

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
NYU_PURPLE = (86, 1, 141)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def createReadingsImage(disp, reading):
    readings_image = sbb.createNewImage(disp)
    readings_draw = sbb.createDrawing(readings_image)
    sbb.drawRectangle(readings_draw, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, NYU_PURPLE)
    sbb.addText(readings_draw, reading, 0, 0, 50, DISPLAY_WIDTH, WHITE)
    sbb.sendToDisplay(disp, readings_image)

disp = sbb.setupDisplay()
while(True):
    createReadingsImage(disp, str(round(random.random() * 10, 3)))
    time.sleep(0.2)
