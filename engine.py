""" Part of the Flow engine.
	Licensed under the terms of the ISC license:

	Copyright (c) 2013 darkf

	Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted,
	provided that the above copyright notice and this permission notice appear in all copies.

	THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
	IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
	WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from flow import Game
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEMOTION

class PygameGame(Game):
	def __init__(self, screenWidth=640, screenHeight=480, fps=30, backgroundColor=(255,255,255), caption="Flow"):
		super(PygameGame, self).__init__()
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.fps = fps
		self.backgroundColor = backgroundColor
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
			self.screen.fill(self.backgroundColor) # clear screen
			# TODO: event handling
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					continueRunning = False
					self.emit("shutdown")
				elif event.type == MOUSEMOTION:
					self.post("mouseMove", event.pos[0], event.pos[1])

			self.update() # do game logic
			pygame.display.update() # flip display
			self.fpsClock.tick(self.fps)
		# de-initialize pygame
		pygame.quit()