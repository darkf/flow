from flow import Entity, Component, system
from engine import PygameGame

game = None # global because of laziness

SquareComponent = Component(size=30)

@system([SquareComponent])
def squareRenderSystem(entity):
	print "square:", entity
	# todo: render square

def main():
	global game
	game = PygameGame()
	squareEntity = Entity(SquareComponent)
	game.scene('main', [
		# entities
		squareEntity
	]).addSystem(squareRenderSystem)
	game.run()

if __name__ == '__main__':
	main()