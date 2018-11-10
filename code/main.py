"""
Purpose:
Scan through asm binaries and generate data structure to be ported to flowchart libs
Port to C++

Author: mikrl
"""
from classes.codeSection import codeSection
from subprocess import call, check_output
import re
import json

FILENAME = "../binaries/loopandcall"



print("[*]Getting objdump output of {0}".format(FILENAME))
dump = check_output(["objdump", "-d",  "-j.text", FILENAME]) #grabs raw output from objdump with required options
print("[*]Grabbing asm of .text")
asm_lines = [line for line in dump.decode('utf-8').strip().split('\n') if len(line)>0] #decodes to utf8 and splits based on newlines
#print("\n".join(asm_lines))

print("[*]Getting function start locations")
function_defs =[(lno, asm_lines[lno]) for  lno, line in enumerate(asm_lines) if re.match('[0-9a-f]+ ', line)]
#print(function_defs)
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
    #print(line)
    
    name = pattern.findall(line)[0]
    hex_offset = pattern2.findall(line)[0][:-1]
    func_start, func_stop = function_bounds[idx]
    body = [line.replace(" ","").split('\t') for line in asm_lines[func_start+1:func_stop]]

    line_nos = [line[0][:-1] for line in body]
    bytes = [line[1] for line in body]
    commands = [line[2] if len(line)==3 else None for line in body] 
    #print([el for el in zip(line_nos, bytes, commands)])
    #print(len(line_nos), len(bytes), len(commands))
    assert (len(line_nos) == len(bytes) == len(commands))
    """
    for i in range(len(line_nos)):
        print("{0}\t{1}\t{2}".format(line_nos[i], bytes[i], commands[i]))
    #breakpoint()
    """
    #print("\n".join(["\t".join(el) for el in body]))
    #breakpoint()

    #parsed_body = [{"line_no": , "bytes": , "command": ,"args":}]
    
    #print("\n".join(body)) #= [asm_lines[start:stop] for start, stop = zip(*function_bounds[idx])]
    
    #breakpoint()
    #print(name, hex_offset, line_nos[-1])
    print(codeSection(name = name, offset = hex_offset, length=line_nos[-1]))
"""
func_class = [codeSection(name = pattern.findall(line), offset=line_no) for line, line_no in function_starts]

test = [pattern.findall(line) for line in asm_lines]
"""
#json_rep = {"funcname":pass, "funcbody": {
    
#function_titles = [title for function in asm_lines 
#if re.match
#{name=
   
