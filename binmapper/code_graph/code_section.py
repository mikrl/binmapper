class executable(object):
    """Representing the executable. Add higher level functions such as rebuilding ELF table or other analysis"""

    #TODO Add support for stripped binaries using instruction analysis

    def __init__(self, body):
        self.body = body
        self.subroutines = []
        pass

    def parseSubroutines(self):
        pass

    def export(self):
        return [subroutine.export() for subroutine in self.subroutines]


class subroutine(object):
    """A section of assembly code, demarcated from the others in a program
    with a parent section that this code was called from or, in the case of main, nothing.
    This should be useful for diagrammatically representing switch and if/else statements as well as function calls


    Attributes are the name of the section, the start offset in the asm file, the length and the children code sections
    methods include get methods for all attributes, a set method for length (everything else determined at creation) and an export
    method for creating a data structure

    Perhaps add a hashing method for fingerprinting to avoid duplicate code sections: if hash in hashes then increment counter.
    """

    def __init__(self, name, offset, end, body):
        self.name = name
        self.width = len(offset)
        self.offset = int(offset, 16)
        self.length = self.calculateLength(offset, end)
        self.body = body
        self.children = []
        self.parents = []
        self.child_names = self.findChildrenNames()

    def calculateLength(self, offset, end):
        return int(end, 16) - int(offset, 16)

    def getName(self):
        return self.name

    def getOffset(self):
        return self.offset

    def getLength(self):
        return self.length

    def addParent(self, new_parent):
        self.parents.append(new_parent)

    def getParents(self):
        return self.parents

    def addChild(self, child):
        self.children.append(child)

    def addChildren(self, children):
        self.children.extend(children)

    def getChildren(self):
        return self.children

    def getChildrenNames(self):
        return self.child_names

    def findChildrenNames(self):
        import re

        call_sub = re.compile("(call)")
        sub_name = re.compile("<.*>")

        callees = [
            line
            for line in self.body
            if line["command"] is not None and call_sub.match(line["command"])
        ]

        callee_names = [
            sub_name.findall(callee["command"]) for callee in callees
        ]  # *returns a 2D list

        return [
            idx for sub in callee_names for idx in sub
        ]  # this flattens the 2D list to a 1D list

    def setLength(self, length):
        self.length = length

    def __repr__(self):  # useful representation of function object
        return (
            "<<< subroutine {0}\tstart:{1:0{3}x}\tend:{1:0{3}x}+{2:0{3}x}>>>\n".format(
                self.name, self.offset, self.length, self.width
            )
        )

    def __str__(self):
        entry = "{1:0{0}x}\t{2}:".format(self.width, self.offset, self.name)
        body = "\n".join(
            [
                "\t{0}:\t{1}\t{2}\n".format(
                    line["line"], line["bytes"], line["command"]
                )
                for line in self.body
            ]
        )
        return entry + body

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def export(self):
        jsonable_dict = {
            "name": self.name,
            "parents": self.parents,
            "children": self.children,
            "offset": self.offset,
            "length": self.length,
        }

        return jsonable_dict
