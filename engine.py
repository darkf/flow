from flow import Game
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

class PygameGame(Game):
	def __init__(self, screenWidth=640, screenHeight=480, fps=30, caption="Flow"):
		super(PygameGame, self).__init__()
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.fps = fps
		self.caption = caption

	def run(self):
		"Pygame mainloop implementation"

		# initialize pygame, the clock and the display
		pygame.init()
		self.fpsClock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.caption)
		if not self.screen:
			raise Exception("Couldn't initialize pygame display")

		continueRunning = True
		while continueRunning:
			# TODO: event handling
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					continueRunning = False

			self.update() # do game logic
			pygame.display.update() # flip display
			self.fpsClock.tick(self.fps)
		# de-initialize pygame
		pygame.quit()