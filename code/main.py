"""
Purpose:
Scan through asm binaries and generate data structure to be ported to flowchart libs
Port to C++

Author: mikrl
"""
from subprocess import call, check_output
import re
import json

FILENAME = "../binaries/loopandcall"

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
        return "<codeSection {0}\tstart:{1}\tend:{1}+{2}>\n".format(self.name, self.offset, 0)#self.offset+self.length)
        
    def export():
        #code to output class as data structure goes here
        pass

print("[*]Getting objdump output of {0}".format(FILENAME))
dump = check_output(["objdump", "-d",  "-j.text", FILENAME]) #grabs raw output from objdump with required options
print("[*]Grabbing asm of .text")
asm_lines = [line for line in dump.decode('utf-8').strip().split('\n') if len(line)>0] #decodes to utf8 and splits based on newlines
#print("\n".join(asm_lines))

print("[*]Getting function start locations")
function_defs =[(lno, asm_lines[lno]) for  lno, line in enumerate(asm_lines) if re.match('[0-9a-f]+ ', line)]
print(function_defs)
function_starts, function_names = [func_info for func_info in zip(*function_defs)]
function_starts = list(function_starts)
function_names = list(function_names)

function_bounds = [(start, stop) for start, stop in zip(function_starts, function_starts[1:]+[None])]

pattern = re.compile('<.*>')
pattern2 = re.compile('[0-9a-f]* ')

print("[*]Creating function_block objects")
"""
for line_no, line in function starts:
    if line_no + 1 == len(function_starts):
function_text = [line[start:finish] for line in asm_lines for finish = start for idx, start in enumerate(function_starts)         
"""
assert(len(function_names) == len(function_bounds))           
for idx, line in enumerate(function_names):
    print(line)
    
    name = pattern.findall(line)[0]
    hex_offset = pattern2.findall(line)[0][:-1]
    func_start, func_stop = function_bounds[idx]
    body = [line.replace(" ","").split('\t') for line in asm_lines[func_start+1:func_stop]]
    """
    for el in body:
        while len(el) < max([len(a) for a in body]):
            el+=[None]
    """
    print("\n".join(["\t".join(el) for el in body]))
    #breakpoint()

    #parsed_body = [{"line_no": , "bytes": , "command": ,"args":}]
    
    #print("\n".join(body)) #= [asm_lines[start:stop] for start, stop = zip(*function_bounds[idx])]
    
    #breakpoint()
    print(codeSection(name = name, offset = hex_offset))
"""
func_class = [codeSection(name = pattern.findall(line), offset=line_no) for line, line_no in function_starts]

test = [pattern.findall(line) for line in asm_lines]
"""
#json_rep = {"funcname":pass, "funcbody": {
    
#function_titles = [title for function in asm_lines 
#if re.match
#{name=
   
