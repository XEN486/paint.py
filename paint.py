import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # hide pygame prompt
import pygame, sys, random
from platform import python_version
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, askopenfilename
import pygame.gfxdraw

root = tk.Tk() # create tk window
root.withdraw() # hide tk window

cM = False # circle mode
lM = False # line mode
sM = True # square mode
fM = False # fill mode

hidden = False # wysiwyg

lT = 0 # times mouse has been clicked while in line mode
p1 = (0, 0)

mx = 0
my = 0

pygame.font.init() # this is needed just to make some stuff work


def flood_fill(surface, position, fill_color, size):
    fill_color = surface.map_rgb(fill_color)  # Convert the color to mapped integer value.
    surf_array = pygame.surfarray.pixels2d(surface)  # Create an array from the surface.
    current_color = surf_array[position]  # Get the mapped integer color value.

    # 'frontier' is a list where we put the pixels that's we haven't checked. Imagine that we first check one pixel and 
    # then expand like rings on the water. 'frontier' are the pixels on the edge of the pool of pixels we have checked.
    #
    # During each loop we get the position of a pixel. If that pixel contains the same color as the ones we've checked
    # we paint it with our 'fill_color' and put all its neighbours into the 'frontier' list. If not, we check the next
    # one in our list, until it's empty.

    frontier = [position]
    while len(frontier) > 0:
        x, y = frontier.pop()
        if x > size[0] or x < 0:
            continue
        if y > size[1] or y < 0:
            continue
        try:  # Add a try-except block in case the position is outside the surface.
            if surf_array[x, y] != current_color:
                continue
        except IndexError:
            continue
        surf_array[x, y] = fill_color
        # Then we append the neighbours of the pixel in the current position to our 'frontier' list.
        
        frontier.append((x, y - 1))  # Up.
        frontier.append((x, y + 1))  # Down.
        frontier.append((x - 1, y))  # Left.
        frontier.append((x + 1, y))  # Right.

    pygame.surfarray.blit_array(surface, surf_array)

