import Smart_Breadboard as sbb
from display import Display
from threading import Thread, Lock, Event
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

# {rfid_num, filename}
global card_dict
card_dict = {1: "sample_circuit.csv"}

global curr_rfid_num
curr_rfid_num = None

rfid_tap = Event()
back_button_press = Event()
next_button_press = Event()
home_button_press = Event()

def rfidTap():
    global card_dict
    global curr_rfid_num

    while True:
        time.sleep(random.randint(5, 10))
        print("rfid tapped")
        rfid_tap.set()
        rfid_num = 1 # replace with reading from rfid
        if rfid_num != curr_rfid_num:
            print("New Card!")
            curr_rfid_num = rfid_num
            display.load_new_circuit(card_dict[rfid_num])

def backButtonPress():
    while (True):
        sbb.wait_for_back_button()
        back_button_press.set()
        print("back button pressed")

def nextButtonPress():
    while (True):
        # sbb.wait_for_next_button()
        time.sleep(random.randint(5, 10))
        next_button_press.set()
        print("next button pressed")

def homeButtonPress():
    while (True):
        sbb.wait_for_home_button()
        home_button_press.set()
        print("middle button pressed")

def updateDisplay():
    while True:
        display.display_current_page()

        if next_button_press.is_set():
            display.move_to_next_page()
            next_button_press.clear()
        time.sleep(0.1)

display_thread = Thread(target=updateDisplay)
rfid_thread = Thread(target=rfidTap)
back_button_thread = Thread(target=backButtonPress)
next_button_thread = Thread(target=nextButtonPress)
home_button_thread = Thread(target=homeButtonPress)

sbb.setupButtons()
display = Display()

display_thread.start()
rfid_thread.start()
back_button_thread.start()
next_button_thread.start()
home_button_thread.start()

display_thread.join()
rfid_thread.join()
back_button_thread.join()
next_button_thread.join()
home_button_thread.join()
