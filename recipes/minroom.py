# minroom.py  21/03/2015  D.J.Whale
#
# Model of a minimum room and it's surroundings,
# lower left front corner translated to (0,0,0).
# Any room can be scaled down to this minimum room.
# Any point coordinate can be scaled down to this minimum room.
# It then allows point comparisons to be made for proximity and face.
# Room coefficients are (ox,oy,oz,sx,sy,sz)
# o=offset(subtracted), s=scale(divided by)
#
# Assessment of proximity and face is then a 3D lookup of an x,y,z index
# in this model.
#
# Pre-computing the model makes proximity and face calculations much
# simpler, and therefore quicker, at runtime.
# This is important if you are doing regular proximity and face checks,
# e.g. for geofencing a forcefield protected room while a player is
# moving live.



# Perform pre-compression of the point
# and pre-compute the model as a unity model (i.e. the smallest it can be)
# point pre-compression could be done by translating the point and the
# model to a near-zero based origin (removing offset).
# the scale could be compressed by....some simple numeric modulus scheme?
# is it a sort of y=mx+c style problem - take off c to translate to zero,
# divide point coords by some divisor to make it fit the unity model,
# then just index into the unity model table (3D table) and read back the
# answer which gives in/touching/out/facetype in one go.

# Here's how this would work:
# minimum model is 9x9x9, with tuples of (proximity, face) in each point.
# work out what divisors in x,y,z are required to scale down the
# forcefield cuboid to a minimum model size (3 float divisions).
# remember these divisors as coefficients.
# work out what subtractors in x,y,z are required to translate the
# forcefield cuboid onto the minimum model (corner at 0,0,0)
# remember these 3 integer coefficients.
# To get the proximity and face of an x,y,z point
#   subtract offset coefficients
#   float divide px,py,pz by the scale coefficients
#   convert all to int
#   lookup x,y,z in the minimal model
#   the resultant tuple is the proximitytype+face.
# the memory space requirements are minimal.
# the computation requirements are small (3 float conversions,
# 3 float divisions, 3 integer conversions, 3 integer subtractions,
# a 3-way index into a data structure).




#def translateCube(x1, y1, z1, x2, y2, z2):
#    #TODO calculate scales and offsets to translate any point in/around room
#    #down to the model coordinates
#    return (ox, oy, oz, sx, sy, sz)



#def translatePoint(room, px, py, pz):
#    # translate a point using the room coefficients.
#    # handle out of range (-ves) properly
#    return ix, iy, iz # TODO indexes into model


#def getPointProximity(room, px, py, pz):
#    ix, iy, iz = translatePoint(room, px, py, pz)
#    proximity, face = model[ix][9-iy][iz]
#    return proximity, face
    

# Proximity types
class Proximity:
    UNKNOWN            = 'X'
    INSIDE             = 'I'
    INSIDE_TOUCHING    = 'IZ'
    OUTSIDE            = 'O'
    OUTSIDE_TOUCHING   = 'OZ'
    ON                 = 'Z'
 
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
    #TODO calculate N,S,E,W,F,C
    #based on an algebraic specification with respect to (x,y,z)


def fillFaces(model):                   
    for x in range(0,9):
        for y in range(0,9):
            for z in range(0,9):
                prox = model[x][y][z]
                face = calcFace(x,y,z)
                data = (prox, face)
                model[x][y][z] = data


# TEST HARNESS

model = buildEmptyModel(9,9,9)
fillProximity(model)
fillFaces(model)
print(str(model))


#TODO: Visualise in minecraft blocks
# one shell at a time
# different colour for different proximity

#TODO: when face done, do the same
# different colour wool for each of 6 face types

#TODO: When tested, capture the model initialiser and
#just put it in a .py file, so it can be restored quickly
#when the module restarts.




