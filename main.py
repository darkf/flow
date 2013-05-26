from flow import Entity, Component, system
from engine import PygameGame
import pygame

game = None # global because of laziness

PositionComponent = Component(x=0, y=0)
VelocityComponent = Component(vx=0, vy=0)
SquareComponent = Component(size=30)

@system([PositionComponent, VelocityComponent])
def physicsSystem(entity):
	entity.x += entity.vx
	entity.y += entity.vy

@system([PositionComponent, SquareComponent])
def squareRenderSystem(entity):
	#print "square:", entity
	pygame.draw.rect(game.screen, (255, 0, 0), pygame.Rect(entity.x, entity.y, entity.size, entity.size))

def main():
	global game
	game = PygameGame()
	squareEntity = Entity(SquareComponent, PositionComponent, VelocityComponent(vx=1, vy=1))
	game.scene('main', [
		# entities
		squareEntity
	]).addSystem(physicsSystem).addSystem(squareRenderSystem)
	game.run()

if __name__ == '__main__':
	main()