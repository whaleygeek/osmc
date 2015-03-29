# minroom.py  21/03/2015  D.J.Whale
#
# Model of a minimum room and it's surroundings.
# The minimum room is a 9x9x9 model as follows:
# 0 = outside, 1=outside_touching, 2=on, 3=inside_touching
# 4 = inside
# 5 = inside_touching, 6=on, 7=outside_touching, 8=outside
#
# Any 3D rectangular room can be scaled down to this minroom.
# There is an internal 9x9x9 lookup table, where the scaled down
# coordinates are used to index into this table, and the type of proximity
# can be quickly calculated.
#
# The model is pre-computed at startup.
# Pre-computing the model makes proximity and face calculations much
# simpler, and therefore quicker, at runtime.
# This is important if you are doing regular proximity and face checks,
# e.g. for geofencing a forcefield protected room while a player is
# moving live.
#
# How to use:
# 1) work out the translation coefficients that map your room onto minroom
#    translation = getCubeTranslation(x1, y1, z1, x2, y2, z2)
#    x1,y1,z1 is lower left corner of wall of room
#    x2,y2,z2 is upper right corner of wall of room
#
# 2) Get the position of a point in or around the room (e.g. player pos)
#    pos = mc.player.getTilePos()
#
# 3) Translate the point and get the proximity type for that position
#    prox, face = getPointProximity(translation, pos.x, pos.y, pos.z)
#
# 4) Make a decision based on proximity type
#    if prox == Proximity.OUTSIDE:
#    if prox == Proximity.OUTSIDE_TOUCHING:
#    if prox == Proximity.ON:
#    if prox == Proximity.INSIDE_TOUCHING:
#    if prox == Proximity.INSIDE:
#
# 5) Make a decision based on face type
#    if face == Face.NORTH:
#    if face == Face.EAST:
#    if face == Face.SOUTH:
#    if face == Face.WEST:
#    if face == Face.FLOOR:
#    if face == Face.CEILING:
#    if face == Face.NONE:


def getCubeTranslation(x1, y1, z1, x2, y2, z2):
    """Calculate offsets and scales to translate any room down to minroom"""
    # cube parameter coordinates
    # x1,y1,z1 smallest coordinate on the wall
    # x2,y2,z2 biggest coordinate on the wall

    #TODO refactor, 3 times the same equation, put in a function
    
    # calculate outside coordinates
    x1_os = x1-2
    y1_os = y1-2
    z1_os = z1-2

    x2_os = x2+2
    y2_os = y2+2
    z2_os = z2+2
    
    # translate so that lowest non-touching corner is at 0,0,0
    # translate lowest point down to minroom corner

    ox = x1_os
    oy = y1_os
    oz = z1_os
    
    # translate highest point by the same amount (not scaled yet)
    # this puts p2_new outside on far edge
    x2_new = x2_os - ox
    y2_new = y2_os - oy
    z2_new = z2_os - oz

    # work out scale factor to scale p2 down to minroom
    # minroom is 9x9x9

    sx = float(x2_new) / 9.0
    sy = float(y2_new) / 9.0
    sz = float(z2_new) / 9.0

    # To translate any point in user_room to min_room:
    # x=(x-ox)/sx, y=(y-oy)/sy, z=(z-oz)/sz
    return (ox, oy, oz, sx, sy, sz)


def translatePoint(translation, px, py, pz):
    """Translate a single point down to the minroom"""
    ox, oy, oz, sx, sy, sz = translation # unpack translation coefficients

    # apply offset then scale
    mpx = (px-ox)/sx
    mpy = (py-oy)/sy
    mpz = (pz-oz)/sz

    # make into int indexes
    # TODO round() or trunc() here??

    mpx = int(mpx)
    mpy = int(mpy)
    mpz = int(mpz)

    # Clamp out of range indexes to the minroom
    mpx = min(max(0, mpx), 8)
    mpy = min(max(0, mpy), 8)
    mpz = min(max(0, mpz), 8)

    return (mpx, mpy, mpz)
       

def getPointProximity(translation, px, py, pz):
    """Work out the proximity type of this point to the given room"""
    
    ix, iy, iz = translatePoint(translation, px, py, pz)
    mc.postToChat("x:" + str(ix) + " y:" + str(iy) + " z:" + str(iz))
    
    proximity, face = model[ix][iy][iz]
    #print((proximity, face))
    
    return proximity, face
    

# Proximity types
class Proximity:
    UNKNOWN            = "unknown"          # 'X'
    INSIDE             = "inside"           # 'I'
    INSIDE_TOUCHING    = "inside_touching"  # 'IZ'
    OUTSIDE            = "outside"          # 'O'
    OUTSIDE_TOUCHING   = "outside_touching" # 'OZ'
    ON                 = "on"               #'Z'
 
# Face types
class Face:
    NONE    = 'X'
    NORTH   = 'N'
    SOUTH   = 'S'
    EAST    = 'E'
    WEST    = 'W'
    FLOOR   = 'F'
    CEILING = 'C'


