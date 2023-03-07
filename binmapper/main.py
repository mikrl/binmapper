##############################################################################
# binmapper: a program to parse disassemblies into a format useful for making into a control flow graph
# Copyright (C) 2018 Michael Lynch (mikrlynch@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
##############################################################################

"""
Purpose:
Scan through asm binaries and generate data structure to be visualised using flowchart libs
Rebuild stripped binaries
Port to C++

Author: mikrl
"""

### Imports ###
from classes.codeSection import subroutine
from subprocess import call, check_output
import re
import json
import networkx as nx


### Constants ###
FILENAME = "../binaries/loopandcall"

### Start ###
print("[*]Getting objdump output of {0}".format(FILENAME))
dump = check_output(
    ["objdump", "-d", "-j.text", FILENAME]
)  # grabs raw output from objdump with required options
print("[*]Grabbing asm of .text")
asm_lines = [
    line for line in dump.decode("utf-8").strip().split("\n") if len(line) > 0
]  # decodes to utf8 and splits based on newlines

print("[*]Getting subroutine start locations")

function_defs = [
    (lno, asm_lines[lno])
    for lno, line in enumerate(asm_lines)
    if re.match("[0-9a-f]+ ", line)
]
function_starts, function_names = [func_info for func_info in zip(*function_defs)]
function_starts = list(function_starts)
function_names = list(function_names)

function_bounds = [
    (start, stop) for start, stop in zip(function_starts, function_starts[1:] + [None])
]

re_func_name = re.compile("<.*>")
re_func_offset = re.compile("[0-9a-f]* ")

print("[*]Creating subroutine objects")
function_list = []

assert len(function_names) == len(function_bounds)


for idx, line in enumerate(function_names):
    name = re_func_name.findall(line)[0]
    hex_offset = re_func_offset.findall(line)[0][:-1]
    func_start, func_stop = function_bounds[idx]
    body = [
        line.replace(" ", "").split("\t")
        for line in asm_lines[func_start + 1 : func_stop]
    ]

    line_nos = [line[0][:-1] for line in body]
    bytecode = [line[1] for line in body]
    commands = [line[2] if len(line) == 3 else None for line in body]

    function_body = [
        {"line": line[0], "bytes": line[1], "command": line[2]}
        for line in zip(line_nos, bytecode, commands)
    ]

    assert len(line_nos) == len(bytecode) == len(commands)

    this_block = subroutine(
        name=name, offset=hex_offset, end=line_nos[-1], body=function_body
    )
    function_list.append(this_block)


print("[*]Determining relationship between subroutines")


for idx, _subroutine in enumerate(function_list):
    # neighbours = function_list[0:idx]+function_list[idx+1:]
    # neighbour_names = [neighbour.name for neighbour in neighbours]

    if len(_subroutine.getChildrenNames()) != 0:
        neighbours = function_list[0:idx] + function_list[idx + 1 :]
        neighbour_names = [neighbour.name for neighbour in neighbours]

        for child_sub in _subroutine.getChildrenNames():
            if child_sub in neighbour_names:
                child_idx = neighbour_names.index(child_sub)
                neighbours[child_idx].addParent(_subroutine)
                _subroutine.addChild(neighbours[child_idx])


# for el in function_list: print(el.export())

graph_dict = {
    name: idx
    for name, idx in enumerate(
        [_subroutine.export()["name"] for _subroutine in function_list]
    )
}
G = nx.DiGraph()
G.add_nodes_from(function_list)
for node in G.nodes:
    children = node.getChildren()
    G.add_edges_from([(node, child) for child in children])

# G.add_edge(1,2)
# G.add_edge(2,3)

################################################################################
# for idx, name in enumerate([_subroutine.export['name'] for _subroutine in function_list]):
#   graph_dict.
