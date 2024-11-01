
###### PROGRAM GUIDE ######

see tl;dr at bottom if you don't wanna read all of this

###### Main Menu ######
The main menu is simpily where the program loads; there is not much to experience there.

###### Note Editor ######

This DAW (Digital Audio Workstation) works by storing groups of notes in chunks called cells or bar groups. These cells are each exactly 2 bars long in the time signature 4/4. The program stores these bars under a number. In the timeline menu, you can slect which bar groups/cells you'd like to appear where. 

The note editor is where you place notes inside these cells/bar groups. You can see what bar group number you are editing in the top right of the screen of this menu as well as what channel you are editing.

To make more bar groups, you just have to press the right arrow key.

Keep in mind, bar groups are specific to their channel and cannot be accessed by other channels

Once you are done placing your notes, head over to the timeline

###### Timeline ######

The timeline is where you place together your bar chunks to form a song. 

The timeline can hold up to 10 instances of bar groups which is quite limiting but all I had time to implement

# Keyboard and Mouse #

# Main Menu #
Press E to access the note editor 
Press and hold H to view a help screen
press M to access the main menu
Press T to access the timeline 

# Note Editor #
Left click to place and/or delete notes (note lengths cannot be changed)
Use the arrow keys to move between/create new bars
Press SPACE to play/stop the currently viewed bars (notes: 1. this audio loops, 2. if you make changes to your melody while the program is playing, you must stop the audio and re start it)
Use number keys 1-4 to change between the 4 different channels
Press E to access the note editor 
Press and hold H to view a help screen
press M to access the main menu
Press T to access the timeline 

# Timeline #
Use the left and right arrow keys to move horizontally accross a channel
Use the up and down arrow keys to select different bars
Use number keys 1-4 to change the channel
Press SPACE to play/stop your audio (notes: 1. this audio loops, 2. if you make changes to the system while the audio is playing you must stop the audio and start it again for a change to be heard)
Press E to access the note editor 
Press and hold H to view a help screen
press M to access the main menu
Press T to access the timeline 


Credits and Special Thanks:
The code for the sine wav generation was obtained from this article (https://medium.com/@noahhradek/sound-synthesis-in-python-4e60614010da)--see the "playTone" function for the code i harvested.
Thank you to all of my table groupmates enduring my vocal stims whilst they try to comeplete their work


# TL;DR #

Use the note editor to edit and create cells
Organize those cells in the timeline
You can press space to hear your music (it loops)


# CODE GRAVEYARD #

# create time values
# t = np.linspace(0, length, length * AUDIO_RATE, dtype=np.float32)
# generate y values for signal
# y = np.sin(2 * np.pi * freq * t)
# print(y)
# q = np.sin(2 * np.pi * freq2 * t)

# result = np.append(y,q)

# save to wave file
# write("sine.wav", AUDIO_RATE, result)

# sig = Sine(440, length=2)
# sig.to_wav("sine.wav")


# initializing pygame and setup
# pygame.init()
# pygame.mixer.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.flip()

# # index of the note in the group
# note_y_index = round(mouse_y / NOTE_HEIGHT)

# if note_x_index == 0:
# 	self.groupOneY[note_x_index] = note_y_index * NOTE_HEIGHT
# elif note_x_index <= 32:
# 	self.groupOneY[note_x_index-1] = note_y_index * NOTE_HEIGHT

# sineOne.playMelody()
# melody = pygame.mixer.Sound('sine.ogg')
# melody.play()

# mouseButtons = pygame.mouse.get_pressed()

### TROUBLE SHOOTING ###
# issue: index is supposedly out of range
# from these print statements it makes no sense as to why it would be out of range
# print(i)
# print(len(self.channels[self.channelNum][self.barNum][0]))
# print(range(len(self.channels[self.channelNum][self.barNum][0])))
# print(self.channels[self.channelNum][self.barNum][0])
########################