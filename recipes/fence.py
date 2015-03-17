# fence.py 17/03/2015  D.J.Whale
#
# a Minecraft wrapper, that validates all coordinates around a 3D fence.
# coordinates inside the fence will delegate to the real minecraft interface.
# coordinates outside will call a buzz() method and squash the call.
#
# This is for building electric fences around sandboxed regions.

import mcpi.minecraft as minecraft
from mcpi.vec3 import Vec3

def trace(msg):
    print("fence." + str(msg))


class Fence():
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2


    def isPointInside(self, x, y, z):
        if  x >= self.x1 and x <= self.x2 \
        and y >= self.y1 and y <= self.y2 \
        and z >= self.z1 and z <= self.z2:
            return True # inside
        return False # outside


    def isSpikeInside(self, x, z):
        return self.isPointInside(x, self.y1, z)


    def isRegionInside(self, x1, y1, z1, x2, y2, z2):
        if x1 < self.x1 or x1 > self.x2:
            return False
        if x2 < self.x1 or x2 > self.x2:
            return False
        
        if y1 < self.y1 or y1 > self.y2:
            return False
        if y2 < self.y1 or y2 > self.y2:
            return False

        if z1 < self.z1 or z1 > self.z2:
            return False
        if z2 < self.z1 or z2 > self.z2:
            return False

        return True # must all be inside
        

    def checkPointOk(self, x, y, z):
        if not self.isPointInside(x, y, z):
            self.buzz()


    def checkSpikeOk(self, x, z):
        if not self.isSpikeInside(x, z):
            self.buzz()


    def checkRegionOk(self, x1, y1, z1, x2, y2, z2):
        if not self.isRegionInside(x1, y1, z1, x2, y2, z2):
            self.buzz()
            

    def buzz(self, culprit=None):
        if culprit == None:
            coords = (self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)
            print("outside of fenced region:" + str(coords))
        else:
            print(str(culprit) + " outside of fenced region")
        #TODO optionally throw exception
    

class FencedMinecraft():
    def __init__(self, fence, inner):
        self.fence = fence
        self.inner = inner
        #self.camera = FencedCamera(fence, inner.camera)
        #self.entity = FencedEntity(fence, inner.entity)
        self.player = FencedPlayer(fence, inner.player)
        self.events = FencedEvents(fence, inner.events)


    @staticmethod
    def create(addr, x1, y1, z1, x2, y2, z2, inner=None):
        trace("create")
        fence = Fence(x1, y1, z1, x2, y2, z2)

        if inner == None:
            # statically bound at this point to the imported mcpi.minecraft
            inner = minecraft.Minecraft.create(addr)
        return FencedMinecraft(fence, inner)

    
    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        trace("getBlock:" + str(args))
        x,y,z = args
        if self.fence.checkPointInside(x,y,z):
            return self.inner.getBlock(args)
        else:
            return None
        
        
    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        trace("getBlockWithData:" + str(args))
        x,y,z = args
        if self.checkPointInside(x,y,z):
            return self.fence.getBlockWithData(args)
        else:
            return None


    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        trace("getBlocks:" + str(args))
        x1,y1,z1,x2,y2,z2 = args
        if self.checkRegionOk(x1,y1,z1,x2,y2,z2):
            return self.fence.getBlocks(args)
        else:
            return None


    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        trace("setBlock:" + str(args))
        x,y,z,b = args
        if self.fence.checkPointOk(x,y,z):
            self.inner.setBlock(args)
        

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        trace("setBlocks:" + str(args))
        x1,y1,z1,x2,y2,z2,data = args
        if self.fence.checkRegionOk(x1,y1,z1,x2,y2,z2):
            self.inner.setBlocks(args)
        

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        trace("getHeight:" + str(args))
        x,z = args
        if self.fence.checkSpikeOk(x,z):
            return self.inner.getHeight(args)
        else:
            return None
        

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        trace("getPlayerEntityIds")
        return self.inner.getPlayerEntityIds()


    #def saveCheckpoint(self):
    #    """Save a checkpoint that can be used for restoring the world"""
    #    pass


    #def restoreCheckpoint(self):
    #    """Restore the world state to the checkpoint"""
    #    pass


    def postToChat(self, msg):
        """Post a message to the game chat"""
        trace("postToChat:" + str(msg))
        self.inner.postToChat(msg)
        

    #def setting(self, setting, status):
    #    """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
    #    pass
    

class FencedPlayer():
    def __init__(self, fence, inner):
        self.fence = fence
        self.inner = inner


    def getPos(self):
        trace("player.getPos")
        return inner.getPos()
    

    def setPos(self, *args):
        trace("player.setPos:" + str(args))
        x,y,z = args
        if self.fence.checkPointOk(x,y,z):
            self.inner.setPos(args)
                

    def getTilePos(self):
        trace("player.getTilePos:" + str(args))
        return self.inner.getTilePos()
        

    def setTilePos(self, *args):
        trace("setTilePos:" + str(args))
        x,y,z = args
        if self.fence.checkPointOk(x,y,z):
            self.inner.setTilePos(args)

        
class FencedEvents:
    def __init__(self, fence, inner):
        self.fence = fence
        self.inner = inner

        
    def clearAll(self):
        """Clear all old events"""
        trace("events.clearAll")
        self.inner.clearAll()
        

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        trace("events.pollBlockHits")
        #TODO work through list and filter out any out of range
        return self.inner.pollBlockHits()


class FencedCamera:
    def __init__(self, fence, inner):
        self.fence = fence
        self.inner = inner


    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.inner.setNormal(args)


    def setFixed(self):
        """Set camera mode to fixed view"""
        self.inner.setFixed()


    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.inner.setFollow(args)


    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        x,y,z = args
        if self.fence.checkPointOk(x,y,z):
            self.inner.setPos(args)


    
# TEST HARNESS

def test():
    """Test that the fencing works"""
    mc = FencedMinecraft.create("localhost", 10,10,10,20,20,20)

    print("\n")
    print("try:outside of fence")
    mc.player.setTilePos(100, 100, 100) # should buzz
    print("\n")

    print("try:inside of fence")
    mc.player.setTilePos(11, 11, 11)    # should not buzz
    print("\n")

    print("try:outside of fence")
    mc.setBlock(100, 100, 100, 1) # should buzz
    print("\n")

    print("try:inside of fence")
    mc.setBlock(11, 11, 11, 1) # should not buzz
    print("\n")

    print("try:outside of fence")
    mc.setBlocks(100, 100, 100, 110, 110, 100, 1) # should buzz
    print("\n")

    print("try:inside of fence")
    mc.setBlocks(10, 10, 10, 12, 12, 12, 1) # should buzz
    print("\n")

    print("try:overlapping fence")
    mc.setBlocks(8, 8, 8, 12, 12, 12, 1) # should buzz
    print("\n")
    
                 
# Only run the test code if this file is the main program

if __name__ == "__main__":
    test()

# END
