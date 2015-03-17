# minecraft_template.py  08/05/2014  D.J.Whale

from vec3 import Vec3

print("Using minecraft_template - empty mcpi wrapper")

def trace(msg):
    print("minecraft." + str(msg))


class CmdPositioner:
    def __init__(self, connection, packagePrefix):
        pass

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        pass

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        pass

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        pass

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        pass

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        pass


class CmdEntity(CmdPositioner):
    def __init__(self, connection):
        pass

        

class CmdPlayer(CmdPositioner):
    def __init__(self, connection):
        pass

    def getPos(self):
        trace("player.getPos")
        return Vec3D(0,0,0)
        

    def setPos(self, *args):
        trace("player.setPos:" + str(args))
        

    def getTilePos(self):
        trace("player.getTilePos:" + str(args))
        return Vec3D(0,0,0)
        

    def setTilePos(self, *args):
        trace("setTilePos:" + str(args))

        
class CmdEvents:
    def __init__(self, connection):
        pass
        
    def clearAll(self):
        """Clear all old events"""
        trace("events.clearAll")
        

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        trace("events.pollBlockHits")
        return []


class CmdCamera:
    def __init__(self, connection):
        pass

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        pass

    def setFixed(self):
        """Set camera mode to fixed view"""
        pass

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        pass

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        pass


class Minecraft:
    def __init__(self, connection=None):
        #self.camera = CmdCamera(connection)
        #self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection)
        self.events = CmdEvents(connection)

    @staticmethod
    def create(addr=None):
        trace("create")
        return Minecraft()

    
    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        trace("getBlock:" + str(args))
        
        
    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        trace("getBlockWithData:" + str(args))


    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        trace("getBlocks:" + str(args))


    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        trace("setBlock:" + str(args))
        

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        trace("setBlocks:" + str(args))
        

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        trace("getHeight:" + str(args))
        

    #def getPlayerEntityIds(self):
    #    """Get the entity ids of the connected players => [id:int]"""
    #    trace("getPlayerEntityIds")        

    #def saveCheckpoint(self):
    #    """Save a checkpoint that can be used for restoring the world"""
    #    pass

    #def restoreCheckpoint(self):
    #    """Restore the world state to the checkpoint"""
    #    pass

    def postToChat(self, msg):
        """Post a message to the game chat"""
        trace("postToChat:" + str(msg))
        

    #def setting(self, setting, status):
    #    """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
    #    pass

# END


