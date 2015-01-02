import pyglet # pyglet library, the graphical library to use, supporting audio
from os.path import join # Dealing with paths

################################################################################
##################### DATA STRUCTURES ##########################################
################################################################################
#------------------------------------------------------------------------------#
#               Strings                                                        #
#------------------------------------------------------------------------------#
SOUND_DIR = "sounds" # Directory of sound resources
ToPlay = "" # Music code to play
Played = "" # Music code already played
mode = "pause"
symbols = " !@#$%^&*()-_+=\"\:;\',./\\[]{}1234567890"
Editor = ""
Info = ""

#~~~~~~~~~~~~~~~ Songs ~~~~~~~~~~~~~~~~~~
Dragon = \
"F-GHI-JIH-HGF   F-GHI-JIH-HIJ   F-GHI-JIH-HGF   G-G-G-HGF-FEF   \
J-J-J-IHI-IJI   H-H-H-IHG-GHG   J-J-J-IHI-IJI   H-H-G-HGF-FEF"
Tomorrow = \
"JJL-L-LL-LMLK- JKL-L-JIH-I--- JIHH-HHOO-NN-ONML-MLK-KLMLL---- O-O---MLL-ML----\
M-M-LH-IJ----- I-H--HHJ-JJII-I--II-I-NM-      \
MMMNO-MLNN-OP-N- ONMLLHIJJ-- J-N-NN-JP-P-O-NMM----\
MMMNON-MNN-OP-NNQ-----POO----- NM-M-MM--L-L-IJ--H"

#------------------------------------------------------------------------------#
#               Numerical States                                               #
#------------------------------------------------------------------------------#
winw = 800
winh = 500
texth = 40
texts = 20
interval = 0.12
maxPlayedSize = 30
maxAppendSize = 30
#------------------------------------------------------------------------------#
#               Pyglet Objects                                                 #
#------------------------------------------------------------------------------#
window = pyglet.window.Window() # Create window
window.set_size(winw,winh) # Set window size

#------------------------------------------------------------------------------#
#               Arrays                                                         #
#------------------------------------------------------------------------------#
# Alphabeta: from "A" to "Z"
alphabeta = [chr(i) for i in range(ord("A"),ord("Z")+1)]
symbolnum = [ord(c) for c in symbols]
#------------------------------------------------------------------------------#
#               Dictionaries                                                   #
#------------------------------------------------------------------------------#
sounds = {} # The map from alphabeta to the corresponding media object

################################################################################
################# FUNCTIONS ####################################################
################################################################################

#------------------------------------------------------------------------------#
#               File Processing                                                #
#------------------------------------------------------------------------------#
# Open file s.mp3 and store the media object into the dictionary
def getSound(s):
    # Open audio files
    m = pyglet.media.load(join(SOUND_DIR,"%s.mp3"%s),streaming=False)
    # Store m into dictionary sounds, under key s
    sounds[s] = m

#------------------------------------------------------------------------------#
#               Command Operation                                              #
#------------------------------------------------------------------------------#
def startPlaying():
    global mode
    mode = "playing"
    pyglet.clock.unschedule(autoPlay) # In case already playing
    pyglet.clock.schedule_interval(autoPlay,interval) # Start playing

def pause():
    global mode
    mode = "pause"
    pyglet.clock.unschedule(autoPlay) # Stop playing

# Entering append mode
def appendMode():
    global mode
    mode = "append"

# Entering edit mode
def editMode():
    global mode
    mode = "edit"

# Entering file open mode
def fileMode():
    global mode
    mode = "file"

# Entering play append mode
def playAppend():
    global mode
    mode = "play append"

# Entering play append mode
def playEdit():
    global mode
    mode = "play edit"

# Reset
def reset():
    global mode, ToPlay, Played, Editor
    mode = "pause"
    ToPlay = ""
    Played = ""
    Editor = ""

# Enter practise mode
def practise():
    global mode
    mode = "practise"

def command(c):
    if c == "c": # Ctrl-C
        pause()
    elif c == "p": # Ctrl-P
        startPlaying()
    elif c == "a": # Ctrl-A
        appendMode()
    elif c == "e": # Ctrl-E
        editMode()
    elif c == "f": # Ctrl-F
        fileMode()
    elif c == "r": # Ctrl-R
        reset()
    elif c == "l": # Ctrl-L
        practise()
    elif c == "A": # Shift-A
        playAppend()
    elif c == "E": # Shift-A
        playEdit()

#------------------------------------------------------------------------------#
#               Sound Manipulation                                             #
#------------------------------------------------------------------------------#
# Play the sound given single char c
def playC(c):
    global Played
    Played += c
    # Play the char and log it in the string Played
    if c.isupper():
        sounds[c].play()
    elif c.islower():
        sounds[c.upper()].play()

# Play function invoked by schedule
def autoPlay(dt):
    global ToPlay
    # If the music to play is empty, stop
    if ToPlay == "": return
    # Take the first character out and play it
    c = ToPlay[0]
    playC(c)
    ToPlay = ToPlay[1:]

# Append music to the ToPlay string
def appendPlay(music):
    global ToPlay
    ToPlay += music

# Play an encoding of a piece of music
def play(music):
    global ToPlay
    ToPlay = music
    startPlaying()

