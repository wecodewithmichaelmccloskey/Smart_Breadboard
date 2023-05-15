import Smart_Breadboard as sbb
from copy import deepcopy

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

class Page:
    def __init__(self, display, back, next):
        self.display = display
        self.back = back
        self.next = next
        self.image = sbb.createNewImage(self.display)
        self.drawing = sbb.createDrawing(self.image)
        sbb.drawRectangle(self.drawing, x = 0, y = 0, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, color = "white")

    def get_image(self):
        return self.image

    def drive_leds(self):
        sbb.turnOffAll()

    def get_next_page(self):
        return self

    def get_prev_page(self):
        return self

    def home(self):
        return None

class Start(Page):
    def __init__(self, display):
        Page.__init__(self, display, None, None)
        self.rfid_tapped = False
        sbb.addText(self.drawing, text = "Smart Breadboard", x = 81, y = 40, fontsize = 35, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Pick a Card", x = 45, y = 127, fontsize = 70, length = 480, color = "black")
        sbb.addText(self.drawing, text = "...", x = 207, y = 190, fontsize = 70, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Tap a card on the reader to start building a circuit", x = 17, y = 280, fontsize = 18, length = 480, color = "black")

    def get_image(self):
        print("Displaying Start")
        print()
        return self.image

    def rfid_tap(self):
        self.rfid_tapped = True
        return self.next

    def home(self):
        if self.rfid_tapped:
            return self.next
        return self

class Instruction(Page):
    def __init__(self, display, back, next, comp, nodes, picture, notes):
        Page.__init__(self, display, back, next)
        self.comp = comp
        self.nodes = self.addGNDVCC(nodes)
        self.led_nodes = self.removeGNDVCC(nodes)
        self.picture = picture
        self.notes = notes
        sbb.addText(self.drawing, "Connect " + str(self.comp) + " to nodes " + ", ".join([str(node) for node in self.nodes]), 250, 10, 24, 220, "black")
        if self.notes != "":
            sbb.addText(self.drawing, "Note: " + self.notes, 250, 100, 24, 220, "black")
        sbb.drawRectangle(self.drawing, x = 0, y = 250, width = DISPLAY_WIDTH, height = 2, color = "black")
        sbb.drawRectangle(self.drawing, x = 159, y = 250, width = 2, height = 70, color = "black")
        sbb.drawRectangle(self.drawing, x = 319, y = 250, width = 2, height = 70, color = "black")
        sbb.addText(self.drawing, text = "BACK", x = 25, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "HOME", x = 185, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "NEXT", x = 345, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addPicture(self.image, self.picture, 10, 10, 200)

    def get_image(self):
        print("Displaying Instruction:")
        print(self.comp)
        print(self.nodes)
        print(self.picture)
        print(self.notes)
        print()
        return self.image

    def drive_leds(self):
        sbb.turnOffAll()
        sbb.runLEDDebug(self.led_nodes, [])

    def addGNDVCC(self, nodes):
        nodes = deepcopy(nodes)
        while 0 in nodes:
            nodes.remove(0)
            nodes.append("Ground")
        while 10 in nodes:
            nodes.remove(10)
            nodes.append("3.3V")
        return nodes

    def removeGNDVCC(self, nodes):
        nodes = deepcopy(nodes)
        while 0 in nodes:
            nodes.remove(0)
        while 10 in nodes:
            nodes.remove(10)
        return nodes

    def get_next_page(self):
        return self.next

    def get_prev_page(self):
        return self.back

class Debug(Page):
    def __init__(self, display, back, next, text, low_voltage, high_voltage):
        Page.__init__(self, display, back, next)
        self.text = text
        self.low_voltage = low_voltage
        self.high_voltage = high_voltage
        self.locked = False
        self.warning = False
        self.help = None

        sbb.addText(self.drawing, text = self.text, x = 10, y = 10, fontsize = 24, length = 460, color = "black")
        sbb.addText(self.drawing, text = "Expected Voltage: " + str((low_voltage + high_voltage) // 2), x = 60, y = 100, fontsize = 20, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Measured Voltage: ", x = 60, y = 120, fontsize = 20, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Expected Current: ", x = 60, y = 140, fontsize = 20, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Measured Current: ", x = 60, y = 160, fontsize = 20, length = 480, color = "black")

        sbb.drawRectangle(self.drawing, x = 0, y = 250, width = DISPLAY_WIDTH, height = 2, color = "black")
        sbb.drawRectangle(self.drawing, x = 159, y = 250, width = 2, height = 70, color = "black")
        sbb.drawRectangle(self.drawing, x = 319, y = 250, width = 2, height = 70, color = "black")
        sbb.addText(self.drawing, text = "BACK", x = 25, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "HELP", x = 185, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "NEXT", x = 345, y = 266, fontsize = 40, length = 480, color = "black")

    def get_image(self):
        print("Displaying Debug:")
        print(self.text)
        print()
        if self.locked:
            symbol = "redminus.jpg"
        else:
            symbol = "greencheck.jpg"
        sbb.addPicture(self.image, symbol, 220, 200, 40)
        return self.image

    def get_next_page(self):
        if self.locked:
            self.warning = True
            return self
        else:
            return self.next

    def get_prev_page(self):
        return self.back

    def home(self):
        return self.help

class Help(Page):
    def __init__(self, display, back, next, suggestions):
        Page.__init__(self, display, back, next)
        self.suggestions = suggestions

        for i in range(len(self.suggestions)):
            sbb.addText(self.drawing, text = suggestions[i], x = 10, y = (i * 80 + 10), fontsize = 20, length = 480, color = "black")

        sbb.drawRectangle(self.drawing, x = 0, y = 250, width = DISPLAY_WIDTH, height = 2, color = "black")
        sbb.drawRectangle(self.drawing, x = 159, y = 250, width = 2, height = 70, color = "black")
        sbb.drawRectangle(self.drawing, x = 319, y = 250, width = 2, height = 70, color = "black")
        sbb.addText(self.drawing, text = "BACK", x = 25, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "HOME", x = 185, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "NEXT", x = 345, y = 266, fontsize = 40, length = 480, color = "black")

    def get_next_page(self):
        return self.next

    def get_prev_page(self):
        return self.back

class End(Page):
    def __init__(self, display):
        Page.__init__(self, display, None, None)

        sbb.addText(self.drawing, text = "Smart Breadboard", x = 81, y = 30, fontsize = 35, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Congratulations!", x = 35, y = 100, fontsize = 50, length = 480, color = "black")
        sbb.addText(self.drawing, text = "You completed the circuit", x = 40, y = 170, fontsize = 30, length = 480, color = "black")
        sbb.addText(self.drawing, text = "Tap a card on the reader to start building a new circuit", x = 17, y = 220, fontsize = 16, length = 480, color = "black")

        sbb.drawRectangle(self.drawing, x = 0, y = 250, width = DISPLAY_WIDTH, height = 2, color = "black")
        sbb.drawRectangle(self.drawing, x = 159, y = 250, width = 2, height = 70, color = "black")
        sbb.drawRectangle(self.drawing, x = 319, y = 250, width = 2, height = 70, color = "black")
        sbb.addText(self.drawing, text = "BACK", x = 25, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "NEXT", x = 185, y = 266, fontsize = 40, length = 480, color = "black")
        sbb.addText(self.drawing, text = "NEXT", x = 345, y = 266, fontsize = 40, length = 480, color = "black")

    def get_image(self):
        print("Displaying End")
        print()
        sbb.turnOffAll()
        return self.image

    def get_next_page(self):
        return self

    def get_prev_page(self):
        return self.back

class Display:
    def __init__(self):
        self.display = sbb.setupDisplay()
        sbb.clearDisplay(self.display)
        self.circuit_name = None
        self.start_page = Start(self.display)
        self.current_page = self.start_page

    def load_new_circuit(self, file_name):
        # open, read, and close file
        try:
            circuit_file = open(file_name, 'r')
        except FileNotFoundError:
            print("File not found")
            self.current_page = ["Start", None]
        circuit_file.readline()
        circuit_info = circuit_file.readline().split(",")
        circuit_file.close()

        # combine data that was split by "/,"
        index = 0
        while index != len(circuit_info):
            if circuit_info[index][-1] == "/":
                circuit_info[index] = circuit_info[index][0:-1] + "," + circuit_info.pop(index + 1)
            else:
                index += 1

        # sort circuit info into respective fields
        self.circuit_name = circuit_info[1].strip()

        prev_page = self.start_page
        for instr_info in circuit_info[2].split(";"):
            comp, nodes, picture, notes = instr_info.split(":")
            nodes = nodes.split("^")
            instr = Instruction(self.display, prev_page, None, comp.strip(), [int(node.strip()) for node in nodes], picture.strip(), notes.strip())
            prev_page.next = instr
            prev_page = instr

        for i in range(len(circuit_info[3].split(";"))):
            debug_info = circuit_info[3].split(";")[i]
            help_info = circuit_info[4].split(";")[i]

            text, low_voltage, high_voltage = debug_info.split(":")
            suggestions = help_info.split(":")

            debug = Debug(self.display, prev_page, None, text.strip(), int(low_voltage.strip()), int(high_voltage.strip())) 
            help = Help(self.display, debug, debug, [suggestion.strip() for suggestion in suggestions])
            debug.help = help

            prev_page.next = debug
            prev_page = debug

        prev_page.next = End(self.display)
        prev_page.next.back = prev_page
        prev_page.next.next = self.start_page

        self.current_page = self.start_page.rfid_tap()

    def display_current_page(self):
        sbb.sendToDisplay(self.display, self.current_page.get_image())
        self.current_page.drive_leds()

    def move_to_next_page(self):
        page = self.current_page.get_next_page()
        if page == None:
            self.current_page = self.start_page.next
        else:
            self.current_page = page

    def move_to_prev_page(self):
        prev_page = self.current_page.get_prev_page()
        if prev_page != self.start_page:
            self.current_page = prev_page

    def move_to_home_page(self):
        page = self.current_page.home()
        if page == None:
            self.current_page = self.start_page.next
        else:
            self.current_page = page
