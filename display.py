import Smart_Breadboard as sbb

class Page:
    def __init__(self, back, next):
        self.back = back
        self.next = next

    def display_page(self):
        pass

    def get_next_page(self):
        pass

class Start(Page):
    def __init__(self):
        Page.__init__(self, None, None)

    def display_page(self):
        print("Displaying Start")
        print()

    def get_next_page(self):
        return self
    
    def rfid_tap(self):
        return self.next

class Instruction(Page):
    def __init__(self, back, next, text, image):
        Page.__init__(self, back, next)
        self.text = text
        self.image = image

    def display_page(self):
        print("Displaying Instruction:")
        print(self.image)
        print(self.text)
        print()

    def get_next_page(self):
        return self.next

class Debug(Page):
    def __init__(self, back, next, text, low_voltage, high_voltage,):
        Page.__init__(self, back, next)
        self.text = text
        self.low_voltage = low_voltage
        self.high_voltage = high_voltage
        self.locked = True
        self.warning = False

    def display_page(self):
        print("Displaying Debug:")
        print(self.text)
        print()

    def get_next_page(self):
        if self.locked:
            self.warning = True
            return self
        else:
            return self.next
        
class End(Page):
    def __init__(self):
        Page.__init__(self, None, None)

    def display_page(self):
        print("Displaying End")
        print()

    def get_next_page(self):
        return self

class Display:
    def __init__(self):
        self.circuit_name = None
        self.current_page = Start()
        self.warning = False
        self.start_page = self.build_start_page()
        self.instructions_page = self.build_instructions_page()
        self.debug_page = self.build_debug_page()
        self.warning = self.build_warning()
        self.resistor_check_page = self.build_resistor_check_page()
        self.voltage_check_page = self.build_voltage_check_page()
        self.end_page = self.build_end_page()
        self.display = sbb.setupDisplay()
        sbb.clearDisplay(self.display)

    def build_start_page(self):
        pass

    def build_instructions_page(self):
        pass

    def build_debug_page(self):
        pass

    def build_warning(self):
        pass

    def build_resistor_check_page(self):
        pass

    def build_voltage_check_page(self):
        pass
    
    def build_end_page(self):
        pass

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

        self.current_page = Start()
        prev_page = self.current_page
        for instr_info in circuit_info[2].split(";"):
            text, image = instr_info.split(":")
            instr = Instruction(prev_page, None, text.strip(), image.strip())
            prev_page.next = instr
            prev_page = instr

        for debug_info in circuit_info[3].split(";"):
            text, low_voltage, high_voltage = debug_info.split(":")
            debug = Debug(prev_page, None, text.strip(), int(low_voltage.strip()), int(high_voltage.strip()))
            prev_page.next = debug
            prev_page = debug

        prev_page.next = End()
        prev_page.next.back = prev_page
        prev_page.next.next = self.current_page

        self.current_page = self.current_page.rfid_tap()
        
    def display_current_page(self):
        self.current_page.display_page()

    def move_to_next_page(self):
        self.current_page = self.current_page.get_next_page()