#------------------------------------------------------------------------------#
#               Functions invoked by callback functions                        #
#------------------------------------------------------------------------------#
# Function invoked when an alphabeta key is pressed
def alphaKeyPress(c):
    global Editor, ToPlay
    if mode == "playing" or mode == "pause":
        if c.isupper():
            command(c)
        elif c.islower():
            playC(c.upper())
    elif mode == "append" or mode == "edit" or mode == "file":
        Editor += c
    elif mode == "play append" or mode == "play edit":
        Editor += c.upper()
        playC(c.upper())
    elif mode == "practise":
        if ToPlay == "":
            pause()
        else:
            n = ToPlay[0]
            if c == n or c.upper() == n:
                playC(c.upper())
                while True:
                    ToPlay = ToPlay[1:]
                    if len(ToPlay) == 0 or ToPlay[0].isalpha():
                        break

# Function invoked when a symbol key is pressed
def symbolKeyPress(c):
    global Editor
    if mode == "playing" or mode == "pause":
        playC(c)
    elif mode == "append" or mode == "edit" or mode == "file":
        Editor += c
    elif mode == "play append" or mode == "play edit":
        Editor += c
        playC(c)

# Function invoked when ESC is pressed
def escPress():
    pass

def backspacePress():
    global Editor
    if mode == "append" or mode == "play append" \
    or mode == "edit" or mode == "play edit" \
    or mode == "file":
        Editor = Editor[:-1]

def returnPress():
    global mode, ToPlay, Editor, filename, Info
    if mode == "append" or mode == "play append":
        pause()
        ToPlay += Editor
        Editor = ""
    elif mode == "edit" or mode == "play edit":
        pause()
        ToPlay = Editor
        Editor = ""
    elif mode == "file":
        try:
            with open(Editor) as f:
                ToPlay += "".join(f.readlines())
        except:
            Info = "%s: File not found."%Editor
        pause()
        Editor = ""

#------------------------------------------------------------------------------#
#               Draw functions                                                 #
#------------------------------------------------------------------------------#
# Routine of Drawing Rectangle
def drawRectangle(x0,y0,x1,y1,outline,fill):
    if outline:
        r,g,b=outline[0],outline[1],outline[2]
        pyglet.graphics.draw(4,pyglet.gl.GL_LINE_LOOP,\
            ('v2i',(x0,y0,x1,y0,x1,y1,x0,y1)),\
            ('c3B',(r,g,b,r,g,b,r,g,b,r,g,b))\
        )
    if fill:
        r,g,b=fill[0],fill[1],fill[2]
        pyglet.graphics.draw(4,pyglet.gl.GL_QUADS,\
            ('v2i',(x0,y0,x1,y0,x1,y1,x0,y1)),\
            ('c3B',(r,g,b,r,g,b,r,g,b,r,g,b))\
        )

def drawText(text,x0,y0,size,fill):
    r,g,b=fill[0],fill[1],fill[2]
    pyglet.text.Label(text,anchor_x="left",anchor_y="bottom",\
        x=x0,y=y0,color=(r,g,b,255),font_name="Arial",font_size=size).draw()

# Draw the background -- white box filling the window
def drawBackground():
    drawRectangle(0,0,winw,winh,None,[255,255,255])

# Draw the text informations
def drawInfo():
    drawText("Music: %s"%ToPlay,0,winh-texth,texts,[0,0,0])
    drawText("Played: %s"%Played[-1-maxPlayedSize:],\
        0,winh-texth*2,texts,[0,0,0])
    if mode == "append":
        drawText("Append: %s"%Editor[-1-maxAppendSize:],\
                 0,winh-texth*3,texts,[0,0,0])
    elif mode == "play append":
        drawText("Append: %s"%Editor[-1-maxAppendSize:],\
                 0,winh-texth*3,texts,[0,0,0])
    elif mode == "edit":
        drawText("Edit: %s"%Editor[-1-maxAppendSize:],\
                 0,winh-texth*3,texts,[0,0,0])
    elif mode == "play edit":
        drawText("Edit: %s"%Editor[-1-maxAppendSize:],\
                 0,winh-texth*3,texts,[0,0,0])
    elif mode == "file":
        drawText("File: %s"%Editor[-1-maxAppendSize:],\
                 0,winh-texth*3,texts,[0,0,0])
    if Info == "":
        drawText("%s"%mode,0,0,texts,[0,0,0])
    else:
        drawText("%s"%Info,0,0,texts,[0,0,0])

################################################################################
################# INITIALIZATION ###############################################
################################################################################

# Load all the sound files
for s in alphabeta:
    getSound(s)

# appendPlay(Tomorrow)

################################################################################
################### CALL BACK FUNCTIONS ########################################
################################################################################

# Callback function: onKeyPress
@window.event
def on_key_press(symbol,modifiers):
    global Info # Information string, any key will erase it
    Info = ""
    # If symbol is between 'a' and 'z'
    if symbol >= pyglet.window.key.A and symbol <= pyglet.window.key.Z:
        # Pressing ctrl, invoke command
        if modifiers & pyglet.window.key.MOD_CTRL:
            command(chr(symbol))
        elif modifiers & pyglet.window.key.MOD_SHIFT:
            alphaKeyPress(chr(symbol).upper())
        else:
            # Invoke the alphakeyPress function
            alphaKeyPress(chr(symbol))
    elif symbol in symbolnum:
        symbolKeyPress(chr(symbol))
    # Esc key pressed
    elif symbol == pyglet.window.key.ESCAPE:
        escPress()
    elif symbol == pyglet.window.key.BACKSPACE:
        backspacePress()
    elif symbol == pyglet.window.key.RETURN:
        returnPress()

# Callback function: onDraw
@window.event
def on_draw():
    # Clear the window
    window.clear()
    drawBackground()
    drawInfo() # Draw the text informations
        
################################################################################

# Start the application
pyglet.app.run()
