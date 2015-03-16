# lights_on_off.py  31/01/2015  D.J.Whale
#
# Show how to turn torches on and off automatically.
# Builds the turner prize "room with a light going on and off"
# Stand in the room, and the lights go on and off.
# Stand outside the room, and they don't (or do they?!)


import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import geofence
import room

FLASH_TIME = 1.0
SIZE       = 10

mc  = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

room.define(pos.x+2, pos.y, pos.z, SIZE, SIZE, SIZE)
geofence.define(pos.x+2, pos.y, pos.z, SIZE, SIZE, SIZE)


def placeTorches():
    """Place a torch on each inner face of the room"""
    global torches

    # FRONT WALL
    x = room.x+(room.width/2) # in middle
    y = room.y+(room.height-3) # down a little bit
    z = room.z+1 # on inside
    pos = (x, y, z)
    torches.append(pos)
    

    # RIGHT WALL
    x = room.x+1 # on inside
    y = room.y+(room.height-3) # down a little bit
    z = room.z+(room.depth/2) # in middle
    pos = (x, y, z)
    torches.append(pos)

    
    # LEFT WALL
    x = room.x+room.width-2 # on inside
    y = room.y+(room.height-3) # down a little bit
    z = room.z+(room.depth/2) # in middle
    pos = (x, y, z)
    torches.append(pos)


    # BACK WALL
    x = room.x+(room.width/2) # in middle
    y = room.y+(room.height-3) # down a little bit
    z = room.z+room.depth-2 # on inside
    pos = (x, y, z)
    torches.append(pos)


    # PLACE TORCHES (not lit)
    setTorches(False)


def setTorches(on):
    """Turn all torches on or off"""
    for torch in torches:
        x = torch[0]
        y = torch[1]
        z = torch[2]
        if on:
            mc.setBlock(x, y, z, block.TORCH.id)
        else:
            mc.setBlock(x, y, z, block.AIR.id)


inRoom    = False
torchesOn = False
torches   = []
nexttime  = None


def manageRoom():
    """Monitor and manage the room"""
    global inRoom, nexttime, torchesOn
    
    if not inRoom and geofence.playerInside():
        setTorches(True)
        inRoom = True
        nexttime = time.time() + FLASH_TIME
        
    elif inRoom and not geofence.playerInside():
        setTorches(False)
        inRoom = False

    elif inRoom:
        now = time.time()
        if now > nexttime:
            torchesOn = not torchesOn
            setTorches(torchesOn)
            nexttime = now + FLASH_TIME


# GAME LOOP
try:
    room.build()
    placeTorches()

    while True:
        time.sleep(0.1)
        manageRoom()
    
finally:
    room.destroy()

# END
