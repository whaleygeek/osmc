# minroom.py  21/03/2015  D.J.Whale
#
# Model of a minimum room and it's surroundings.
# Any room can be scaled down to this minimum room.
# Any point coordinate can be scaled down to this minimum room.
# It then allows point comparisons to be made for proximity and face.
# Room coefficients are (sx,sy,sz,ox,oy,oz)
#
# Assessment of proximity and face is then a 3D lookup of an x,y,z index
# in this model.
#
# Pre-computing the model makes proximity and face calculations much
# simpler, and therefore quicker, at runtime.
# This is important if you are doing regular proximity and face checks,
# e.g. for geofencing a forcefield protected room while a player is
# moving live.



# SCHEME D:
# like scheme C, but perform pre-compression of the point
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
# forcefield cuboid onto the minimum model (centered around 0,0,0)
# remember these 3 integer coefficients.
# To get the proximity and face of an x,y,z point
#   float divide px,py,pz by the scale coefficients
#   convert all to int
#   subtract the offset coefficients
#   lookup x,y,z in the minimal model
#   the resultant tuple is the proximitytype+face.
# the memory space requirements are minimal.
# the computation requirements are small (3 float conversions,
# 3 float divisions, 3 integer conversions, 3 integer subtractions,
# a 3-way index into a data structure).




def getRoomTransform(x1, y1, z1, x2, y2, z2):
    #TODO calculate scales and offsets to translate any point in/around room
    #down to the model coordinates
    return (sx, sy, sz, ox, oy, oz)



def translatePoint(room, px, py, pz):
    # translate a point using the room coefficients.
    # handle out of range (-ves) properly
    return ix, iy, iz # TODO indexes into model


def getPointProximity(room, px, py, pz):
    ix, iy, iz = translatePoint(room, px, py, pz)
    proximity, face = model[ix][iy][iz]
    return proximity, face
    

# Proximity types
class Proximity
    UNKNOWN            = 0 # X
    INSIDE             = 1 # i
    TOUCHING_INSIDE    = 2 # I
    OUTSIDE            = 3 # o
    TOUCHING_OUTSIDE   = 4 # O
    ON_FIELD           = 5 # Z
 
# Face types
class Face
    NONE    = 0 # X
    NORTH   = 1 # N
    SOUTH   = 2 # S
    EAST    = 3 # E
    WEST    = 4 # W
    FLOOR   = 5 # F
    CEILING = 6 # C

# Shorter names for Proximity and Face to make the table easier to write
X = Proximity.UNKNOWN
i = Proximity.INSIDE
I = Proximity.TOUCHING_INSIDE
o = Proximity.OUTSIDE
O = Proximity.TOUCHING_OUTSIDE
Z = Proximity.ON_FIELD

N = Face.NORTH
S = Face.SOUTH
E = Face.EAST
W = Face.WEST
F = Face.FLOOR
C = Face.CEILING


model =
[
    [ # X=0
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=1
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=2
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=3
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=4
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=5
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=6
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=7
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
    [ # X=8
        [ # Y=0
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=1
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=2
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=3
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=4
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=5
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=6
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=7
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
        [ # Y=8
        # Z=  0     1     2     3     4     5     6     7     8    
            (X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),(X,X),
        ],
    ],
]
