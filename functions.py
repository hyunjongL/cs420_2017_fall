import allocator

DEBUG = False
max_mem_size = 10000
variable_address_start = 0x10000000
man = None


def man_init(size, start):
    global man
    man = allocator.allocator(size, start)


class function:
    type = 'N/A'
    value = 0

    def __init__(self, name, type,
                 line=0, parameters=[]):
        self.name = name
        # return type
        self.type = type
        self.line = 0
        self.parameters = parameters
        self.num = len(parameters)

    def __str__(self):
        return self.prototype + ' at line ' + str(self.line)


def test():
    a = function('sum', 'int', parameters=[('int', 'x'), ('int', 'y')])
    print(a)


if __name__ == '__main__':
    test()
