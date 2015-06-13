import pygame
from consts import *
from event.base_event import *

class SnakePart( pygame.sprite.Sprite ):
    def __init__( self , position , m ):
        pygame.sprite.Sprite.__init__( self )
        self.image = m
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Food( pygame.sprite.Sprite ):
    def __init__( self , position , m ):
        pygame.sprite.Sprite.__init__( self )
        self.image = m
        self.rect = self.image.get_rect()
        self.rect.topleft = position

snake_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

class EventDrawInit( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority

    def do_action( self ):
        self.env[ "uic" ].add_event( EventDrawGround( self.env , self.priority + TICKS_PER_TURN ) )

class EventDrawGround( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority

    def do_action( self ):
        # TODO
        '''
        What this event do is to arrange objects on the surface
        '''
        snake_image = pygame.image.load("snake_part.png")
        food_image = pygame.image.load("food.png")
        snake_group.empty()
        food_group.empty()

        for x, y in self.env["snake"]:
            snake_group.add(SnakePart([x, y], IMG_SNAKE_PART))

        for x, y in self.env["foods"]:
            food_group.add(SnakePart([x, y], IMG_FOOD))     

        self.env[ "uic" ].add_event( EventDrawGround( self.env , self.priority + TICKS_PER_TURN ) )


class EventClearInit( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority
        self.env[ "screen" ].blit( IMG_BG , ( 0 , 0 ) )

    def do_action( self ):
        self.env[ "uic" ].add_event( EventDrawClear( self.env , self.priority + TICKS_PER_TURN ) )

class EventDrawClear( BaseEvent ):
    def __init__( self , env , priority ):
        self.env      = env
        self.priority = priority
        self.surf     = env[ "screen" ]

    def do_action( self  ):
        # TODO
        '''
        What this event do is to draw objects on to the surface
        '''
        self.env[ "screen" ].blit( IMG_BG , ( 0 , 0 ) )
        snake_group.draw(self.env[ "screen" ])
        food_group.draw(self.env[ "screen" ])
        pygame.display.flip()
        self.env[ "uic" ].add_event( EventDrawClear( self.env , self.priority + TICKS_PER_TURN ) )
