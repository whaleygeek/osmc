# room.py  15/03/2015  D.J.Whale
#
# builds a room.
# Idea taken from Adventures in Minecraft Adventure 6 (duplicator.py)


import mcpi.minecraft as minecraft
import mcpi.block as block

mc  = minecraft.Minecraft.create()

x      = None
y      = None
z      = None
width  = None
height = None
depth  = None


def define(rx, ry, rz, rwidth, rheight, rdepth):
    """Define the parameters of the room"""
    global x, y, z, width, height, depth
    x      = rx
    y      = ry
    z      = rz
    width  = rwidth
    height = rheight
    depth  = rdepth

    
def build():
    """Build a room with a door and a light"""
    
    # build walls
    mc.setBlocks(x,       y,        z,
                 x+width, y+height, z+depth,
                 block.WOOD_PLANKS.id)

    # carve out the inside
    mc.setBlocks(x+1,       y,          z+1,
                 x+width-2, y+height-1, z+depth-2,
                 block.AIR.id)

    # carve out a door in middle of front face
    mc.setBlocks(x+(width/2)-2, y,   z,
                 x+(width/2)+2, y+4, z,
                 block.AIR.id)

    # add a light so you can see inside
    mc.setBlock(x+(width/2), y+height-4, z+1,
                block.TORCH.id)


def clear():
    """remove all blocks inside the room"""
    # build room contents out of air
    mc.setBlocks(x+1,         y,            z+1,
                 x+(width-1), y+(height-1), z+(depth-1),
                 block.AIR.id)
    
    # put back the light
    mc.setBlock(x+(width/2), y+height-4, z+1,
                block.TORCH.id)

    
def destroy():
    """Remove all traces of the room"""
    # build room out of air
    mc.setBlocks(x,       y,        z,
                 x+width, y+height, z+depth,
                 block.AIR.id)


# TEST HARNESS

def test():
    """Test that the room build works"""
    import time
    pos  = mc.player.getTilePos()
    SIZE = 10

    define(pos.x+4, pos.y, pos.z, SIZE, SIZE, SIZE)
    mc.postToChat("Building the room")
    time.sleep(3)
    build()

    # Build something in there
    mc.setBlocks(x+(width*1/4), y,              z+(depth*1/4),
                 x+(width*3/4), y+(height*1/4), z+(depth*3/4),
                 block.MELON.id)
    
    mc.postToChat("Take a look for 10 secs")
    time.sleep(10)
    
    mc.postToChat("Room about to be cleared")
    time.sleep(3)
    clear()
    mc.postToChat("Room cleared")

    time.sleep(10)
    mc.postToChat("About to demolish room in 3 seconds")
    time.sleep(3)
    destroy()
    mc.postToChat("The room has gone")
    

# Only run the test code if this file is the main program

if __name__ == "__main__":
    test()

# END
