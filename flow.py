""" The heart of the Flow engine.
	Licensed under the terms of the ISC license:

	Copyright (c) 2013 darkf

	Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted,
	provided that the above copyright notice and this permission notice appear in all copies.

	THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
	IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
	WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from copy import copy

class Component(object):
	def __init__(self, **attributes):
		# we're acting somewhat like a named tuple here for now
		self.parent = None
		self.attributes = attributes
		for k,v in attributes.iteritems():
			setattr(self, k, v)

	def __call__(self, **attributes):
		# instantiate (copy) a component with arguments
		new = copy(self)
		new.parent = self
		for k,v in attributes.iteritems():
			if k not in self.attributes:
				raise AttributeError("Attribute '%s' doesn't exist on %r" % (k, self))
			new.attributes[k] = v
			setattr(new, k, v)
		return new

	def __repr__(self):
		return "<Component with: %s>" % ', '.join(self.attributes.iterkeys())

	def isInstanceOf(self, component):
		"Are we an instance of this component?"
		if self.parent and self.parent.isInstanceOf(component):
			return True
		return self.parent == component

class Entity(object):
	def __init__(self, *components):
		# instantiate (actually copy) components
		def newComponent(component):
			c = copy(component)
			c.parent = component
			return c
		self.components = [newComponent(c) for c in components]

	def __getattr__(self, attr):
		# XXX: ugly
		if attr == "components":
			return super(Entity, self).__getattribute__(attr)

		for component in self.components:
			if attr in component.attributes:
				return getattr(component, attr)
		raise AttributeError("Entity does not have the attribute '%s'" % attr)

	def __setattr__(self, attr, value):
		# XXX: ugly
		if attr == "components":
			return super(Entity, self).__setattr__(attr, value)

		for component in self.components:
			if attr in component.attributes:
				return setattr(component, attr, value)
		raise AttributeError("Entity does not have the attribute '%s'" % attr)

	def has(self, component):
		"Do we have a specific component?"
		return any(c.isInstanceOf(component) for c in self.components)

	def has_all(self, components):
		"Do we have *all* of these components?"
		return all(self.has(component) for component in components)

	def __repr__(self):
		return "<Entity with: %s>" % ', '.join(repr(c) for c in self.components)

class Scene(object):
	def __init__(self, name, elements):
		self.name = name
		self.entities = []
		self.systems = []

		for element in elements:
			self.add(element)

	def add(self, element):
		if isinstance(element, Entity):
			self.entities.append(element)
		elif isinstance(element, System):
			self.systems.append(element)
		else:
			raise ValueError("Not an entity or a system: %r" % element)
		return self

	def update(self):
		"Runs an update tick. Calls all systems."
		for system in self.systems:
			system.run(self)

class System(object):
	def __init__(self, filtered_components, fn):
		self.filtered_components = filtered_components
		self.fn = fn

	def run(self, scene):
		"Filters the entities of `scene` and runs the system on each entity matching the desired components."
		for entity in scene.entities:
			match = True # too late for this, add flags!
			for filterComponent in self.filtered_components:
				if not entity.has(filterComponent):
					match = False # one of the filters didn't match	
			if match:
				self.fn(entity)

class Game(object):
	def __init__(self):
		self.scenes = {}
		self.currentScene = None

	def scene(self, name, children):
		"Defines a scene."
		scene = Scene(name, children)
		if self.currentScene is None:
			# automatically transition to the first scene defined
			self.currentScene = scene
		self.scenes[name] = scene
		return scene

	def query(self, components, exclude=None):
		"Runs a query for entities with specific components. Able to exclude specific entities."
		if exclude is None:
			exclude = []
		elif type(exclude) != list:
			exclude = [exclude]

		for entity in self.currentScene.entities:
			if entity not in exclude and entity.has_all(components):
				yield entity

	def update(self):
		"Runs an update tick. Calls all systems."
		self.currentScene.update()

def system(*components):
	"The `system` decorator."
	return lambda fn: System(components, fn)
