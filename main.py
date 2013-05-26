from flow import Entity, Component, system
from engine import PygameGame
import pygame

game = None # global because of laziness

PositionComponent = Component(x=0, y=0)
VelocityComponent = Component(vx=0, vy=0)
SquareComponent = Component(size=30)
ColorComponent = Component(r=0, g=0, b=0)

@system([PositionComponent, VelocityComponent])
def physicsSystem(entity):
	entity.x += entity.vx
	entity.y += entity.vy

@system([PositionComponent, SquareComponent])
def squareRenderSystem(entity):
	color = (0, 0, 0) if not entity.has(ColorComponent) else (entity.r, entity.g, entity.b)
	pygame.draw.rect(game.screen, color, pygame.Rect(entity.x, entity.y, entity.size, entity.size))

def main():
	global game
	game = PygameGame()
	squareEntity = Entity(SquareComponent, PositionComponent, VelocityComponent(vx=1, vy=1), ColorComponent(r=255, g=0, b=0))
	game.scene('main', [
		# entities
		squareEntity
	]).addSystem(physicsSystem).addSystem(squareRenderSystem)
	game.run()

if __name__ == '__main__':
	main()