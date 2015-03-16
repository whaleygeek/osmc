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

      
def save(x, y, z, width, height, depth, filename):
        """Save a cuboid region to a file"""
	f = open(filename, "w")

        # metadata header
	f.write(str(SIZEX) + "," + str(SIZEY) + "," + str(SIZEZ) + "\n")

	for y in range(SIZEY):
		# Write a blank line at the start of each layer of data    
		f.write("\n")

		for x in range(SIZEX):
			line = ""

			for z in range(SIZEZ):
				blockid = mc.getBlock(originx+x, originy+y, originz+z)
				if line != "":
					line = line + ","
				line = line + str(blockid)
			f.write(line + "\n")
	f.close()
  
    
def load(filename, x, y, z):
        """load from a file to a cuboid region"""
	f = open(filename, "r")
 
	lines = f.readlines()

	# The first line in the file is the metadata, it holds the 3 sizes
	coords = lines[0].split(",")
	sizex = int(coords[0])
	sizey = int(coords[1])
	sizez = int(coords[2])

        # each following line contains a full raster of blockId's
	lineidx = 1

	for y in range(sizey):
		lineidx = lineidx + 1
		for x in range(sizex):
			line = lines[lineidx]
			# skip expected space between layers
			lineidx = lineidx + 1
			data = line.split(",")
			for z in range(sizez):
				blockid = int(data[z])
				mc.setBlock(originx+x, originy+y, originz+z, blockid)
	f.close()


# TEST HARNESS

def testLoad():
        """Test the load feature"""
        listing()
        name = raw_input("filename? ")
        pos = mc.player.getTilePos()
        load(pos.x+5, pos.y, pos.z, filename)


def testSave():
        """Test the save feature"""
        listing()
        name = raw_input("filename to save to? ")
        size = int(raw_input("size of area? "))
        size = size/2
        pos = mc.player.getTilePos()
        save(pos.x-size, pos.y,         pos.z-size,
             pos.x+size, pos.y+(size*2) pos.z,
             filename)


# MAIN PROGRAM (only if this script is run)

if __name__ == "__main__":
        testSave()
        testLoad()
        
# END