def save():
    files = [('PNG Files', '*.png'),
             ('All Files', '*.*')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    if file != None:
        file.close()
    return file

def openF():
    files = [('PNG Files', '*.png'),
             ('All Files', '*.*')]

    filename = askopenfilename(filetypes = files, defaultextension = files)
    return filename

with open('options.cfg', 'r') as f:
    options = f.read()

options = options.split(' ')
size = (int(options[0]), int(options[1])) # width, height
brushThickness = 10 # brush thickness
scr = pygame.display.set_mode(size) # set res

screen = pygame.surface.Surface(size)
textSurface = pygame.surface.Surface((85, 50), flags=pygame.SRCALPHA)
cursorSurface = pygame.surface.Surface(size, flags=pygame.SRCALPHA)

clock = pygame.time.Clock() # create a clock
icon = pygame.image.load('./Resources/icon.png') # load our icon

myfont = pygame.font.SysFont('Arial', 10)

paintMsgs = ['Paint lives!', 'Hello, paint!', 'The world is made of paint!', 'Paint is now running!', 'Paint, now with colour!', 'Paint program', 'Paint!!', 'This changes every run!', 'paint.net more like paint.py!', 'Brought to you by: XENON, Con and Stefix1', 'This is the last one!']
paintMsg = random.choice(paintMsgs) # set the first line printed by console

pygame.display.set_icon(icon) # set the icon
    
backgroundCol = (255,255,255)
brushCol = (0,0,0)

screen.fill(backgroundCol)

sdlVer = ""
sdlVer += str(pygame.get_sdl_version()[0]) + "." # get first version num
sdlVer += str(pygame.get_sdl_version()[1]) + "." # get second version num
sdlVer += str(pygame.get_sdl_version()[2]) # get third version num

def renderText(bSize):
    textSurface.fill(backgroundCol)
    inverseBackground = (255-backgroundCol[0], 255-backgroundCol[1], 255-backgroundCol[2])
    colorText = myfont.render('Colour:', True, inverseBackground, backgroundCol)
    brushText = myfont.render('Brush Size: {}x'.format(bSize), True, inverseBackground, backgroundCol)
    mposText = myfont.render('X: {}, Y: {}'.format(mx, my), True, inverseBackground, backgroundCol)
    if cM:
        modeText = myfont.render('Circle Mode', True, inverseBackground, backgroundCol)
        textSurface.blit(mposText, (0, 30))
    elif lM:
        modeText = myfont.render('Line Mode', True, inverseBackground, backgroundCol)
        if lT == 0:
            pointText = myfont.render('Select P1', True, inverseBackground, backgroundCol)
            textSurface.blit(pointText, (0, 30))
            textSurface.blit(mposText, (0, 40))
        elif lT == 1:
            pointText = myfont.render('Select P2', True, inverseBackground, backgroundCol)
            textSurface.blit(pointText, (0, 30))
            textSurface.blit(mposText, (0, 40))
    elif sM:
        modeText = myfont.render('Square Mode', True, inverseBackground, backgroundCol)
        textSurface.blit(mposText, (0, 30))
    elif fM:
        modeText = myfont.render('Fill Mode', True, inverseBackground, backgroundCol)
        textSurface.blit(mposText, (0, 30))
    textSurface.blit(colorText, (0, 0))
    textSurface.blit(brushText, (0, 10))
    textSurface.blit(modeText, (0, 20))
    pygame.draw.rect(textSurface, brushCol, pygame.Rect((35, 0), (10,10)))

def updateText():
    if brushThickness == 10:
        renderText(1)

    elif brushThickness == 5:
        renderText(0.5)

    elif brushThickness == 2.5:
        renderText(0.25)
    
    else:
        renderText(brushThickness-10)

pygame.display.set_caption('paint.py')

print(f'{paintMsg}\n\nWARNING: Changing background colour clears the screen!\n\nPython Version: {python_version()}\nSDL Version: {sdlVer}\nPygame Version: {pygame.version.ver}\n\nLeft Click - brush tool\nRight Click - eraser tool\nF - enable/disable fill tool\nH - enable/disable wysiwyg mode\nW - activate square mode\nE - activate line mode\nR - activate circle drawing mode\nC - clear screen\nP - pick brush colour\nB - pick background colour\nS - save image\nI - import image\nO - Pick a colour on screen\n1-= - various brush sizes')

while True:
    updateText()
    if cM:
        pygame.draw.circle(cursorSurface, brushCol, (mx-5, my-5), brushThickness)
    elif lM:
        if lT == 1:
            #pygame.draw.line(screen, brushCol, p1, (mx, my), int(brushThickness))
            pygame.draw.line(cursorSurface, brushCol, p1, (mx, my), int(brushThickness))
        else:
            pygame.draw.rect(cursorSurface, brushCol, pygame.Rect((mx-5, my-5), (brushThickness, brushThickness)))
    else:
        pygame.draw.rect(cursorSurface, brushCol, pygame.Rect((mx-5, my-5), (brushThickness, brushThickness)))
    cursorSurface.set_alpha(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit event
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # key press event
            if event.key == pygame.K_c:
                screen.fill((backgroundCol))

            if event.key == pygame.K_p:
                prevBrushCol = brushCol
                brushCol = askcolor(title="Brush Colour Picker")[0] # askcolor gives us a dialog
                if brushCol == None:
                    brushCol = prevBrushCol # if we didn't set our background colour

            if event.key == pygame.K_b:
                prevBackgroundCol = backgroundCol
                backgroundCol = askcolor(title="Background Colour Picker")[0] # askcolor gives us a dialog
                if backgroundCol == None:
                    backgroundCol = prevBackgroundCol # if we didn't set our background colour
                else:
                    screen.fill(backgroundCol)
                    brushThickness = 10
                    updateText()

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
                brushThickness = 2.5
                updateText()

            if event.key == pygame.K_2:
                brushThickness = 5
                updateText()

            if event.key == pygame.K_3:
                brushThickness = 10
                updateText()

            if event.key == pygame.K_4:
                brushThickness = 15
                updateText()

            if event.key == pygame.K_5:
                brushThickness = 20
                updateText()

            if event.key == pygame.K_6:
                brushThickness = 25
                updateText()

            if event.key == pygame.K_7:
                brushThickness = 30
                updateText()

            if event.key == pygame.K_8:
                brushThickness = 35
                updateText()

            if event.key == pygame.K_9:
                brushThickness = 40
                updateText()

            if event.key == pygame.K_0:
                brushThickness = 45
                updateText()

            if event.key == pygame.K_MINUS:
                brushThickness = 50
                updateText()

            if event.key == pygame.K_EQUALS:
                brushThickness = 55
                updateText()

            if event.key == pygame.K_r:
                lM = False
                sM = False
                if cM:
                    cM = False
                    sM = True
                else:
                    cM = True
                updateText()

            if event.key == pygame.K_e:
                cM = False
                sM = False
                fM = False
                if lM:
                    sM = True
                else:
                    lM = True
                updateText()

            if event.key == pygame.K_w:
                cM = False
                lM = False
                sM = True
                updateText()

            if event.key == pygame.K_h:
                hidden = not hidden
                if hidden:
                    textSurface.set_alpha(0)
                else:
                    textSurface.set_alpha(255)

            if event.key == pygame.K_f:
                cM = False
                sM = False
                lM = False
                fM = not fM
                if not fM:
                    sM = True
                updateText()

        mx, my = pygame.mouse.get_pos() # mouse x pos, mouse y pos
        if pygame.mouse.get_pressed()[0]:
            if cM:
                pygame.draw.circle(screen, brushCol, (mx-5, my-5), brushThickness)
            elif sM:
                pygame.draw.rect(screen, brushCol, pygame.Rect((mx-5, my-5), (brushThickness,brushThickness))) # on mouse button left pressed down, draw a tiny square
            elif lM:
                updateText()
                lT += 1
                if lT == 1:
                    updateText()
                    p1 = (mx, my)
                elif lT == 2:
                    pygame.draw.line(screen, brushCol, p1, (mx, my), int(brushThickness))
                    lT = 0
                    updateText()

            elif fM:
                flood_fill(screen, (mx, my), brushCol, size)
        if pygame.mouse.get_pressed()[2]:
            pygame.draw.rect(screen, backgroundCol, pygame.Rect((mx-5, my-5), (brushThickness,brushThickness))) # on mouse button right pressed down, draw a tiny square in the colour of the background
        scr.blit(screen, (0, 0)) # display everything on the image layer
        scr.blit(textSurface, (0, 0)) # display everything on the text layer
        scr.blit(cursorSurface, (0, 0)) # display transparent cursor

        pygame.display.flip()
        cursorSurface.fill((0,0,0,0))
        clock.tick()
        
