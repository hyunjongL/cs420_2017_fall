import sys

input_name = sys.argv[1]
input_file = open(input_name, 'r')
input_txt = input_file.read()
output_txt = ''
operators = ['*', '/', '+', '-']

#Basic functions to figure out if a character is a number, letter or an operator
def is_letter(x):
    if x >= 'a' and x <= 'z':
        return True
    if x >= 'A' and x <= 'Z':
        return True
    return False

def is_number(x):
    if x >= '0' and x <= '9':
        return True
    return False

def is_operator(x):
    if x in operators:
        return True
    return False

class Tree():   # Class Tree
                # It has left, right and data.
    def __init__(self, x):
        self.left = None
        self.right = None
        self.data = x

    def set_right(self, x):
        self.right = x

    def set_left(self, x):
        self.left = x

    def set_data(self, x):
        self.data = x

    def empty(self):
        if self.left == None and self.right == None:
            return True
        return False

    def rightmost(self):
        if self.right == None:
            return self
        else:
            return self.right.rightmost()

def preorder_trav(root):    #traverses a tree in preorder way
    result = root.data
    if root.left != None:
        result += preorder_trav(root.left)
        result += preorder_trav(root.right)
    return result


def make_tree(nodes):       #makes a tree based on the given nodes
    state = 1
    pos = 1
    max_len = len(nodes)
    if max_len == 0:
        return -1
    top = Tree(nodes[0])
    while(pos < max_len):
        if state == 0:      # num or var
            if is_operator(nodes[pos]):
                return -1
            else :
                new = Tree(nodes[pos])
                top.rightmost().set_right(new)
                pos += 1
            state += 1
        elif state == 1:
            if is_operator(nodes[pos]):
                if nodes[pos] == '*' or nodes[pos] == '/':
                    temp = top.rightmost().data
                    top.rightmost().set_data(nodes[pos])
                    top.rightmost().set_left(Tree(temp))
                    pos += 1
                else :
                    new = Tree(nodes[pos])
                    new.set_left(top)
                    top = new
                    pos += 1
                state -= 1
            else :
                return -1
    return top

def check_line(line):   #checks if a list of nodes has correct syntax
    state = 0
    for i in line:
        if state == 0 and (not is_operator(i)):
            state += 1
            continue
        elif state == 1 and is_operator(i):
            state -= 1
            continue
        else:
            return False
    if state == 1:
        return True
    else :
        return False

def parse_nodes(nodes): #returns a preorder traversed result of a tree without making a tree
                        #currently not used
    newnodes = list()
    pos = 0
    max_len = len(nodes)
    while(pos < max_len):
        if nodes[pos] == '*' or nodes[pos] == '/':
            temp = nodes[pos] + newnodes.pop() + nodes[pos+1]
            newnodes.append(temp)
            pos += 2
        else :
            newnodes.append(nodes[pos])
            pos += 1
    finalnode = ''
    pos = 0
    max_len = len(newnodes)
    while(pos < max_len):
        if newnodes[pos] == '+' or newnodes[pos] == '-':
            finalnode = newnodes[pos] + finalnode + newnodes[pos+1]
            pos += 2
        else :
            finalnode = newnodes[pos]
            pos += 1
    return finalnode

# Returns a parsed line of code
def parse_line_to_nodes(line):
    nodes = list()
    pos = 0
    max_len = len(line)
    while(pos < max_len):
        if line[pos] == ' ':
            pos += 1
        else :
            if is_letter(line[pos]):
                nodes.append(line[pos])
                pos += 1
                continue
            elif is_number(line[pos]):
                number = line[pos]
                pos += 1
                while(pos < max_len and is_number(line[pos])):
                    number += line[pos]
                    pos += 1
                nodes.append(number)
            elif is_operator(line[pos]):
                nodes.append(line[pos])
                pos += 1
                continue
            else:
                return 'incorrect syntax'
    if(not check_line(nodes)):
        return 'incorrect syntax'
    #return parse_nodes(nodes)
    return nodes


def parse_line(line):
    nodes = parse_line_to_nodes(line)
    if nodes == 'incorrect syntax':
        return 'incorrect syntax'
    return preorder_trav(make_tree(parse_line_to_nodes(line)))



for line in input_txt.split('\n'):
    if(line == ''):
        continue
    output_txt += parse_line(line)
    output_txt += '\n'


input_file.close()
output_file = open('output.txt', 'w')
output_file.write(output_txt)
output_file.close()
