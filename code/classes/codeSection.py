class function_block(object):
    """A section of assembly code, demarcated from the others in a program
    with a parent section that this code was called from or, in the case of main, nothing.
    This should be useful for diagrammatically representing switch and if/else statements as well as function calls


    Attributes are the name of the section, the start offset in the asm file, the length and the parent code section
    methods include get methods for all attributes, a set method for length (everything else determined at creation) and an export method for creating a data structure

    Perhaps add a hashing method for fingerprinting to avoid duplicate code sections: if hash in hashes then increment counter.
    """
    def __init__(self, name = 'main', offset = 0, end = 0, body = [None], parents = [None]):
        self.name = name
        self.width = len(offset)
        self.offset = int(offset, 16)
        self.length = self.calculateLength(offset, end)
        self.parents = parents

    def calculateLength(self, offset, end):
      return   int(end, 16) - int(offset, 16)
        
    def getName(self):
        return self.name

    def getOffset(self):
        return self.offset

    def getLength(self):
        return self.length

    def addParent(new_parent):
        self.parent.append(new_parent)
    
    def getParents(self):
        return self.parents

    def setLength(self, length):
        self.length = length

    def __repr__(self):
        return "<<< function_block {0}\tstart:{1:0{3}x}\tend:{1:0{3}x}+{2:0{3}x}>>>\n".format(self.name, self.offset, self.length, self.width)

    def __str__(self):
        #return string that looks like objdump output
        pass
    
    def export():
        #code to output class as data structure goes here
        pass
