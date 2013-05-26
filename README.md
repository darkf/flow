**Flow** - a dynamic Entity-Component-System engine for Python

Overview
---------

**Components** are just grab-bags of data. They're similar to the concept **models** you might be familiar with in other systems like MVC.

    PositionComponent = Component(x=0, y=0)
    VelocityComponent = Component(vx=0, vy=0)
    SquareComponent = Component(size=30)
    
Here we define two components, just being containers for their attributes (a set of `x` and `y` positions, a `vx` and `vy` vector for velocity, and a `size` for defining a square.)

**Entities** are likewise just grab-bags of *components* - they also handle getting and setting attributes on components.

    spaceship = Entity(PositionComponent, VelocityComponent(vx=1, vy=1), SquareComponent)
    
Now we have a `spaceship` that has a position, a velocity (heading to the bottom-right), and is a square. But it's all just data! We could print that data out:

    >>> print(spaceship.size)
    30
    
But what good is that if we can't do anything?

**Systems** are functions that accept an entity (possibly filtered by required components) as input and performs an operation on it. They're called every update tick, so they're useful for defining game and rendering logic.

    # update every entity with a position and a velocity
    @system(PositionComponent, VelocityComponent)
    def physicsSystem(entity):
        entity.x += entity.vx
        entity.y += entity.vy
    
And we might want to render all squares with positions:

    @system(PositionComponent, SquareComponent)
    def squareRenderSystem(entity):
        drawRectangle(entity.x, entity.y, entity.size, entity.size)
        
Implementation
--------------

We provide an engine that uses [pygame](http://pygame.org) to power the graphics and timing. Using it is simple:

    from flow import Entity, Component, system
    from engine import PygameGame
    
    # ...
    
    if __name__ == '__main__':
        game = PygameGame(800, 600) # 800x600 window
        game.scene('main', [
            # systems
            physicsSystem, squareRenderSystem,
            # entities
            spaceship
        ])
        game.run()
        
And you're done.