from flow import Entity, Component, system
from engine import PygameGame

SquareComponent = Component(size=30)

@system([SquareComponent])
def squareRenderSystem(entity):
	print "square:", entity
	# todo: render square

def main():
	game = PygameGame()
	squareEntity = Entity(SquareComponent)
	game.scene('main', [
		# entities
		squareEntity
	]).addSystem(squareRenderSystem)
	game.update()

if __name__ == '__main__':
	main()