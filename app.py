import Smart_Breadboard as sbb
from display import Display
from threading import Thread, Lock, Event
import random
import time

# {rfid_num: filename}
global card_dict
card_dict = {247721997126: "sample_circuit.csv"}

global curr_rfid_num
curr_rfid_num = None

back_button_press = Event()
next_button_press = Event()
home_button_press = Event()

def rfidTap():
    global card_dict
    global curr_rfid_num

    while True:
        print("Reading")
        rfid_num = sbb.readCard()
        print("read")
        if rfid_num != curr_rfid_num and rfid_num != None:
            print("New Card!")
            curr_rfid_num = rfid_num
            display.load_new_circuit(card_dict[rfid_num])
        time.sleep(0.1)

def nextButtonPress():
    while True:
        sbb.wait_for_next_button()
        next_button_press.set()
        print("next button pressed")

def backButtonPress():
    while True:
        sbb.wait_for_back_button()
        back_button_press.set()
        print("back button pressed")

def homeButtonPress():
    while True:
        sbb.wait_for_home_button()
        home_button_press.set()
        print("home button pressed")

def updateDisplay():
    while True:
        display.display_current_page()

        if next_button_press.is_set():
            display.move_to_next_page()
            next_button_press.clear()
        if back_button_press.is_set():
            display.move_to_prev_page()
            back_button_press.clear()
        if home_button_press.is_set():
            display.move_to_home_page()
            home_button_press.clear()
        time.sleep(0.1)

display_thread = Thread(target=updateDisplay)
rfid_thread = Thread(target=rfidTap)
next_button_thread = Thread(target=nextButtonPress)
back_button_thread = Thread(target=backButtonPress)
home_button_thread = Thread(target=homeButtonPress)
sbb.setupButtons()
display = Display()

display_thread.start()
rfid_thread.start()
next_button_thread.start()
back_button_thread.start()
home_button_thread.start()
display_thread.join()
rfid_thread.join()
next_button_thread.join()
back_button_thread.join()
home_button_thread.join()
