import variable

max_mem_size = 1000
# variable_address_start = 0
if max_mem_size != 10000:
    variable.man = variable.allocator.allocator(max_mem_size)
    variable.DEBUG = False

man = variable.man_init(max_mem_size)


class environment:
    def __init__(self, ret=0, parent=None):
        self.parent = parent
        self.names = {}
        self.ret = ret

    def set_return_to_name(self, name):
        obj, _ = self.parent.find_name(name)
        self.ret = obj.addr

    def find_name(self, name):
        for i in self.names:
            if self.names[i].name == name:
                return self.names[i], self
        if self.parent is not None:
            return self.parent.find_name(name)
        else:
            return None, None

    def find_address(self, addr):
        for i in self.names:
            if self.names[i].has_address(addr):
                return self.names[i], self
        if self.parent is not None:
            return self.parent.find_address(addr)
        else:
            return None, None

    def dec_variable(self, name, type, num=0):
        new_var = variable.variable(name, type, num=num)
        if name in self.names:
            new_var.parent = self.names[name]
        self.names[name] = new_var

    def set_variable(self, name, value, num=None, line=0):
        parent, env = self.find_name(name)
        if parent is None:
            raise Exception("Variable " + name + " has not been declared")
        if num is None:
            new_var = parent.set_variable(value, line)
            # new_var = variable.variable(name, parent.type, value=value, parent=parent)
        else:
            new_var = parent.set_variable(value, line)
            # new_var = variable.variable(name, parent.type, value=value, num=num, parent=parent)
        env.names[name] = new_var

    def set_address(self, addr, value, line=0):
        parent, env = self.find_address(addr)
        if parent is None:
            raise Exception("Cannot find variable at address " + str.format('0x{:08x}', addr))
        new_var = parent.set_variable(value, line)
        # new_var = variable.variable(parent.name, parent.type, value=value, parent=parent)
        env.names[parent.name] = new_var

    def new_env(self):
        next_scope = environment(parent=self)
        return next_scope

    def return_func(self, value):
        if self.parent is None:
            print("Program finished with exit code " + str(value))
            return
        self.parent.set_address(self.ret, value)
        for i in self.names:
            man.deallocate(self.names[i].addr, self.names[i].size)
        return self.parent

    def __str__(self):
        result = ''
        result += ('return address: ' + str.format('0x{:08x}', self.ret))
        result += ('\nsaved variables:\n')
        for i in self.names:
            i = self.names[i]
            result += ('\t' + i.name + ' ' + i.addrstr + ' ' + str(i.value) + '\n')
        if self.parent is None:
            return result
        return result + str(self.parent)

    def trace_name(self, name):
        obj, _ = self.find_name(name)
        obj.trace()


def test():
    a = variable.variable('a', 'int')
    new_env = environment(a.addr)
    new_env.dec_variable('b', 'int')
    new_env.set_variable('b', 4)
    b, env = new_env.find_name('b')
    another_env = environment(b.addr, new_env)
    another_env.dec_variable('c', 'float')
    another_env.dec_variable('b', 'int')
    another_env.set_address(b.addr, 8)
    another_env.set_variable('b', 4)
    env = another_env.return_func(7)

    print(env)
    man.show_bitmap()


if __name__ == '__main__':
    test()
