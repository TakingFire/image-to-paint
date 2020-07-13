from subprocess import Popen
import PySimpleGUI as sg
import pyautogui as gui
from PIL import Image
from sys import exit
import time

# Necessary function for bundling icons with pyinstaller
import sys, os
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

sg.theme('SystemDefaultForReal')

gui.PAUSE = 0
screen_w, screen_h = gui.size()

# Margin is left here only to calculate the rough canvas
margin_h = ((46 + 242+ 52)*(screen_h / 2160) +10)
margin_w = (10)
canvas_h = int((screen_h - margin_h))
canvas_w = int((screen_w - margin_w))

# Establish UI layout
column1 = [[sg.Text('Select an image:')],
          [sg.InputText('', size=(30, 1), disabled=True, enable_events=True, key='Input'), sg.FileBrowse('🗁', key='Browse')],
          [sg.Text('', size=(30, 1), justification='right', key='Resize')]]

column2 = [[sg.Text('Estimated Time:\nUnknown', key='Estimate')],
          [sg.Text(f'Canvas size: {canvas_w} x {canvas_h}\nImage size: Unknown', key='Stats')]]

layout = [[sg.Column(column1), sg.VerticalSeparator(), sg.Column(column2)],
          [sg.HorizontalSeparator()],
          [sg.Button('Begin'), sg.Button('Exit'), sg.Text('To terminate the process, move the mouse to a screen corner.')]]

window = sg.Window('Image to Paint - Pixel by pixel', layout)

# Loop for UI interaction / image selection
while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'): exit()
    try:
        image = Image.open(values['Input']).convert('L') # Enter image name
        image_w, image_h = image.size
    except AttributeError: continue

    window['Stats'].update(f'Canvas size: {canvas_w} x {canvas_h}\nImage size: {image_w} x {image_h}')
    window['Estimate'].update(f'Estimated Time:\n{round(((image_h*image_w)*0.0025)/60)} minutes')

    if image_h > canvas_h or image_w > canvas_w:
        window['Resize'].update('The image will be automatically resized.')
    if event == 'Begin':
        window.close()
        break

# Resize image if bigger than the canvas
ratio_h = (image_h / image_w)
ratio_w = (image_w / image_h)

if image_h > canvas_h:
    image2 = image.resize((round(canvas_h * ratio_w), canvas_h))
    image_w, image_h = image2.size
elif image_w > canvas_w:
    image2 = image.resize((canvas_w, round(canvas_w * ratio_h)))
    image_w, image_h = image2.size

# Open paint and fit canvas to new image
Popen('mspaint')
time.sleep(1)
gui.hotkey('win', 'up')
gui.hotkey('ctrl', 'e')
gui.write(str(image_w))
gui.press('tab')
gui.write(str(image_h))
gui.press('enter')

# Attempt to use specific icons for resolution range
def iconpath(file):
    if screen_h >= 2160:
        return gui.locateCenterOnScreen(resource_path('C:/Users/BACur/Documents/Python Scripts/image-to-paint/icons/' + file + '.png'), confidence=0.5)
    elif screen_h in range(1440, 2160):
        return gui.locateCenterOnScreen(resource_path('C:/Users/BACur/Documents/Python Scripts/image-to-paint/icons/' + file + '2.png'), confidence=0.5)
    elif screen_h < 1440:
        return gui.locateCenterOnScreen(resource_path('C:/Users/BACur/Documents/Python Scripts/image-to-paint/icons/' + file + '3.png'), confidence=0.5)

# Automatically set up pencil and colors
time.sleep(2)
x, y = iconpath('pencil')
gui.click(x, y)
x, y = iconpath('c2')
gui.click(x, y)
x, y = iconpath('grey')
gui.click(x, y)
x, y = iconpath('canvas')
gui.moveTo(x, y)
time.sleep(.2)

# Iterate through pixels and do stuff
def looppx():
    pixels = image.getdata()
    col, row = 1, 0
    for color in pixels:
        if col > image_w:
            col = 1
            row += 1
            gui.moveTo(x, y +row)
        if color in range(0, 85):
            gui.click()
        elif color in range(86, 174): # Adjust these for the color sensitivity
            gui.rightClick()
        elif color in range(175, 256):
            pass
        gui.moveRel(1, 0)
        col += 1

if __name__ == "__main__":
    looppx()
