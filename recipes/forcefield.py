# forcefield.py  18/03/2015  D.J.Whale
#
# NOTE: Still a work in progress
# NOTE: Not yet tested
#
# Shows how to prevent the player from escaping from a region.
# It builds a forcefield around a region, teleporting the player back
# to the "last known good" location if they escape the forcefield
# via any means.
#
# This can be used both for "in" and "out" scenarios:
# "in"  - e.g. keeping a player inside jail
# "out" - e.g. keeping a player outside of a locked room
#
# There is also a door that can be opened and closed, this is really
# a hole in the forcefield, that if present, you can safely walk through it.
#
# Eventually we want to be able to have multiple rooms, and rooms to have
# multiple doors. But that is not easy to code until we change this to an
# object oriented implemntation - we will do that a little later. First it is
# important to get the logic working correctly.

import mcpi.minecraft as minecraft
import mcpi.block as block

mc  = minecraft.Minecraft.create()

# The coordinates of the forcefield
x1 = None
y1 = None
z1 = None
x2 = None
y2 = None
z2 = None

# Is the player kept inside/outside of the region
keep_inside = True

# The forcefield can be enabled/disabled
enabled = False

# The last known good position either inside/outside of the field
lastgood_x = None
lastgood_y = None
lastgood_z = None

# The coordinates of a rectangular doorway that can be enabled/disabled
door_x1 = None
door_y1 = None
door_z1 = None
door_x2 = None
door_y2 = None
door_z2 = None

# Is the door open or closed?
door_closed = True


def define(field_x1, field_y1, field_z1, field_x2, field_y2, field_z2, keepin=True):
    """Remember the bounding box of the forcefield"""
    global x1, y1, z1, x2, y2, z2, keep_inside
    
    x1          = field_x1
    y1          = field_y1
    z1          = field_Y1
    x2          = field_x2
    y2          = field_y2
    z2          = field_z2
    keep_inside = keepin


def defineDoor(x1, y1, z1, x2, y2, z2):
    global door_x1, door_y1, door_z1, door_x2, door_y2, door_z2
    door_closed = True
    door_x1 = x1
    door_y1 = y1
    door_z1 = z1
    door_x2 = x2
    door_y2 = y2
    door_z2 = z2


def keepin(in=True):
    """Keep player inside(True) or outside(False)"""
    global keep_inside
    keep_inside = in


def keepout(out=True)
    """Keep player outside(True) or ionside(False)"""
    global keep_inside
    keep_inside = not out


