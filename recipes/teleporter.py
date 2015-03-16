# teleporter.py  16/03/2015  D.J.Whale
#
# Shows how to move the player to a different location
#
# Idea taken from Adventures In Minecraft, Adventure 2, rent.py

import mcpi.minecraft as minecraft

mc  = minecraft.Minecraft.create()

x = None
y = None
z = None

saved_x = None
saved_y = None
saved_z = None


def define(to_x, to_y, to_z):
    """Remember the location to teleport to"""
    global x, y, z

    x      = to_x
    y      = to_y
    z      = to_z


def jump():
    """Jump to the teleport destination"""
    global saved_x, saved_y, saved_z
    
    pos = mc.player.getTilePos()
    saved_x = pos.x
    saved_y = pos.y
    saved_z = pos.z
    mc.player.setTilePos(x, y, z)
    

def back():
    """Jump back to the position before the teleport"""
    mc.player.setTilePos(saved_x, saved_y, saved_z)

    
# TEST HARNESS

def test():
    """Test that the teleporter works"""
    import time
    
    TO_X = 10
    TO_Y = 0
    TO_Z = 10
    define(TO_X, TO_Y, TO_Z)
    
    mc.postToChat("Teleporting...")
    time.sleep(3)
    jump()
    mc.postToChat("You have arived!")

    time.sleep(5)

    mc.postToChat("Taking you back")
    time.sleep(3)
    back()
    mc.postToChat("You are back home!")

# Only run the test code if this file is the main program

if __name__ == "__main__":
    test()

# END
