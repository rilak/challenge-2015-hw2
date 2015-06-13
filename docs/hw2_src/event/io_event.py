import pygame
from consts import *
from event.game_event import EventEndGame
from event.base_event import *
from pygame.locals import *

move_keys = {
    pygame.locals.K_LEFT : ( -1 , 0 ),
    pygame.locals.K_RIGHT : ( 1 , 0 ),
    pygame.locals.K_UP : ( 0 , -1 ),
    pygame.locals.K_DOWN : ( 0 , 1 ),
}

class EventIOEvent( BaseEvent ):
    def __init__( self , env , priority ):
        self.env      = env
        self.priority = priority

    def do_action( self ):
        for e in pygame.event.get():
            if e.type == pygame.locals.QUIT:
                self.env[ "pyQUIT" ] = True
                self.env[ "gamec" ].add_event( EventEndGame( self.env , self.priority + TICKS_PER_TURN ) )
            # TODO
            '''
            Check what key does player press then change the state of the game
            '''
            if e.type != pygame.locals.KEYDOWN:
                continue
            if e.key in move_keys:
                new_direction = move_keys[e.key]
                if new_direction != self.env["dir"]:
                    self.env["dir"] = new_direction

        self.env[ "uic" ].add_event( EventIOEvent( self.env , self.priority + TICKS_PER_TURN ) )

