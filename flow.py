class Component(object):
	def __init__(self):
		pass

class Entity(object):
	def __init__(self, *components):
		self.components = components

class Scene(object):
	def __init__(self):
		self.entities = []

class Game(object):
	def __init__(self):
		self.scenes = {}
		self.currentScene = None

def system(fn):
	"`system` decorator"
	return fn