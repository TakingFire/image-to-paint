from subprocess import Popen
import PySimpleGUI as sg
import pyautogui as gui
from PIL import Image
import time

gui.PAUSE = 0
screen_w, screen_h = gui.size()
screenratio_h = screen_h / 2160
screenratio_w = screen_w / 3840

margin_h = ((45 + 242+ 52)*screenratio_h +10)
margin_w = (10)

image = Image.open(r'image.png').convert('L') # Enter image name
image_w, image_h = image.size

# Note: I would use tuples or lists for each pair, but this is easier to subtract
canvas_h = int((screen_h - margin_h))
canvas_w = int((screen_w - margin_w))

# Resize image if bigger than the canvas
ratio_h = (image_h / image_w)
ratio_w = (image_w / image_h)

if image_h > canvas_h:
    image2 = image.resize((round(canvas_h * ratio_w), canvas_h))
    image_w, image_h = image2.size
elif image_w > canvas_w:
    image2 = image.resize((canvas_w, round(canvas_w * ratio_h)))
    image_w, image_h = image2.size

# Print some stats
print(f'Canvas size: ({canvas_w} x {canvas_h})')
print(f'Image size:  ({image_w} x {image_h})')
print(f'Estimated time: {round((image_h*image_w)*0.0025)} seconds')

# Open paint and fit canvas to new image
Popen('mspaint')
time.sleep(1)
gui.hotkey('win', 'up')
gui.hotkey('ctrl', 'e')
gui.write(str(image_w))
gui.press('tab')
gui.write(str(image_h))
gui.press('enter')

# Automatically set up pencil and colors
time.sleep(.1)
gui.click(470*screenratio_w, 140*screenratio_h)
time.sleep(.01)
gui.click(1416*screenratio_w, 170*screenratio_h)
time.sleep(.01)
gui.click(1524*screenratio_w, 124*screenratio_h)
time.sleep(.01)
gui.moveTo(5, (margin_h-10)-5)
time.sleep(.2)

# Iterate through pixels and do stuff

def looppx():
    pixels = image.getdata()
    col, row = 1, 0
    for color in pixels:
        if col > image_w:
            col = 1
            row += 1
            gui.moveTo(5, (margin_h-10)-5 +row)
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
