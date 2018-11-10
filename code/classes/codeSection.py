class codeSection(object):
    """A section of assembly code, demarcated from the others in a program
    with a parent section that this code was called from or, in the case of main, nothing.
    This should be useful for diagrammatically representing switch and if/else statements as well as function calls


    Attributes are the name of the section, the start offset in the asm file, the length and the parent code section
    methods include get methods for all attributes, a set method for length (everything else determined at creation) and an export method for creating a data structure

    Perhaps add a hashing method for fingerprinting to avoid duplicate code sections: if hash in hashes then increment counter.
    """
    def __init__(self, name = 'main', offset = 0, length = 0, parent = None):
        self.name = name
        self.offset = offset
        self.length = length
        self.parent = None
        
    def getName(self):
        return self.name

    def getOffset(self):
        return self.offset

    def getLength(self):
        return self.length

    def getParent(self):
        return self.parent

    def setLength(self, length):
        self.length = length

    def __repr__(self):
        return "<<< codeSection {0}\tstart:{1}\tend:{1}+{2}>>>\n".format(self.name, self.offset, self.offset+self.length)
        
    def export():
        #code to output class as data structure goes here
        pass
