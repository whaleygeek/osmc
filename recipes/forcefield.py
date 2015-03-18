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
#TODO FieldType.DISABLED, FieldType.KEEPIN, FieldType.KEEPOUT, FieldType.BOTHWAYS
keep_inside = True

# The forcefield can be enabled/disabled
enabled = False

# Proximity types
class Proximity:
    UNKNOWN            = 0
    INSIDE             = 1
    TOUCHING_INSIDE    = 2
    OUTSIDE            = 3
    TOUCHING_OUTSIDE   = 4
    IN_FIELD           = 5
    IN_DOORWAY         = 6
    OUTSIDE_AT_DOORWAY = 7
    INSIDE_AT_DOORWAY  = 8

# Face types
class Face:
    NONE    = 0
    NORTH   = 1
    SOUTH   = 2
    EAST    = 3
    WEST    = 4
    FLOOR   = 5
    CEILING = 6

# The last known good position either inside/outside of the field
lastgood_x = None
lastgood_y = None
lastgood_z = None

# The last known proximity value
# Useful for helping to detect which direction walking through doorway
lastprox   = Proximity.UNKNOWN

# The coordinates of a rectangular doorway that can be enabled/disabled
doorway_x1 = None
doorway_y1 = None
doorway_z1 = None
doorway_x2 = None
doorway_y2 = None
doorway_z2 = None

# Is the door open or closed?
doorway_closed = True


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


def defineDoorway(x1, y1, z1, x2, y2, z2):
    global doorway_x1, doorway_y, doorway_z1, doorway_x2, doorway_y2, doorway_z2
    global doorway_closed
    
    doorway_closed = True
    doorway_x1 = x1
    doorway_y1 = y1
    doorway_z1 = z1
    doorway_x2 = x2
    doorway_y2 = y2
    doorway_z2 = z2


#TODO setFieldDirection
def keepin(in=True):
    """Keep player inside(True) or outside(False)"""
    global keep_inside
    keep_inside = in


#TODO setFieldDirection
def keepout(out=True)
    """Keep player outside(True) or ionside(False)"""
    global keep_inside
    keep_inside = not out


#TODO setFieldDirection
def enable(enable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = enable


#TODO setFieldDirection
def disable(disable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = not disable


#TODO set swing directions of doorway?    
def openDoorway(open=True):
    """Open the door(if True)"""
    global doorway_closed
    doorway_closed = not open

        
#TODO set swing directions of doorway?    
def closeDoorway(close=True):
    """Close the door(if True)"""
    global doorway_closed
    door_closedway = close


def getProximity(px, py, pz):
    """Work out what type of proximity to the field we have"""

    #Proximity
    #   Proximity.UNKNOWN            
    #   Proximity.INSIDE             
    #   Proximity.TOUCHING_INSIDE    
    #   Proximity.OUTSIDE            
    #   Proximity.TOUCHING_OUTSIDE   
    #   Proximity.IN_FIELD           
    #   Proximity.IN_DOORWAY         
    #   Proximity.OUTSIDE_AT_DOORWAY 
    #   Proximity.INSIDE_AT_DOORWAY

    #Face
    #   Face.NONE
    #   Face.NORTH
    #   Face.EAST
    #   Face.SOUTH
    #   Face.WEST
    #   Face.FLOOR
    #   Face.CEILING

    return Proximity.UNKNOWN, Face.NONE #TODO


def isInside(px, py, pz):
    """Is the player safely inside the force field?"""
    global lastprox
    
    ptype, pface = getProximity(px, py, pz)
    if ptype == Proximity.INSIDE \
    or ptype == Proximity.INSIDE_AT_DOORWAY \
    or ptype == Proximity.TOUCHING_INSIDE:
        return True # INSIDE
    
    # IN_FIELD and IN_DOORWAY create a result that depends on lastprox
    if ptype == Proximity.IN_FIELD:
        if lastprox == Proximity.INSIDE or lastprox == Proximity.TOUCHING_INSIDE:
            return True # INSIDE
        
        if lastprox == Proximity.OUTSIDE or lastprox == Proximity.TOUCHING_OUTSIDE:
            return False # NOT INSIDE

        #TODO sideways movements from doorway to field?
        #TODO where is lastprox updated?
        return False # NOT INSIDE

    if ptype == Proximity.IN_DOORWAY:
        if lastprox == Proximity.INSIDE or lastprox == Proximity.INSIDE_AT_DOORWAY:
            return True # NOT INSIDE
        
        if lastprox == Proximity.OUTSIDE or lastprox == Proximity.OUTSIDE_AT_DOORWAY:
            return False # NOT INSIDE

        #TODO sideways movements from field to doorway?
        #TODO where is lastprox updated?
        return False # NOT INSIDE


def isOutside(px, py, pz):
    """Is the player safely outside the force field?"""
    ptype, pface = getProximity(px, py, pz)
    #TODO: see notes on getProximity()
    #OUTSIDE, OUTSIDE_AT_DOORWAY, TOUCHING_OUTSIDE
    #IN and DOORWAY create a result that depends on previous state
    # Similar logic to isInside
    pass # TODO


def isTouchingField(px, py, pz):
    """Is the player touching the force field?"""
    ptype, pface = getProximity(px, py, pz)
    if ptype == Proximity.TOUCHING_INSIDE or ptype == PROXIMITY_TOUCHING_OUTSIDE \
    or ptype == Proximity.IN_FIELD:
        return True
    return False


def isInField(px, py, pz):
    """Is the player touching the force field?"""
    ptype, pface = getProximity(px, py, pz)
    if ptype == Proximity.IN_FIELD:
        return True
    return False
    

def isAtDoorway(px, py, pz):
    """Work out if player is at the door region"""
    ptype, pface = getProximity(px, py, pz)
    if ptype == Proximity.OUTSIDE_AT_DOORWAY \
    or ptype == Proximity.INSIDE_AT_DOORWAY \
    or ptype == Proximity.IN_DOORWAY:
        return True
    return False


def loop():
    """Run the forcefield checking loop"""
    global lastgood_x, lastgood_y, lastgood_z

    # TODO if the player walks through the door, need to allow them
    # to be the other side. But in a way that the forcefield is still
    # active in all the other regions.
    # i.e. really the forcefield should always work in both directions?
    # or perhaps we have to configure which directions the forcefield
    # is enabled (disabled, keepin, keepout, bothways)

    #TODO do we have to update lastprox here?
    
    pos = mc.player.getTilePos()

    #TODO directions on doorway?
    if not door_closed and isAtDoorway(pos.x, pos.y, pos.z):
        return # Don't buzz if walking through door

    #TODO direction enforcements on field?
    if keep_inside and not isInside(pos.x, pos.y, pos.z) and not:
        buzz()

    #TODO direction enforcements on field?
    elif not keep_inside and isInside(pos.x, pos.y, pos.z):
        buzz()
        
    elif isInField(pos.x, pos.y, pos.z):
        buzz()
        
    elif isTouchingField(pos.x, pos.y, pos.z):
        warning()
        
    else: # must be ok, nothing specific to report
        lastgood_x = pos.x
        lastgood_y = pos.y
        lastgood_z = pos.z

        
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


def showDoorway(visible=True):
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
    defineDoorway(15,0,15,20,0,20)
    build()
    keepin()
    enable()
    showDoorway()
    openDoorway()
    
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
    defineDoorway(15,0,15,20,0,20)
    build()
    keepout()
    enable()
    showDoorway()
    openDoorway()
    
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
