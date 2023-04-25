import Smart_Breadboard as sbb
from threading import Thread, Lock, Event
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320


global page
page = "Start-Up"

global instr_num
instr_num = 1

rfid_tap = Event()
left_button_press = Event()
right_button_press = Event()
middle_button_press = Event()

def rfidTap():
    pass

def leftButtonPress():
    while (True):
        sbb.wait_for_back_button()
        left_button_press.set()
        print("left button pressed")

def rightButtonPress():
    while (True):
        sbb.wait_for_next_button()
        right_button_press.set()
        print("right button pressed")

def middleButtonPress():
    while (True):
        sbb.wait_for_home_button()
        middle_button_press.set()
        print("middle button pressed")

def updateDisplay():
    global page
    global instr_num

    while True:
        print(page)
        if page == "Start-Up":
            displayStartup()
        elif page == "Instructions":
            if left_button_press.is_set():
                page = "Start-Up"
            if right_button_press.is_set():
                page = "End"
            if middle_button_press.is_set():
                page = "Debug"
        elif page == "Debug":
            if left_button_press.is_set():
                page = "Instructions"
            if right_button_press.is_set():
                page = "End"
            if middle_button_press.is_set():
                page = "Help"
        elif page == "Help":
            if left_button_press.is_set():
                page = "Debug"
            if right_button_press.is_set():
                page = "Instructions"
            if middle_button_press.is_set():
                page = "Instructions"
        elif page == "End":
            if left_button_press.is_set():
                page = "Start-Up"
            if right_button_press.is_set():
                page = "Start-Up"
            if middle_button_press.is_set():
                page = "Start-Up"

        if rfid_tap.is_set():
            print("rfid tapped")
            page = "Instructions"
            instr_num = 1
            rfid_tap.clear()
        if left_button_press.is_set():
            left_button_press.clear()
        if right_button_press.is_set():
            right_button_press.clear()
        if middle_button_press.is_set():
            middle_button_press.clear()

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
right_button_thread = Thread(target=rightButtonPress)
middle_button_thread = Thread(target=middleButtonPress)

disp = sbb.setupDisplay()
sbb.clearDisplay(disp)
sbb.setupButtons()

display_thread.start()
rfid_thread.start()
left_button_thread.start()
right_button_thread.start()
middle_button_thread.start()

display_thread.join()
rfid_thread.join()
left_button_thread.join()
right_button_thread.join()
middle_button_thread.join()
