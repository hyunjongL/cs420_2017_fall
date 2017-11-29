import allocator

DEBUG = False
max_mem_size = 10000
variable_address_start = 0x10000000
man = None


def man_init(size, start=0):
    global man
    man = allocator.allocator(size, start)
    return man


class variable:
    type = 'N/A'
    value = 0

    def __init__(self, name, type,
                 value=None, size=4, num=0, parent=None,
                 line=0, addr=-1, env=None):
        self.name = name
        self.type = type
        if value is None:
            self.value = 'N/A'
        else:
            self.value = value
        self.parent = parent
        self.size = size
        self.line = 0
        self.num = num
        self.env = env
        if addr == -1:
            try:
                self.addr = man.allocate(size)
            except:
                raise Exception("Address not able to allocate free space")
        else:
            self.addr = addr
        self.addrstr = str.format('0x{:08x}', self.addr)

    def set_variable(self, value, line=0):
        new_var = variable(self.name,
                           self.type,
                           value=value,
                           size=self.size,
                           parent=self,
                           line=line,
                           addr=self.addr)
        return new_var

    def has_address(self, addr):
        if (self.addr <= addr) and (self.addr + self.size > addr):
            return True
        return False

    def deallocate(self):
        man.deallocate(self.addr, self.size)
        if self.parent is not None:
            self.parent.deallocate()

    def trace(self):
        if self.parent is not None:
            self.parent.trace()
        print(self.value, 'at', self.line)


def test(n):
    import random
    import string
    # make n variables and deallocate them
    names = list()
    for i in range(n):
        try:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            value = random.random()
            names.append(variable(name, 'float', value=value, size=4, line=0))
        except:
            print('error allocating variables')
            return -1
    if DEBUG:
        man.show_bitmap()
    for i in names:
        try:
            if DEBUG:
                print(i.name, i.addrstr, i.value)
            i.deallocate()
        except:
            print('error deallocating variables')
            return -1
    if DEBUG:
        man.show_bitmap()
    print('test passed, ' + str(n) + ' variables allocated and deallocated')


if __name__ == '__main__':
    man_init(max_mem_size, variable_address_start)
    test(250)
