""" Shapes demo for the Flow engine.
	Should display a red square approaching from the top-left, a green one from the top-right,
	and a yellow circle approaching from the middle down, almost converging.

	Copyright (c) 2013 darkf
	Licensed under the terms of the WTFPL <http://www.wtfpl.net> """

from flow import Entity, Component, system
from engine import PygameGame
import pygame

game = None # we use a global because we're lazy programmers

PositionComponent = Component(x=0, y=0)
VelocityComponent = Component(vx=0, vy=0)
SquareComponent = Component(size=30)
CircleComponent = Component(radius=20)
ColorComponent = Component(r=0, g=0, b=0)

@system(PositionComponent, VelocityComponent)
def physicsSystem(entity):
	entity.x += entity.vx
	entity.y += entity.vy

@system(PositionComponent, CircleComponent)
def circleRenderSystem(entity):
	pygame.draw.circle(game.screen, (255, 255, 0), (entity.x, entity.y), entity.radius)

@system(PositionComponent, SquareComponent)
def squareRenderSystem(entity):
	color = (0, 0, 0) if not entity.has(ColorComponent) else (entity.r, entity.g, entity.b)
	pygame.draw.rect(game.screen, color, pygame.Rect(entity.x, entity.y, entity.size, entity.size))

def main():
	global game
	game = PygameGame()
	game.scene('main', [
		# systems
		physicsSystem, squareRenderSystem, circleRenderSystem,

		# entities
		# red square from top-left
		Entity(SquareComponent, PositionComponent, VelocityComponent(vx=1, vy=1), ColorComponent(r=255, g=0, b=0)),
		# green square from top-right
		Entity(SquareComponent, PositionComponent(x=game.screenWidth - SquareComponent.size, y=0),
			   VelocityComponent(vx=-1, vy=1), ColorComponent(r=0, g=255, b=0)),
		# circle
		Entity(CircleComponent, PositionComponent(x=game.screenWidth / 2 - CircleComponent.radius), VelocityComponent(vy=1))
	])
	game.run()

if __name__ == '__main__':
	main()