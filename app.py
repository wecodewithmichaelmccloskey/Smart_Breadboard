import Smart_Breadboard as sbb
from threading import Thread, Lock, Event
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320


global page
page = "Start-Up"

rfid_tap = Event()
left_button_press = Event()

disp = sbb.setupDisplay()

def rfidTap():
    while (True):
        time.sleep(random.randint(10, 15))
        rfid_tap.set()
        print("rfid tapped")

def leftButtonPress():
    while (True):
        time.sleep(random.randint(10, 15))
        left_button_press.set()
        print("left button pressed")

def updateDisplay():
    global page

    while True:
        print(page)
        if page == "Start-Up":
            displayStartup()
            if rfid_tap.is_set():
                page = "Card Selection Confirmation"
                rfid_tap.clear()
            if left_button_press.is_set():
                left_button_press.clear()
        elif page == "Card Selection Confirmation":
            displayCardSelectionConfirmation()
            if rfid_tap.is_set():
                rfid_tap.clear()
            if left_button_press.is_set():
                page = "Start-Up"
                left_button_press.clear()
        time.sleep(0.1)

def displayStartup():
    image = sbb.createNewImage(disp)
    draw = sbb.createDrawing(image)
    sbb.drawRectangle(draw, x = 0, y = 0, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, color = WHITE)
    sbb.addText(draw, text = "Smart Breadboard", x = 81, y = 40, fontsize = 35, length = 480, color = BLACK)
    sbb.addText(draw, text = "Pick a Card", x = 45, y = 127, fontsize = 70, length = 480, color = BLACK)
    sbb.addText(draw, text = "...", x = 207, y = 190, fontsize = 70, length = 480, color = BLACK)
    sbb.addText(draw, text = "Tap a card on the reader to start building a circuit", x = 17, y = 280, fontsize = 18, length = 480, color = BLACK)
    sbb.sendToDisplay(disp, image)

def displayCardSelectionConfirmation():
    image = sbb.createNewImage(disp)
    draw = sbb.createDrawing(image)
    sbb.drawRectangle(draw, x = 0, y = 0, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, color = WHITE)
    sbb.drawRectangle(draw, x = 0, y = 250, width = DISPLAY_WIDTH, height = 2, color = BLACK)
    sbb.drawRectangle(draw, x = 239, y = 250, width = 2, height = 70, color = BLACK)
    sbb.addText(draw, text = "You've Selected", x = 121, y = 20, fontsize = 30, length = 480, color = BLACK)
    sbb.addText(draw, text = "CIRCUIT NAME", x = 21, y = 100, fontsize = 60, length = 480, color = BLACK)
    sbb.addText(draw, text = "YES", x = 83, y = 266, fontsize = 40, length = 480, color = BLACK)
    sbb.addText(draw, text = "NO", x = 330, y = 266, fontsize = 40, length = 480, color = BLACK)
    sbb.sendToDisplay(disp, image)

display_thread = Thread(target=updateDisplay)
rfid_thread = Thread(target=rfidTap)
left_button_thread = Thread(target=leftButtonPress)

sbb.clearDisplay(disp)

display_thread.start()
rfid_thread.start()
left_button_thread.start()

display_thread.join()
rfid_thread.join()
left_button_thread.join()
