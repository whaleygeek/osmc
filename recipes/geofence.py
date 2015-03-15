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
    

def build():
    """Build a room with a door"""
    
    # build walls
    mc.setBlocks(x, y, z,
                 x+width, y+height, z+depth,
                 block.WOOD_PLANKS.id)

    # carve out the inside
    mc.setBlocks(x+1, y, z+1,
                 x+width-2, y+height-1, z+depth-2,
                 block.AIR.id)

    # carve out a door in middle of front face
    mc.setBlocks(x+(width/2)-2, y, z,
                 x+(width/2)+2, y+4, z,
                 block.AIR.id)


def destroy():
    """Remove all traces of the room"""
    # build room out of air
    mc.setBlocks(x, y, z,
                 x+width, y+height, z+depth,
                 block.AIR.id)


def playerInside():
    """Geo fence the room, returns True if inside the room"""
    pos = mc.player.getTilePos()
    if  pos.x >= x and pos.x <= x + width \
    and pos.y >= y and pos.y <= y + height \
    and pos.z >= z and pos.z <= z + depth:
        return True # in room
    return False # not in room


def action():
    """only called when the player is in the room"""
    mc.postToChat("Player is in the room")

    
# TEST HARNESS

def test():
    """Test that the geofencing works"""
    import time
    pos  = mc.player.getTilePos()
    SIZE = 20

    try:
        define(pos.x+4, pos.y, pos.z, SIZE, SIZE, SIZE)
        build()
        
        while True:
            time.sleep(1)
            if playerInside():
                action()
        
    finally:
        destroy()


# Only run the test code if this file is the main program

if __name__ == "__main__":
    test()

# END
