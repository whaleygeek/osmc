# geofence.py  15/03/2015  D.J.Whale
#
# Shows how to geo-fence a range of coordinates
#
# Set the geofence range with define()
# build a functional room with build()
# remove the room with destroy()
# check if player present with playerInside()
#
# Test harness demonstrates:
#   Whenever your player is within this region, the action() function
#   is called. When your player is not within this region, the action()
#   function is not called.
#
# import this module if you want to use it's features in another program.
# run this module directly if you want to test it out
#
# Idea taken from Adventures In Minecraft, Adventure 2, rent.py

import mcpi.minecraft as minecraft
import mcpi.block as block

mc  = minecraft.Minecraft.create()

x      = None
y      = None
z      = None
width  = None
height = None
depth  = None


def define(x1, y1, z1, w, h, d):
    """Remember the location and dimensions of the room"""
    global x, y, z, width, height, depth

    # Remember the dimensions of the room
    x      = x1
    y      = y1
    z      = z1
    width  = w
    height = h
    depth  = d


def highlight(visible):
    """Highlight the corners of the geofenced region"""
    if visible:
        b = block.STONE.id
    else:
        b = block.AIR.id

    mc.setBlock(x,       y,        z, b)
    mc.setBlock(x+width, y,        z, b)
    mc.setBlock(x,       y+height, z, b)
    mc.setBlock(x+width, y+height, z, b)

    mc.setBlock(x,       y,        z+depth, b)
    mc.setBlock(x+width, y,        z+depth, b)
    mc.setBlock(x,       y+height, z+depth, b)
    mc.setBlock(x+width, y+height, z+depth, b)


def playerInside():
    """Geo fence the room, returns True if inside the room"""
    pos = mc.player.getTilePos()
    return inside(pos.x, pos.y, pos.z)


def inside(px, py, pz):
    if  px >= x and px <= x + width \
    and py >= y and py <= y + height \
    and pz >= z and pz <= z + depth:
        return True # inside geofenced region
    return False # not inside geofenced region


def action():
    """only called when the player is in the room"""
    mc.postToChat("Player is inside geofenced region")



# TEST HARNESS

def test():
    """Test that the geofencing works"""
    import time
    pos  = mc.player.getTilePos()
    SIZE = 20

    define(pos.x+4, pos.y, pos.z, SIZE, SIZE, SIZE)
    highlight(True)
    
    try:
        while True:
            time.sleep(1)
            if playerInside():
                action()
    finally:
        highlight(False)
        

# Only run the test code if this file is the main program

if __name__ == "__main__":
    test()

# END
