# the code for the sine wav generation was obtained from this article
# https://medium.com/@noahhradek/sound-synthesis-in-python-4e60614010da
# see the "playTone" function for the code i harvested

# imports
import numpy as np
from scipy.io.wavfile import write
import pygame
import os
import sys

# variables
WIDTH = 800
HEIGHT = 600

# audiorate
AUDIO_RATE = 44100

# colours :D
RED = (255,0,0)
BLUE = (0,0,255)
LIGHT_GREEN = (72, 217, 74)
DARK_GREEN = (44, 171, 46)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)

# the locations for the white keys 
WHITE_KEYS = [0,2,3,5,7,8,10,12,14,15,17,19,20,22,24,26,27,29]

# height and width of the placed nnotes
NOTE_WIDTH = 22
NOTE_HEIGHT = 20

# empty bar list generic thing for adding new bars
groupOneX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
groupOneY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


# classes
# omg look it's a class for the sine waves wowie
class SineWave:
	def __init__(self):
		# list of all required pitches
		# technically this could be represented with a log but i do not understand that
		self.pitches = [783.99,739.99,698.46,659.25,622.25,587.33,554.37,523.25,
						493.88,466.16,440.00,415.30,392.00,369.99,349.23,329.63,311.13,293.66,277.18,261.63,
						246.94,233.08,220.00,207.65,196.00,185.00,174.61,164.81,155.56,146.83]

	# makes a special variable thing with values corresponding to a sine wave
	def playTone(self, freq, length):
		# gets the time (x value) of the sine wave
		t = np.linspace(0, length, int(length * AUDIO_RATE), dtype=np.float32)
		# gets the y value to the corresponding time value (x value) of the sine wave
		tone = 0.25 * np.sin(2 * np.pi * freq * t)
		return tone

	# organizes the different values of the sine waves into a list
	def developMelody(self, channelNum, barNum):
		freqList = []

		# loping through all the possible states of notes for that bar and channel number
		for i in range(len(newSong.channels[channelNum][barNum][0])):

			# if no note
			if newSong.channels[channelNum][barNum][0][i] == False:
				# add an empty pitch
				freqList.append(0)

			# if note
			elif newSong.channels[channelNum][barNum][0][i] == True:
				# add a pitch according to the note location
				freqList.append(self.pitches[newSong.channels[channelNum][barNum][1][i]])

		return freqList

	# turns the sine wave values into a .ogg file
	def playMelody(self):
		freqList = self.developMelody(newSong.channelNum,newSong.barNum)

		# runs for every note in the list
		for i in range(len(freqList)):

			if i == 0:
				# creates an array with the first pitch
				result = self.playTone(freqList[i], 0.125)
			else:
				# adds a pitch to the array
				result = np.append(result, self.playTone(freqList[i], 0.125))

		# makes an ogg file from the array
		write("sine.ogg", AUDIO_RATE, result)

	# same thing as developMelody except for multiple channels and organizes it based on the order of specified bars
	def developTimeLineMelody(self, channelNum):
		freqList = []

		# for each of the 10 cells
		for i in range(10):

			# for every note in a cell
			for playing in range(len(newSong.channels[channelNum][0][0])):

				# if the current channel's bar number from group bars has an x value in that spot of being False
				if newSong.channels[channelNum][newSong.barGroups[channelNum][i]][0][playing] == False:
					freqList.append(0)

				# if the current channel's bar number from group bars has an x value in that spot of being True
				elif newSong.channels[channelNum][newSong.barGroups[channelNum][i]][0][playing] == True:
					# append the corresponding pitch value
					freqList.append(self.pitches[newSong.channels[channelNum][newSong.barGroups[channelNum][i]][1][playing]])
					
		return freqList

	# same thing as playMelody except for multiple channels and based of the specified bar orders
	def playTimeLineMelody(self):
		# runs for every channel 
		for i in range(4):
			freqList = self.developTimeLineMelody(i)

			# runs for every note in the frequency list
			for j in range(len(freqList)):
				if j == 0:
					# create the special numpy array thingy and add tone
					result = self.playTone(freqList[j], 0.125)
				else:
					# append to that numpy array thingy
					result = np.append(result, self.playTone(freqList[j], 0.125))

			# makes a .ogg file corresponding to each channel
			write("sine" + str(i) + ".ogg", AUDIO_RATE, result)

