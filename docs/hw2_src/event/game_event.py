
import random
import pygame
from consts import *
from event.base_event import *
from event.io_event import *
from event.ui_event import *


def abs( x ):
    if x < 0:
        return -x
    return x

class EventCheckSnake( BaseEvent ):
    def __init__( self , env , priority ):
        self.env      = env
        self.priority = priority
        self.snake = self.env[ "snake" ]
        self.foods = self.env[ "foods" ]

    def check_is_dead( self ):
        for ( i , ( px , py ) ) in enumerate( self.snake ):
            if not ( 0 <= px <= 925 and 0 <= py <= 540 ):
                print( "DEAD : out of boarder" )
                return True
            for ( j , ( tx , ty ) ) in enumerate( self.snake ):
                if i == j:
                    continue
                if abs( px - tx ) < 2 and abs( py - ty ) < 2:
                    print( "DEAD : bump into self" )
                    print( str( ( px , py ) ) + " " + str( i ) )
                    print( str( ( tx , ty ) ) + " " + str( j ) )
                    return True
        return False

    def do_add_head( self ):
        ( dx , dy ) = self.env[ "dir" ]
        ( hx , hy ) = self.snake[ 0 ]
        for i in range( 1 , 11 ):
            self.snake.insert( 0 , ( hx + i * dx * 2 , hy + i * dy * 2 ) )

    def do_eat_foods( self ):
        ( dx , dy ) = self.env[ 'dir' ]
        ( hx , hy ) = self.snake[ 0 ]
        for ( tx , ty ) in self.foods:
            if abs( hx - tx ) <= 20 and abs( hy - ty ) <= 20:
                print( "EAT " + str( ( tx , ty ) ) )
                self.foods.remove( ( tx , ty ) )
                self.do_add_head()
                ( hx , hy ) = self.snake[ 0 ]


    def do_move( self ):
        ( dx , dy ) = self.env[ "dir" ]
        ( hx , hy ) = self.snake[ 0 ]
        self.snake.insert( 0 , ( hx + dx * 2 , hy + dy * 2 ) )
        self.snake.pop()

    def do_action( self ):
        if self.check_is_dead():
            self.env[ "pyQUIT" ] = True
            self.env[ "gamec" ].add_event( EventEndGame( self.env , self.priority + TICKS_PER_TURN ) )
            return

        self.do_eat_foods()
        self.do_move()

        self.env[ "gamec" ].add_event( EventCheckSnake( self.env , self.priority + TICKS_PER_TURN ) )

class EventAddFood( BaseEvent ):
    def __init__( self , env , priority ):
        self.env      = env
        self.priority = priority
        self.foods    = self.env[ "foods" ]
        self.snake    = self.env[ "snake" ]

    def check_collision( self , p ):
        ( x , y ) = p
        for ( tx , ty ) in self.foods:
            if abs( tx - x ) < 40 or abs( ty - y ) < 40:
                return False
        for ( tx , ty ) in self.snake:
            if abs( tx - x ) < 40 or abs( ty - y ) < 40:
                return False
        return True

    def do_action( self ):

        if len( self.foods ) > 40:
            self.env[ "gamec" ].add_event( EventAddFood( self.env , self.priority + FOOD_ADD_TIME ) )


        p = ( random.randrange( 925 - 20 ) , random.randrange( 540 - 20 ) )

        while self.check_collision( p ):
            p = ( random.randrange( 925 - 20 ) , random.randrange( 540 - 20 ) )

        self.foods.append( p )

        self.env[ "gamec" ].add_event( EventAddFood( self.env , self.priority + FOOD_ADD_TIME ) )

class EventStartGame( BaseEvent ):
    def __init__( self , env , random_seed , priority ):
        self.env = env
        self.random_seed = random_seed
        self.priority = priority

    def do_action( self ):
        random.seed( self.random_seed )
        self.env[ "pyQUIT" ] = False
        # TODO
        '''
        Init some data in env[] when the game starts, and add some events to the controllers
        '''

class EventEndGame( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority

    def do_action( self ):
        self.env[ "uic" ].stop()
        self.env[ "gamec" ].stop()