def enable(enable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = enable


def disable(disable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = not disable

    
def openDoor(open=True):
    """Open the door(if True)"""
    global door_closed
    door_closed = not open
        
    
def closeDoor(close=True):
    """Close the door(if True)"""
    global door_closed
    door_closed = close

# Sense proximity to the field as follows:
#   inside:   contained by field, at least 1 block away from it
#   touching: next to field or on the field, in any dimension
#   outside:  not contained by the field, at least 1 block away from it

# TODO touching-inside and touching-outside???
# TODO better to say checkField() and get two constants back?
#   OUTSIDE, INSIDE, TOUCHING-OUTSIDE, TOUCHING-INSIDE, ON
#   NORTH, EAST, SOUTH, WEST, ROOF, CEILING
# could then build these other functions from a single assessment if required
# Do we want DOOR_OUTSIDE, DOOR_INSIDE, DOOR_ON also (only if enabled??)
# or both if disabled and enabled, if you know you are at the door you could
# pop up a message even though it is closed.

def getProximity(px, py, pz):
    """Work out what type of proximity to the field we have"""
    pass
    # proximity type
    #   OUTSIDE
    #   INSIDE
    #   TOUCHING_OUTSIDE
    #   TOUCHING_INSIDE
    #   AT
    #   DOOR_OUTSIDE
    #   DOOR_INSIDE
    #   DOOR_AT

    # face type
    #   NORTH
    #   EAST
    #   SOUTH
    #   WEST
    #   FLOOR
    #   CEILING
    #   DOOR??? (multiple doors might be interesting later e.g. invisible mazes
    #   with multiple doors), although we could just return DOOR and return
    #   some extra data which is a door index number.
    


#TODO: see notes on getProximity()
def isInside(px, py, pz):
    """Is the player safely inside the force field?"""
    if  px > x1 and px < x2 \
    and py > y1 and py < y2 \
    and pz > z1 and pz < z2:
        return True # inside
    return False # not inside (outside or touching-field)


#TODO: see notes on getProximity()
def isOutside(px, py, pz):
    """Is the player safely outside the force field?"""
    if px < x1 or px > x2 \
    or py < y1 or py > y2 \
    or pz < z1 or pz > z2:
        return True # outside
    return False # not outside (inside or touching-field)


#TODO: see notes on getProximity()
def isTouchingField(px, py, pz):
    """Is the player touching the force field?"""
    # Note, on the field, touching field outside, touching field inside?
    # might want to give a warning if touching, but buzz if on field
    
    # inside touching - check if any coordinates overlap with 6 walls
    # defined at the inner edge of the enclosure

    # outside touching - check if any coordinates overlap with 6 walls
    # defined at the outer edge of the enclosure
    pass # TODO


#TODO: see notes on getProximity()
def isOnField(px, py, pz):
    """Is the player touching the force field?"""
    # Note, on the field, touching field outside, touching field inside?
    # might want to give a warning if touching, but buzz if on field
    # check if any coordinates overlap with the 6 virtual walls of the
    # enclosure (remember the force field might be invisible and might be
    # overlayed on a real structure to save space)
    pass # TODO
    

#TODO: see notes on getProximity()
def isAtDoor(px, py, pz):
    """Work out if player is at the door region"""
    #If the door is open this will be useful to allow walking through door"""
    #at outside door face
    #at inside door face
    #at door threshold
    pass # TODO


def loop():
    """Run the forcefield checking loop"""
    global lastgood_x, lastgood_y, lastgood_z

    # TODO if the player walks through the door, need to allow them
    # to be the other side. But in a way that the forcefield is still
    # active in all the other regions.
    # i.e. really the forcefield should always work in both directions?
    
    pos = mc.player.getTilePos()

    #TODO: see notes on getProximity()
    if not door_closed and isAtDoor(pos.x, pos.y, pos.z):
        return # Don't buzz if walking through door
    
    #TODO: see notes on getProximity()
    if keep_inside and not isInside(pos.x, pos.y, pos.z) and not:
        buzz()
        
    #TODO: see notes on getProximity()
    elif not keep_inside and isInside(pos.x, pos.y, pos.z):
        buzz()
        
    #TODO: see notes on getProximity()
    elif isOnField(x, y, z):
        buzz()
        
    #TODO: see notes on getProximity()
    elif isTouchingField(x, y, z):
        warning()
        
    else: # must be ok, nothing specific to report
        lastgood_x = x
        lastgood_y = y
        lastgood_z = z

        
def warning():
    mc.postToChat("Getting a bit close to the force field!")

        
def buzz():
    """Put the player back to the last known good position"""
    if keep_inside:
        mc.postToChat("You can't escape!")
    else:
        mc.postToChat("You can't get inside!")
        
    mc.player.setTilePos(lastgood_x, lastgood_y, lastgood_z)


def hollow(x1, y1, z2, x2, y2, z2, b):
    """Build a hollow enclosure"""
    mc.setBlocks(x1, y1, z1, x2, y2, z2, b)
    mc.setBlocks(x1+1, y1+1, z1+1, x2-1, y2-1, z2-1, block.AIR.id)
    

def wrapper(x1, y1, z1, x2, y2, z2, b):
    """Build a wrapped enclosure without destroying insides"""
    # build floor
    mc.setBlocks(x1, y1, z1, x2, y1, z2, b)
    # build ceiling
    mc.setBlocks(x1, y2, z1, x2, y2, z2, b)
    
    # build north wall
    mc.setBlocks(x1, y1, z2, x2, y2, z2, b)
    # build south wall
    mc.setBlocks(x1, y1, z1, x2, y2, z1, b)

    # build east wall
    mc.setBlocks(x1, y1, z1, x1, y2, z2, b)
    # build west wall
    mc.setBlocks(x2, y1, z1, x2, y2, z2, b)    
    

def build(visible=True, hollow=False):
    """Build glass where the forcefield is"""
    if visible:
        b = block.GLASS_BLOCK.id
    else:
        b = block.AIR.id

    if hollow:
        # build a hollow enclosure, mainly for testing
        hollow(x1, y1, z1, x2, y2, z2, b)
    else:
        # Non hollow enclosures good for wrapping around existing buildings
        wrapper(x1, y1, z1, x2, y1, z2, b)        


def showDoor(visible=True):
    """Show or hide the door"""
    if visible:
        b = block.AIR.id
    else:
        b = block.GLASS_BLOCK.id
    mc.setBlocks(door_x1, door_y1, door_z1, door_x2, door_y2, door_z2, b)


# TEST HARNESS

def testin():
    """Test that the "keep in" forcefield works"""
    define(10,-1,10,30,30,30)
    defineDoor(15,0,15,20,0,20)
    build()
    showDoor()
    keepin()
    enable()
    
    mc.player.setTilePos(15, 0, 15) # inside
    mc.postToChat("Try to escape the jail")
    
    try:
        while True:
            time.sleep(0.1)
            loop()
            pos = mc.player.getTilePos()
            if not door_closed and isAtDoor(pos.x, pos.y, pos.z):
                mc.postToChat("Ooo, looks like a door!")
                
            if isOutside(pos.x, pos.y, pos.z):
                mc.postToChat("Did you find the door?")
    finally:
        build(false)


def testout():
    """Test that the "keep out" forcefield works"""
    define(10,-1,10,30,30,30)
    defineDoor(15,0,15,20,0,20)
    build()
    showDoor()
    keepout()
    enable()
    
    mc.player.setTilePos(0, 0, 0) # outside
    mc.postToChat("Try to get into the locked room")
    
    try:
        while True:
            time.sleep(0.1)
            loop()
            pos = mc.player.getTilePos()
            if not door_closed and isAtDoor(pos.x, pos.y, pos.z):
                mc.postToChat("Ooo, looks like a door!")
                
            if isInside(pos.x, pos.y, pos.z):
                mc.postToChat("Did you find the door?")            
    finally:
        build(false)


# Only run the test code if this file is the main program

if __name__ == "__main__":
    testin()
    #testout()

# END
