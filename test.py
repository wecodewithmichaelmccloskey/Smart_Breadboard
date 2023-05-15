import Smart_Breadboard as sbb
from display import Display
from threading import Thread, Lock, Event
import time
import random

# {rfid_num: filename}
global card_dict
card_dict = {247721997126: "sample_circuit.csv"}

global curr_rfid_num
curr_rfid_num = None

next_button_press = Event()

def rfidTap():
    global card_dict
    global curr_rfid_num

    while(True):
        rfid_num = sbb.readCard()
        if rfid_num != curr_rfid_num and rfid_num != None:
            print("New Card!")
            curr_rfid_num = rfid_num
            display.load_new_circuit(card_dict[rfid_num])

def nextButtonPress():
    while (True):
        # sbb.wait_for_next_button()
        time.sleep(random.randint(5, 10))
        next_button_press.set()
        print("next button pressed")

def updateDisplay():
    while(True):
        display.display_current_page()

        if next_button_press.is_set():
            display.move_to_next_page()
            next_button_press.clear()
        time.sleep(0.1)

display_thread = Thread(target=updateDisplay)
rfid_thread = Thread(target=rfidTap)
next_button_thread = Thread(target=nextButtonPress)

sbb.setupButtons()
display = Display()

display_thread.start()
rfid_thread.start()
next_button_thread.start()
display_thread.join()
rfid_thread.join()
next_button_thread.join()