def buildEmptyModel(sx, sy, sz):
    # make a 9*9*9 list of lists of lists (independent lists)
    xlist = []
    for x in range(sx):
        ylist = []
        for y in range(sy):
            zlist = []
            for z in range(sz):
                zlist.append(None)
            ylist.append(zlist)
        xlist.append(ylist)
    return xlist

  
def fillProximity(model):
    # fill in 5 wrapped shells of proximity data, centered at (4,4,4)

    # shell 0 (1 write)
    model[4][4][4] = Proximity.INSIDE

    # shell 1 (27 reads, 26 writes)
    for x in [3,4,5]:
        for y in [3,4,5]:
            for z in [3,4,5]:
                if model[x][y][z] == None:
                    model[x][y][z] = Proximity.INSIDE_TOUCHING

    # shell 2 (125 reads, 98 writes)
    for x in [2,3,4,5,6]:
        for y in [2,3,4,5,6]:
            for z in [2,3,4,5,6]:
                if model[x][y][z] == None:
                    model[x][y][z] = Proximity.ON

    # shell 3 (343 reads, 218 writes)
    for x in [1,2,3,4,5,6,7]:
        for y in [1,2,3,4,5,6,7]:
            for z in [1,2,3,4,5,6,7]:
                if model[x][y][z] == None:
                    model[x][y][z] = Proximity.OUTSIDE_TOUCHING

    # shell 4 (729 reads, 386 writes)
    for x in [0,1,2,3,4,5,6,7,8]:
        for y in [0,1,2,3,4,5,6,7,8]:
            for z in [0,1,2,3,4,5,6,7,8]:
                if model[x][y][z] == None:
                    model[x][y][z] = Proximity.OUTSIDE

def calcFace(x,y,z):
    return '?'
    #TODO calculate N,S,E,W,F,C,X
    #based on an algebraic specification with respect to (x,y,z)
    #with x,y,z == (0..8)


def fillFaces(model):                   
    for x in range(0,9):
        for y in range(0,9):
            for z in range(0,9):
                prox = model[x][y][z]
                face = calcFace(x,y,z)
                data = (prox, face)
                model[x][y][z] = data



# TEST HARNESS -----------------------------------------------------------------

# Visualise in minecraft blocks
# one shell at a time
# different colour for different proximity

def visualise():
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    pos.x += 1

    prox_list  = [
        Proximity.INSIDE,
        Proximity.INSIDE_TOUCHING,
        Proximity.ON,
        Proximity.OUTSIDE_TOUCHING,
        Proximity.OUTSIDE
    ]

    block_list = [
        block.STONE.id,
        block.GLASS.id,
        block.MELON.id,
        block.GLASS.id,
        block.STONE.id
    ]

    for i in range(len(prox_list)):
        wantedProximity = prox_list[i]
        b = block_list[i]
        
        for x in range(9):
            for y in range(9):
                for z in range(9):
                    prox,face = model[x][y][z]
                    if prox == wantedProximity:
                        #print(str((x,y,z)))
                        mc.setBlock(pos.x+x, pos.y+y, pos.z+z, b)

        mc.postToChat("Look at shell:" + str(i))

                    

    #TODO: when face done, do the same
    # different colour wool for each of 6 face types

    #TODO: When tested, capture the model[][][] initialiser and
    #just put it in a .py file, so it can be restored quickly
    #when the module restarts.


def buildroom(x1, y1, z1, x2, y2, z2, b):
    # build a physical room
    mc.setBlocks(x1,   y1,   z1,   x2,   y2,   z2,   b)
    mc.setBlocks(x1+1, y1+1, z1+1, x2-1, y2-1, z2-1, block.AIR.id)

    
def testroom():
    pos = mc.player.getTilePos()
    RR = (0,0,0,10,10,10)
    R = (pos.x+RR[0], pos.y+RR[1], pos.z+RR[2], pos.x+RR[3], pos.y+RR[4], pos.z+RR[5])
    
    buildroom(R[0], R[1], R[2], R[3], R[4], R[5], block.GLASS.id)

    # work out translation coefficients
    translate = getCubeTranslation(R[0], R[1], R[2], R[3], R[4], R[5])

    try:
        # game loop - monitor player proximity
        while True:
            time.sleep(1)
            pos = mc.player.getTilePos()
            prox,face = getPointProximity(translate, pos.x, pos.y, pos.z)
            mc.postToChat("prox:" + str(prox))
    finally:
        # destroy the room on exit
        buildroom(R[0], R[1], R[2], R[3], R[4], R[5], block.AIR.id)
        

# MAIN PROGRAM -----------------------------------------------------------------

model = buildEmptyModel(9, 9, 9)
fillProximity(model)
fillFaces(model)

if __name__ == "__main__":
    #print(str(model))
    #visualise()
    
    import mcpi.minecraft as minecraft
    import mcpi.block as block
    import time
    mc = minecraft.Minecraft.create()
    
    testroom()

# END