# omg look it's a class for the song wowie
class Song:
	def __init__(self):
		# pygame init moment
		pygame.init()
		# pygame mixer init moment
		pygame.mixer.init()
		# 1 channel per each wave
		pygame.mixer.Channel(0).set_volume(1)
		pygame.mixer.Channel(1).set_volume(1)
		pygame.mixer.Channel(2).set_volume(1)
		pygame.mixer.Channel(3).set_volume(1)

		# setting up the game screen
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('GB Studio')

		# channels and stuff (making it easier to understand)
		self.SQR1 = [
			[groupOneX.copy(),groupOneY.copy()]
		]
		self.SQR2 = [
			[groupOneX.copy(),groupOneY.copy()]
		]
		self.TRI = [
			[groupOneX.copy(),groupOneY.copy()]
		]
		self.RND = [
			[groupOneX.copy(),groupOneY.copy()]
		]
		self.channels = [self.SQR1,self.SQR2,self.TRI,self.RND]

		# the current state of the thing playing 
		self.playingState = False
		# MAIN = Main screen, EDIT = editing screen, TILI = time line
		self.screenState = "MAIN"
		# loading font
		self.font = pygame.font.SysFont("dejavusansmono", 30)
		self.channelNum = 0
		self.barNum = 0
		# self.barGroups[channelNumber][cellNumber]
		self.barGroups = [
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0]]
		self.barGroupsCellIndex = 0
		self.barGroupsChannelNum = 0
		self.mainMenuHelp = False
		self.noteEditorHelp = False
		self.timeLineHelp = False

	# main menu of the system (where it loads to on startup)
	def mainMenu(self):

		# text display
		text = self.font.render("Main Menu", True, BLACK)
		textRect = text.get_rect(center=(WIDTH//2, (HEIGHT//2)-60))
		self.screen.blit(text, textRect)

		text = self.font.render("Press E for Editing Menu", True, BLACK)
		textRect = text.get_rect(center=(WIDTH//2, (HEIGHT//2)-30))
		self.screen.blit(text, textRect)

		text = self.font.render("Press and hold H for a help screen", True, BLACK)
		textRect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
		self.screen.blit(text, textRect)

		text = self.font.render("Press M for the Main Menu", True, BLACK)
		textRect = text.get_rect(center=(WIDTH//2, (HEIGHT//2)+30))
		self.screen.blit(text, textRect)

		text = self.font.render("Press T for Timeline View", True, BLACK)
		textRect = text.get_rect(center=(WIDTH//2, (HEIGHT//2)+60))
		self.screen.blit(text, textRect)

		# drawing main menu help 
		if self.mainMenuHelp == True:
			self.drawMainMenuHelp()

	# the note editor of the system
	def noteEditor(self):
		# drawing the black keys of the piano
		pygame.draw.rect(self.screen, BLACK, (0,0,20,HEIGHT))
		# drawing the timeline lines for vertical plane
		for i in range(32):
			if i % 4 == 0:
				pygame.draw.line(self.screen, BLACK, (i*NOTE_WIDTH + 20,0),(i*NOTE_WIDTH + 20,HEIGHT))
			else:
				pygame.draw.line(self.screen, GREY, (i*NOTE_WIDTH + 20,0),(i*NOTE_WIDTH + 20,HEIGHT))

		# drawing the timeline lines for horizontal plane and the white keys
		for i in range(30):

			# drawing black box for black keys
			pygame.draw.line(self.screen, BLACK, (0,i*NOTE_HEIGHT),(WIDTH,i*NOTE_HEIGHT))

			# drawing white boxes for white keys
			if i in WHITE_KEYS:
				pygame.draw.rect(self.screen, WHITE, (0,20 * i,20,20))

		# drawing notes to the screen if any are present
		# for every note in the current bar group of that channel
		for i in range(len(self.channels[self.channelNum][self.barNum][0])):

			# if there is a note found there, draw it
			if self.channels[self.channelNum][self.barNum][0][i] == 1:
				pygame.draw.rect(self.screen, DARK_GREEN, (i * NOTE_WIDTH + 20,self.channels[self.channelNum][self.barNum][1][i]* NOTE_HEIGHT,NOTE_WIDTH,NOTE_HEIGHT))
		
		# drawing black sidebar on the right of the note editor
		pygame.draw.rect(self.screen, BLACK, (WIDTH-75,0,WIDTH,HEIGHT))

		# displaying bar number
		text = self.font.render("Bar#", True, WHITE)
		textRect = text.get_rect(center=(WIDTH - 38, HEIGHT//32))
		self.screen.blit(text, textRect)

		text = self.font.render(str(self.barNum + 1), True, WHITE)
		textRect = text.get_rect(center=(WIDTH - 38, ((HEIGHT//32) * 2) + 5))
		self.screen.blit(text, textRect)

		# displaying channel number
		text = self.font.render("CHNL", True, WHITE)
		textRect = text.get_rect(center=(WIDTH - 38, (HEIGHT//32) * 5))
		self.screen.blit(text, textRect)

		text = self.font.render(str(self.channelNum + 1), True, WHITE)
		textRect = text.get_rect(center=(WIDTH - 38, ((HEIGHT//32) * 6) + 5))
		self.screen.blit(text, textRect)

		# displaying help menu for the note editor 
		if self.noteEditorHelp == True:
			self.drawNoteEditorHelp()

	# the timeline menu of the system
	def timeLine(self):
		# 4 channels at the side
		# drawing black sidebar on the right of the note editor
		pygame.draw.rect(self.screen, BLACK, (0,0,75,HEIGHT))

		# displaying channel
		text = self.font.render("SQR1", True, WHITE)
		self.screen.blit(text, (0, (HEIGHT//4) - 150))
		# displaying channel
		text = self.font.render("SQR2", True, WHITE)
		self.screen.blit(text, (0, ((HEIGHT//4) * 2) - 150))
		# displaying channel
		text = self.font.render("TRI", True, WHITE)
		self.screen.blit(text, (0, ((HEIGHT//4) * 3)- 150))
		# displaying channel
		text = self.font.render("RND", True, WHITE)
		self.screen.blit(text, (0, ((HEIGHT//4) * 4)- 150))

		# when you press play it plays all of the channels
		# the bar numbers will be the specified ones
		for i in range(len(self.barGroups)):

			# drawing the correct number of bars
			for j in range(len(self.barGroups[i])):

				# highlight the box the user is currently on
				if i == self.barGroupsChannelNum and j == self.barGroupsCellIndex:
					pygame.draw.rect(self.screen, WHITE, ((j * 72) + 75,(i * 144),62,62))
					text = self.font.render(str(self.barGroups[i][j]+1), True, BLACK)
					textRect = text.get_rect(center=((j * 72) + 75 + 31, (i * 144) + 31))
					self.screen.blit(text, textRect)

				# normal colour for the other bars
				else:
					pygame.draw.rect(self.screen, DARK_GREEN, ((j * 72) + 75,(i * 144),62,62))
					text = self.font.render(str(self.barGroups[i][j]+1), True, WHITE)
					textRect = text.get_rect(center=((j * 72) + 75 + 31, (i * 144) + 31))
					self.screen.blit(text, textRect)

		# displaying the help menu if true
		if self.timeLineHelp == True:
			self.drawTimeLineHelp()

	# updating the screen
	def update(self):
		# background colour
		self.screen.fill(LIGHT_GREEN)
		# updating for correct screen
		if self.screenState == "MAIN":
			newSong.mainMenu()
		elif self.screenState == "EDIT":
			newSong.noteEditor()
		elif self.screenState == "TILI":
			newSong.timeLine()
		pygame.display.flip()

	# stoping all audio channels from playing
	def stoppingAudio(self):
		self.loadingScreen()
		self.melody = pygame.mixer.Sound('sine.ogg')
		self.melody0 = pygame.mixer.Sound('sine0.ogg')
		self.melody1 = pygame.mixer.Sound('sine0.ogg')
		self.melody2 = pygame.mixer.Sound('sine0.ogg')
		self.melody3 = pygame.mixer.Sound('sine0.ogg')
		self.melody.stop()
		for i in range(4):
			pygame.mixer.Channel(i).stop()
		self.playingState = False

	# displaying a loading message whenever the application must load
	def loadingScreen(self):
		text = self.font.render("Loading... Please Wait!", True, WHITE)
		textRect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
		pygame.draw.rect(self.screen, BLACK, textRect)
		self.screen.blit(text, textRect)
		pygame.display.flip()

	# different menu's help texts
	def drawMainMenuHelp(self):
		self.writeTextLine("Keyboard & Mouse Help Menu:|E - Go to note editor|H - Show help menu|M - Go to main menu|T - Go to timeline|")

	def drawNoteEditorHelp(self):
		self.writeTextLine("Keyboard & Mouse Help Menu:|E - Go to note editor|H - Show help menu|M - Go to main menu|T - Go to timeline|Left arrow key - Move to/create new bar|Right arrow key - Go back to previous bar|Space bar - Play and loop bar|1 to 4 - Change channel|")

	def drawTimeLineHelp(self):
		self.writeTextLine("Keyboard & Mouse Help Menu:|E - Go to note editor|H - Show help menu|M - Go to main menu|T - Go to timeline|Left arrow key - Move left on cell|Right arrow key - Move right on cell|Up arrow key - raise cell number|Down arrow key- lower cell number|Space bar - Play and loop song|1 to 4 - Change channel|")

	# displaying text at bottom of screen function (used for help menu text)
	def writeTextLine(self, inputText):
		# create an empty list and int variable
		textList = [""]
		indentCount = 0
		# looping through every character in the inputted text
		for i in inputText:
			if i == '|':
				# line break and start a new item in the list
				indentCount += 1
				textList.append("")
			else:
				# add character to that item
				textList[indentCount] = str(textList[indentCount] + i)

		# remove the last empty item
		textList.pop(indentCount)

		# display the text on screen
		for i in range(indentCount):
			text = self.font.render(textList[i], True, WHITE)
			textRect = text.get_rect(center=(WIDTH//2, HEIGHT - 30 * (indentCount - i)))
			pygame.draw.rect(self.screen, BLACK, textRect)
			self.screen.blit(text, textRect)

	# holding all of the possible events
	def events(self):
		# reset help menu variable
		self.mainMenuHelp = False
		self.noteEditorHelp = False
		self.timeLineHelp = False

		# getting mouse positions
		mouse_x, mouse_y = pygame.mouse.get_pos()

		# a bit of correction for the mouse position so placing notes feels better
		mouse_x -= 5
		mouse_y -= 5

		# checking for the help menu button for the screen
		keys = pygame.key.get_pressed()
		if self.screenState == "MAIN":
			if keys[pygame.K_h]:
				self.mainMenuHelp = True
		if self.screenState == "EDIT":
			if keys[pygame.K_h]:
				self.noteEditorHelp = True
		if self.screenState == "TILI":
			if keys[pygame.K_h]:
				self.timeLineHelp = True

		# event for loop
		for event in pygame.event.get():

			# exiting the game
			if event.type == pygame.QUIT:
				pygame.quit()
				running = False
				sys.exit()

			# key pressing events
			if event.type == pygame.KEYDOWN:
				# go to main menu
				if event.key == pygame.K_m:
					self.barNum = 0
					self.screenState = "MAIN"
					self.stoppingAudio()
				# go to note editor
				elif event.key == pygame.K_e:
					self.barNum = 0
					self.channelNum = 0
					self.stoppingAudio()
					self.screenState = "EDIT"
				# go to timeline
				elif event.key == pygame.K_t:
					self.barNum = 0
					self.channelNum = 0
					self.stoppingAudio()
					self.screenState = "TILI"

			# timeline screen
			if self.screenState == "TILI":

				# timeline editor screen moving
				if event.type == pygame.KEYDOWN:

					# moving to different cells horizontally
					if event.key == pygame.K_RIGHT:
						if self.barGroupsCellIndex < 9:
							self.barGroupsCellIndex += 1
					if event.key == pygame.K_LEFT:
						if self.barGroupsCellIndex > 0:
							self.barGroupsCellIndex -= 1

					# changing the cell's number
					if event.key == pygame.K_UP:
						if self.barGroups[self.barGroupsChannelNum][self.barGroupsCellIndex] < len(self.channels[self.channelNum])-1:
							self.barGroups[self.barGroupsChannelNum][self.barGroupsCellIndex] += 1
					if event.key == pygame.K_DOWN:
						if self.barGroups[self.barGroupsChannelNum][self.barGroupsCellIndex] > 0:
							self.barGroups[self.barGroupsChannelNum][self.barGroupsCellIndex] -= 1

					# change channel
					if event.key == pygame.K_1:
						self.barGroupsChannelNum = 0
						self.channelNum = 0
					if event.key == pygame.K_2:
						self.barGroupsChannelNum = 1
						self.channelNum = 1
					if event.key == pygame.K_3:
						self.barGroupsChannelNum = 2
						self.channelNum = 2
					if event.key == pygame.K_4:
						self.barGroupsChannelNum = 3
						self.channelNum = 3

					# playing/stopping the timeline
					if event.key == pygame.K_SPACE:
						if self.playingState == False:
							self.loadingScreen()
							sineOne.playTimeLineMelody()

							# loading all of the melodies into the mixer
							self.melody0 = pygame.mixer.Sound('sine0.ogg')
							self.melody1 = pygame.mixer.Sound('sine1.ogg')
							self.melody2 = pygame.mixer.Sound('sine2.ogg')
							self.melody3 = pygame.mixer.Sound('sine3.ogg')

							# loading all of the sounds into a channel
							pygame.mixer.Channel(0).play(self.melody0, -1)
							pygame.mixer.Channel(1).play(self.melody1, -1)
							pygame.mixer.Channel(2).play(self.melody2, -1)
							pygame.mixer.Channel(3).play(self.melody3, -1)

							self.playingState = True

						# stopping the sound from playing
						elif self.playingState == True:
							self.stoppingAudio()
							self.playingState = False

			# if on the editing screen
			if self.screenState == "EDIT":

				# mouse sensing
				if event.type == pygame.MOUSEBUTTONDOWN:
					# adding/removing note when left mouse clicked
					if event.button == 1:
						# index of the note in the group
						note_x_index = round(mouse_x / NOTE_WIDTH)
						note_y_index = round(mouse_y / NOTE_HEIGHT)
						# making sure the specifide placement is within the measures
						if note_x_index == 0:
							# no minus one so it does not turn and become 32 
							self.channels[self.channelNum][self.barNum][0][note_x_index] = not self.channels[self.channelNum][self.barNum][0][note_x_index]
							self.channels[self.channelNum][self.barNum][1][note_x_index] = note_y_index
						elif note_x_index <= 32:
							# minus 1 to keep index in range
							self.channels[self.channelNum][self.barNum][0][note_x_index-1] = not self.channels[self.channelNum][self.barNum][0][note_x_index-1]
							self.channels[self.channelNum][self.barNum][1][note_x_index-1] = note_y_index

				# keydown but for note editor
				if event.type == pygame.KEYDOWN:
					# play melody haha
					if event.key == pygame.K_SPACE:
						# generating and playing the sound
						if self.playingState == False:
							sineOne.playMelody()
							self.melody = pygame.mixer.Sound('sine.ogg')
							self.melody.play(-1)
							self.playingState = True
						# stopping the sound
						elif self.playingState == True:
							self.melody.stop()
							self.playingState = False

					# moving to another bar group
					if event.key == pygame.K_RIGHT:
						self.barNum += 1
						# if that bar group does not exist, make it exist (make a new empty bar group)
						if self.barNum > (len(self.channels[self.channelNum])-1):
							self.channels[self.channelNum].append([groupOneX.copy(),groupOneY.copy()])

					# going back to previous bar groups
					if event.key == pygame.K_LEFT:
						if self.barNum > 0:
							self.barNum -= 1

					# change channel
					if event.key == pygame.K_1:
						self.channelNum = 0
						self.barNum = 0
					if event.key == pygame.K_2:
						self.channelNum = 1
						self.barNum = 0
					if event.key == pygame.K_3:
						self.channelNum = 2
						self.barNum = 0
					if event.key == pygame.K_4:
						self.channelNum = 3
						self.barNum = 0

# calling song and sinewave classes
newSong = Song()
sineOne = SineWave()
# main game loop
running = True
while running:
	newSong.update()
	newSong.events()