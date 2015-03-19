# forcefield.py  18/03/2015  D.J.Whale
#
# NOTE: Still a work in progress
# NOTE: Still getting the internal modelling correct for this module
# NOTE: Not yet tested (at all!)
#
# Shows how to prevent the player from escaping from a force-field protected
# region within minecraft.
#
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
# object oriented implementation - we will do that a little later. First it is
# important to get the logic working correctly.
#
# TODO: A lot of this code will simplify if we build a surface abstraction
# and a point abstraction (sx1, sy1, sz1, sx2, sy2, sz2) and (px, py, pz)
# as classes that group the coordinates together. We can then perform
# coordinate math on those objects, rather than passing all the coordinates
# around to functions. But classes/objects will be a next generation of this
# module once the algorithms have been designed and tested (i.e. object
# orientation done by refactoring, adding in classes/objects to solve the
# problems of multiplicity, such as needing multiple doors in a forcefield,
# or needing to handle multiple forcefields simultaneously).

# NOTE: Could we reduce the scale of the problem by reducing actual coordinates
# to small signs and unity deltas, and then just do a brute force compare?
# The compare could be a table-driven compare even.
# This might be an optimisation, it makes sense to leave a logical development
# path in the github history, so people can see how a more advanced and
# optimised solution was created from an initial dumb solution. Only optimise
# once we have figures on performance, so that the right thing is optimised.
#
# Note, most of the maths in this module is independent of minecraft. It could
# be applied to any 3D coordinate space. This might mean that we put all
# the maths in a separate coordinateMaths package, and then write a simple
# minecraft specific implementation around the outside. That might be a
# refactoring step.

import mcpi.minecraft as minecraft
import mcpi.block as block


# SURFACE UTILITIES ------------------------------------------------------------
# Utilities that help with coordinate maths associated with surfaces.
# This is not minecraft specific, and will eventually be refactored into a
# separate utility module. It will also be written with a set of objects
# in a future release, so that we don't have to pass loads of coordinate
# parameters around all the time.

# We would normally assume that a cube is defined from the smallest
# coordinates to the biggest coordinates. But there is nothing that
# requires that to be the case in the Minecraft API (you can draw a cube
# from any two opposite corners). So all of these functions have to assume
# that any scheme could be used, and we normalise coordinates before
# calculation takes place to the smallest first, the biggest second.
# This then simplifies the maths that follows.


def getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2):
    return min(sx1, sy1), min(sy1, sy2), min(sz1, sz2)


def getLargestCoords(sx1, sy1, sz1, sx2, sy2, sz2):
    return max(sx1, sy1), max(sy1, sy2), max(sz1, sz2)


def isPointOnSurface(px, py, pz, sx1, sy1, sz1, sx2, sy2, sz2):
    """Work out if a point is on a given 3D surface"""
    # Usually we will use this with a 2D surface,
    # but it is easier to model it as a 3D surface,
    # it means one function can handle a surface in any dimension.

    minx, miny, minz = getSmallestCoords()
    maxx, mayz, maxy = getLargsetCoords()
    
    if  px >= minx and px <= maxx \
    and py >= miny and py <= maxy \
    and pz >= minz and pz <= maxz:
        return True # IS on surface
    return False # NOT on surface


def getNorthSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the north face of a 3D cube"""
    # +z is south, -z is north (i.e. want the smallest z surface)
    # Note that s?1 does not have to be smaller than s?2
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return minx, miny, minz, maxx, maxy, minz


def getEastSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the east face of a 3D cube"""
    # +x is east, -x is west
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return maxx, miny, minz, maxx, maxy, maxz


def getSouthSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the south face of a 3D cube"""
    # +z is south, -z is north
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return minx, miny, maxz, maxx, maxy, maxz


def getWestSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the west face of a 3D cube"""
    # +x is east, -x is west
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return minx, miny, minz, minx, maxy, maxz


def getFloorSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the floor face of a 3D cube"""
    # -y is down, +y is up
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return minx, miny, minz, maxx, miny, maxz


def getCeilingSurface(sx1, sy1, sz1, sx2, sy2, sz2):
    """Get a surface that represents just the ceiling face of a 3D cube"""
    # -y is down, +y is up
    minx, miny, minz = getSmallestCoords(sx1, sy1, sz1, sx2, sy2, sz2)
    maxx, maxy, maxz = getLargestCoords( sx1, sy1, sz1, sx2, sy2, sz2)
    return minx, maxy, minz, maxx, maxy, maxz

# Might need these in order to assess TOUCHING_INSIDE and TOUCHING_OUTSIDE??
# moveSurfaceNorth
# moveSurfaceEast
# moveSurfaceWest
# moveSurfaceSouth
# moveSurfaceUp
# moveSurfaceDown

# or might not - once we factor out the doorway logic into a separate proximity
# checker, the maths might be much simpler and be done with simple cuboid
# expansions or contractions (or two overlapping cuboid checks), rather
# than doing all the 6-face checking logic.


# PROXIMITY TO A REGION --------------------------------------------------------
# This maths is independent of minecraft, its all to do with coordinates.

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

def getProximity(px, py, pz):
    """Work out what type of proximity to the field we have"""
    
    #Face INITIAL DESIGN
    # Note, this should really be a disambiguator for the other methods.
    # e.g. if you are IN_FIELD, which face are you in?
    # e.g. if you are TOUCHING_OUTSIDE, which face are you touching?
    # if you are TOUCHING_INSIDE, which face are you touching?
    # To calculate the face depends on which surface you are doing pointOnSurface
    # on, which may depend on how far through the proximity assessment tree you are
    #   Face.NORTH
    #   Face.EAST
    #   Face.SOUTH
    #   Face.WEST
    #   Face.FLOOR
    #   Face.CEILING
    #   Face.NONE


    # NOTE: It looks like we might have to separate door proximity
    # from general field proximity, otherwise AT_DOORWAY and INSIDE/OUTSIDE
    # cannot be represented by a single return value.
    
    #Proximity INITIAL DESIGN
    # (regardless of if doorway is open or not)
    #   Proximity.IN_DOORWAY
    #     pointOnSurface(doorway)
    
    #   Proximity.INSIDE_AT_DOORWAY
    #     need to know doorway surface direction
    #     create a surface that is just inside doorway
    #     pointOnSurface(doorwayInside)
    
    #   Proximity.OUTSIDE_AT_DOORWAY
    #     need to know doorway surface direction
    #     create a surface that is just outside doorway
    #     pointOnSurface(doorwayOutside)
    
    #   Proximity.IN_FIELD
    #     need to blot out an open doorway from calculations
    #     if doorway closed, then ignore doorway calcs
    #     could check pointOnSurface() of all 6 faces
    #     if we always calculate what face we are on this might be fine
    #     if we only want to know if in field, quicker way is cube-inner
    
    #   Proximity.TOUCHING_INSIDE
    #     if doorway closed, ignore doorway in calcs
    #     if doorway open, exclude doorway from calcs
    #     could get 6 inner surfaces and check pointOnSurface
    #     or could define inner cube and check if on outer surface of that cube
    #     with -1/+1 on coordinates
    
    #   Proximity.TOUCHING_OUTSIDE
    #     if doorway closed, ingnore doorway in calcs
    #     if doorway open, exclude doorway from calcs
    #     could get 6 outer surfaces and check pointOnSurface
    #     or could define outer cube and check if on outside
    #     with -1/+1 on coordinates
    
    #   Proximity.INSIDE
    #     how does doorway affect this?
    #     if doorway closed, no effect?
    #     but would be nice to know you are standing at the doorway
    #     but then you might not be seen as being inside?
    #     NOTE:### can we handle doorway with this proximity
    #     or does it need to be an independent check after "general proximity"
    #
    #   Proximity.OUTSIDE
    #     same issues as for INSIDE regarding doorway
    #
    #   Proximity.UNKNOWN
    #     would it ever return this? Might be useful for a "prevprox"
    #     but presumably a sample of all the coordinates would always give
    #     us one of the other values?


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


# FORCEFIELD -------------------------------------------------------------------
# This implements the forcefield logic.
# It builds on top of the surface and proximity utilities.

mc  = minecraft.Minecraft.create()

# The coordinates of the forcefield
x1 = None
y1 = None
z1 = None
x2 = None
y2 = None
z2 = None

# Is the player kept inside/outside of the region
#see notes about two independent field directions
#TODO FieldType.DISABLED, FieldType.KEEPIN, FieldType.KEEPOUT, FieldType.BOTHWAYS
keep_inside = True

# The forcefield can be enabled/disabled
enabled = False


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
#TODO see notes about door swing direction
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


#TODO setFieldDirection (keepin keepout should be independently settable)
def keepin(in=True):
    """Keep player inside(True) or outside(False)"""
    global keep_inside
    keep_inside = in


#TODO setFieldDirection (keepin keepout should be independently settable)
def keepout(out=True)
    """Keep player outside(True) or ionside(False)"""
    global keep_inside
    keep_inside = not out


#TODO setFieldDirection (should be a global enable for the field)
def enable(enable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = enable


#TODO setFieldDirection (should be a global disable for the field)
def disable(disable=True):
    """Enable or disable the force field"""
    global enabled
    enabled = not disable


#TODO set swing directions of doorway? (independent allowin/allowout)   
def openDoorway(open=True):
    """Open the door(if True)"""
    global doorway_closed
    doorway_closed = not open

        
#TODO set swing directions of doorway? (independent allowin/allowout)
def closeDoorway(close=True):
    """Close the door(if True)"""
    global doorway_closed
    door_closedway = close


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
