import pygame
from consts import *
from event.base_event import *

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
            if e.type == pygame.locals.KEYUP:
                if e.key not in move_keys:
                    continue
                self.env[ "dir" ] = move_keys[ e.key ]
                print( str( self.env[ "dir" ] ) )
            elif e.type == pygame.locals.QUIT:
                self.env[ "pyQUIT" ] = True
                self.env[ "gamec" ].add_event( EventEndGame( self.env , self.priority + TICKS_PER_TURN ) )

        self.env[ "uic" ].add_event( EventIOEvent( self.env , self.priority + TICKS_PER_TURN ) )

