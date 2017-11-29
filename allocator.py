# 4 byte for int, float
# 4 byte for char also
# so, allocating 4 bytes in a time would be plausible


def bitmap(size):
    bits = int(size/4)
    result = list()
    for i in range(bits):
        result.append(0)
    return result


class allocator:
    def __init__(self, size, start=0):
        self.start = start
        self.bitmap = bitmap(size)
        self.max = size
        self.curr = start

    def allocate(self, size):
        if self.curr + size > self.max + self.start:
            raise Exception("cannot allocate, not enough space")
        pointer = self.curr
        while self.curr < pointer + size:
            if self.bitmap[int((self.curr - self.start)/4)] == 1:
                print('already taken')
                return -1
            self.bitmap[int((self.curr - self.start)/4)] = 1
            self.curr += 4
        return pointer

    def deallocate(self, pointer, size):
        curr = pointer
        while(curr < pointer + size):
            if self.bitmap[int((curr - self.start)/4)] == 0:
                raise Exception("Cannot deallocate not allocated address")
                return -1
            self.bitmap[int((curr - self.start)/4)] = 0
            curr += 4
        self.slide_cursor()
        return 1

    def show_bitmap(self):
        print('Memory Status: ', end='')
        for i in range(len(self.bitmap)):
            print(self.bitmap[i], end='')
        print()

    def slide_cursor(self):
        while self.bitmap[int((self.curr - self.start)/4)] == 0:
            self.curr -= 4
            if self.curr == self.start:
                return


class dummy:
    def __init__(self, addr, size):
        self.addr = addr
        self.addrstr = str.format('0x{:08x}', addr)
        self.size = size


def test(k, max, man):
    names = list()
    counter = 0
    for i in range(int(max/8)):
        try:
            t = man.allocate(k)
            if t == -1:
                exit()
            names.append(dummy(t, k))
        except:
            if len(names) == int(max/k):
                print('success allocating memory')
                break
            else:
                print('Failed to allocate')

    man.show_bitmap()
    for i in names:
        print(i.addrstr)
        counter += man.deallocate(i.addr, i.size)
    if counter == int(max/8):
        print('success deallocating')
    else:
        print('failed to deallocate')
    man.show_bitmap()

if __name__ == '__main__':
    man = allocator(1000, 8172)
    test(12, 120, man)
    test(4, 120, man)
