import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # hide pygame prompt
import pygame, sys, random
from platform import python_version
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, askopenfilename

root = tk.Tk() # create tk window
root.withdraw() # hide tk window

pygame.font.init() # this is needed just to make some stuff work

def save():
    files = [('PNG Files', '*.png'),
             ('All Files', '*.*')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    file.close()
    return file

def openF():
    files = [('PNG Files', '*.png'),
             ('All Files', '*.*')]

    filename = askopenfilename()
    return filename

with open('options.cfg', 'r') as f:
    options = f.read()

options = options.split(' ')
size = (int(options[0]), int(options[1])) # width, height
brushThickness = 10 # brush thickness
scr = pygame.display.set_mode(size) # set res

screen = pygame.surface.Surface(size)
textSurface = pygame.surface.Surface((80, 20))
finalSurface = pygame.surface.Surface(size)

clock = pygame.time.Clock() # create a clock
icon = pygame.image.load('./Resources/icon.png') # load our icon

myfont = pygame.font.SysFont('Arial', 10)

paintMsgs = ['Paint lives!', 'Hello, paint!', 'The world is made of paint!', 'Paint is now running!', 'Paint, now with colour!', 'Paint program', 'Paint!!', 'This changes every run!', 'paint.net more like paint.py!', 'This is the last one!']
paintMsg = random.choice(paintMsgs) # set the first line printed by console

pygame.display.set_icon(icon) # set the icon
pygame.display.set_caption('paint.py') # set the title
    
backgroundCol = (255,255,255)
brushCol = (0,0,0)

screen.fill(backgroundCol)

sdlVer = ""
sdlVer += str(pygame.get_sdl_version()[0]) + "." # get first version num
sdlVer += str(pygame.get_sdl_version()[1]) + "." # get second version num
sdlVer += str(pygame.get_sdl_version()[2]) # get third version num

print(f'{paintMsg}\n\nWARNING: Changing background colour clears the screen!\n\nPython Version: {python_version()}\nSDL Version: {sdlVer}\nPygame Version: {pygame.version.ver}\n\nLeft Click - Brush Tool\nRight Click - Eraser Tool\nC - clear screen\nP - pick brush colour\nB - pick background colour\nS - save image\nI - import image\nO - Pick a colour on screen\n1-0 - various brush sizes')

def renderText(bSize):
    inverseBackground = (255-backgroundCol[0], 255-backgroundCol[1], 255-backgroundCol[2])
    textSurface.fill(backgroundCol)
    colorText = myfont.render('Colour:', True, inverseBackground, backgroundCol)
    brushText = myfont.render('Brush Size: {}x'.format(bSize), True, inverseBackground, backgroundCol)
    textSurface.blit(colorText, (0, 0))
    textSurface.blit(brushText, (0, 10))

renderText(1)

while True:
    pygame.draw.rect(textSurface, brushCol, pygame.Rect((35, 0), (10,10)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit event
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # key press event
            if event.key == pygame.K_c:
                screen.fill((backgroundCol))

            if event.key == pygame.K_p:
                prevBrushCol = brushCol
                brushCol = askcolor(title="Brush Colour Picker")[0] # askcolor gives us a dialog, this is why we needed to make a tk window
                if brushCol == None:
                    brushCol = prevBrushCol # if we didn't set our background colour

            if event.key == pygame.K_b:
                prevBackgroundCol = backgroundCol
                backgroundCol = askcolor(title="Background Colour Picker")[0] # askcolor gives us a dialog, this is why we needed to make a tk window
                if backgroundCol == None:
                    backgroundCol = prevBackgroundCol # if we didn't set our background colour
                else:
                    screen.fill(backgroundCol)
                    brushThickness = 10
                    renderText(1)

            if event.key == pygame.K_s:
                file = save()
                if file != None:
                    filePath = file.name
                    os.remove(filePath)
                    pygame.image.save(screen, filePath)

            if event.key == pygame.K_i:
                filePath = openF()
                if filePath != "":
                    loadedImg = pygame.image.load(filePath) # load our image
                    screen.fill((255,255,255)) # create a blank white canvas to blit our image onto
                    screen.blit(loadedImg, (0, 0)) # blit it

            if event.key == pygame.K_o:
                colour = screen.get_at((mx, my))
                brushCol = (colour[0], colour[1], colour[2])

            if event.key == pygame.K_1:
                brushThickness = 10
                renderText(1)

            if event.key == pygame.K_2:
                brushThickness = 15
                renderText(5)

            if event.key == pygame.K_3:
                brushThickness = 20
                renderText(10)

            if event.key == pygame.K_4:
                brushThickness = 25
                renderText(15)

            if event.key == pygame.K_5:
                brushThickness = 30
                renderText(20)

            if event.key == pygame.K_6:
                brushThickness = 35
                renderText(25)

            if event.key == pygame.K_7:
                brushThickness = 40
                renderText(35)

            if event.key == pygame.K_8:
                brushThickness = 45
                renderText(40)

            if event.key == pygame.K_9:
                brushThickness = 50
                renderText(45)

            if event.key == pygame.K_0:
                brushThickness = 55
                renderText(50)

        mx, my = pygame.mouse.get_pos() # mouse x pos, mouse y pos
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, brushCol, pygame.Rect((mx-5, my-5), (brushThickness,brushThickness))) # on mouse button left pressed down, draw a tiny square
            
        if pygame.mouse.get_pressed()[2]:
            pygame.draw.rect(screen, backgroundCol, pygame.Rect((mx-5, my-5), (brushThickness,brushThickness))) # on mouse button right pressed down, draw a tiny square in the colour of the background

        scr.blit(screen, (0, 0)) # display everything on the image layer
        scr.blit(textSurface, (0, 0)) # display everything on the text layer

        pygame.display.flip()
        clock.tick()
        
