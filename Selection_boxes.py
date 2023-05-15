import Smart_Breadboard as sbb

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
NYU_PURPLE = (86, 1, 141)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

disp = sbb.setupDisplay()
left_selection_image = sbb.createNewImage(disp)
left_selection_draw = sbb.createDrawing(left_selection_image)
sbb.drawRectangle(left_selection_draw, 0, 0, 240, 320, NYU_PURPLE)
sbb.drawRectangle(left_selection_draw, 240, 0, 240, 320, WHITE)
sbb.addText(left_selection_draw, "Current Reading", 50, 140, 30, 140, WHITE)
sbb.addText(left_selection_draw, "Voltage Reading", 290, 140, 30, 140, BLACK)

right_selection_image = sbb.createNewImage(disp)
right_selection_draw = sbb.createDrawing(right_selection_image)
sbb.drawRectangle(right_selection_draw, 0, 0, 240, 320, WHITE)
sbb.drawRectangle(right_selection_draw, 240, 0, 240, 320, NYU_PURPLE)
sbb.addText(right_selection_draw, "Current Reading", 50, 140, 30, 140, BLACK)
sbb.addText(right_selection_draw, "Voltage Reading", 290, 140, 30, 140, WHITE)

left_selection = True

while(True):
    if left_selection == True:
        sbb.sendToDisplay(disp, left_selection_image)
    else:
        sbb.sendToDisplay(disp, right_selection_image)
    if input() == "":
        left_selection = not left_selection
