import sys

input_name = sys.argv[1]
print(input_name)

input_file = open(input_name, 'r')
input_txt = input_file.read()
output_txt = ''
operators = ['*', '/', '+', '-']

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

def check_line(line):
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

def parse_nodes(nodes):
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
def parse_line2(line):
    nodes = list()
    pos = 0
    max_len = len(line)
    print(max_len)
    while(pos < max_len):
        if line[pos] == ' ':
            if (pos == 0) or (pos == max_len - 1):
                pos += 1
                continue
            else :
                if is_operator(line[pos-1]) or is_operator(line[pos+1]):
                    if is_operator(line[pos-1]) and is_operator(line[pos+1]):
                        return 'incorrect syntax'
                    else:
                        pos += 1
                        continue
                else :
                    return 'incorrect syntax'
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
    return parse_nodes(nodes)


print(is_letter('a'))

for line in input_txt.split('\n'):
    if(line == ''):
        continue
    output_txt += parse_line2(line)
    output_txt += '\n'


input_file.close()
output_file = open('output.txt', 'w')
output_file.write(output_txt)
output_file.close()
