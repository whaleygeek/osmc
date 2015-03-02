# autotorch.py  31/01/2015  D.J.Whale
#
# Show how to turn torches on and off automatically.
# Builds the turner prize "room with a light going on and off"
# Stand in the room, and the lights go on and off.
# Stand outside the room, and they don't (or do they?!)


import mcpi.minecraft as minecraft
import mcpi.block as block
import time

FLASH_TIME = 1.0
WIDTH = 10
DEPTH = 10
HEIGHT = 10

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()
ROOM_X = pos.x + 2
ROOM_Y = pos.y
ROOM_Z = pos.z


def buildRoom():
    """Build a cube room with a door"""
    # build a cube
    mc.setBlocks(ROOM_X, ROOM_Y, ROOM_Z, ROOM_X+WIDTH, ROOM_Y+HEIGHT, ROOM_Z+DEPTH, block.WOOD_PLANKS.id)

    # carve out the inside
    mc.setBlocks(ROOM_X+1, ROOM_Y, ROOM_Z+1, ROOM_X+WIDTH-2, ROOM_Y+HEIGHT-1, ROOM_Z+DEPTH-2, block.AIR.id)

    # carve out a door in middle of front face
    mc.setBlocks(ROOM_X+(WIDTH/2)-2, ROOM_Y, ROOM_Z,
                 ROOM_X+(WIDTH/2)+2, ROOM_Y+4, ROOM_Z, block.AIR.id)


def destroyRoom():
    """Remove all traces of the room"""
    # build cube out of air
    mc.setBlocks(ROOM_X, ROOM_Y, ROOM_Z, ROOM_X+WIDTH, ROOM_Y+HEIGHT, ROOM_Z+DEPTH, block.AIR.id)


def placeTorches():
    """Place a torch on each inner face of the room"""
    global torches

    # FRONT WALL
    x = ROOM_X+(WIDTH/2) # in middle
    y = ROOM_Y+(HEIGHT-3) # down a little bit
    z = ROOM_Z+1 # on inside
    pos = (x, y, z)
    torches.append(pos)
    

    # RIGHT WALL
    x = ROOM_X+1 # on inside
    y = ROOM_Y+(HEIGHT-3) # down a little bit
    z = ROOM_Z+(DEPTH/2) # in middle
    pos = (x, y, z)
    torches.append(pos)

    
    # LEFT WALL
    x = ROOM_X+WIDTH-2 # on inside
    y = ROOM_Y+(HEIGHT-3) # down a little bit
    z = ROOM_Z+(DEPTH/2) # in middle
    pos = (x, y, z)
    torches.append(pos)


    # BACK WALL
    x = ROOM_X+(WIDTH/2) # in middle
    y = ROOM_Y+(HEIGHT-3) # down a little bit
    z = ROOM_Z+DEPTH-2 # on inside
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


def playerInRoom():
    """Geo fence the room, returns True if inside the room"""
    pos = mc.player.getTilePos()
    if pos.x >= ROOM_X and pos.x <= ROOM_X + WIDTH \
    and pos.y >= ROOM_Y and pos.y <= ROOM_Y + HEIGHT \
    and pos.z >= ROOM_Z and pos.z <= ROOM_Z + DEPTH:
        return True # in room
    return False # not in room


inRoom = False
torchesOn = False
torches = []
nexttime = None


def manageRoom():
    """Monitor and manage the room"""
    global inRoom, nexttime, torchesOn
    
    if not inRoom and playerInRoom():
        setTorches(True)
        inRoom = True
        nexttime = time.time() + FLASH_TIME
        
    elif inRoom and not playerInRoom():
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
    buildRoom()
    placeTorches()

    while True:
        time.sleep(0.1)
        manageRoom()
    
finally:
    destroyRoom()

# END
