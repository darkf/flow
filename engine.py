from flow import Game

class PygameGame(Game):
	def __init__(self):
		super(PygameGame, self).__init__()
		print "pygame __init__"