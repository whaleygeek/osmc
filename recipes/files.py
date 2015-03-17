# files.py  16/03/2015  D.J.Whale
#
# file load and save of spaces in Minecraft

import mcpi.minecraft as minecraft
import mcpi.block as block
import glob

FILE_EXTN = "*.csv"

mc = minecraft.Minecraft.create()


def listing():
    """List all files that could be loaded"""
    files = glob.glob(FILE_EXTN)

    for filename in files:
        print(filename)

    print("\n")


def save(sx, sy, sz, width, height, depth, filename):
    """Save a cuboid region to a file"""
    f = open(filename, "w")
    print("whd=" + str(width) + " " + str(height) + " " + str(depth))

    # metadata header
    f.write(str(width) + "," + str(height) + "," + str(depth) + "\n")

    for y in range(height):
        print("save:" + str(y) + "/" + str(height))
        # Write a blank line at the start of each layer of data
        f.write("\n")

        for x in range(width):
            line = ""
            print("..save:" + str(x) + "/" + str(width))
            for z in range(depth):
                blockid = mc.getBlock(sx+x, sy+y, sz+z)
                if line != "":
                    line = line + ","
                line = line + str(blockid)
            f.write(line + "\n")
    f.close()


def getsize(filename):
    """Get size information from a file"""
    f = open(filename, "r")

    line = f.readline()

    # The first line in the file is the metadata, it holds the 3 sizes
    coords = line.split(",")
    width  = int(coords[0])
    height = int(coords[1])
    depth  = int(coords[2])
    f.close()
    return width, height, depth

    
def load(sx, sy, sz, filename):
    """load from a file to a cuboid region"""
    f = open(filename, "r")

    lines = f.readlines()

    # The first line in the file is the metadata, it holds the 3 sizes
    coords = lines[0].split(",")
    width = int(coords[0])
    height = int(coords[1])
    depth = int(coords[2])

    # each following line contains a full raster of blockId's
    lineidx = 1

    for y in range(height):
        print("load:" + str(y) + "/" + str(height))
        lineidx = lineidx + 1
        for x in range(width):
            line = lines[lineidx]
            # skip expected space between layers
            lineidx = lineidx + 1
            data = line.split(",")
            for z in range(depth):
                blockid = int(data[z])
                mc.setBlock(sx+x, sy+y, sz+z, blockid)
    f.close()


# TEST HARNESS

def testLoad():
    """Test the load feature"""
    listing()
    filename = raw_input("filename? ")
    pos = mc.player.getTilePos()
    width, height, depth = getsize(filename)
    # Put the player at the centre of the construction
    width = width / 2
    depth = depth / 2
    load(pos.x-width, pos.y, pos.z-depth, filename)


def testSave():
    """Test the save feature"""
    listing()
    filename = raw_input("filename to save to? ")
    size = int(raw_input("size of area? "))
    pos = mc.player.getTilePos()
    half = size/2
    save(pos.x-half, pos.y, pos.z-half,
         size, size, size,
         filename)


# MAIN PROGRAM (only if this script is run)

if __name__ == "__main__":
    testSave()
    testLoad()

# END
