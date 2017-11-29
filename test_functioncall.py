import environment
import functions

'''
int sum(int x, int y){  0
    return x + y;       1
}                       2
int main(){             3
    int a;              4
    int b;              5
    a = 7;              6
    b = 15;             7
    int c;              8
    c = sum(a, b)       9
    printf("%d", c);    10
    return 0;           11
}                       12

1. declare a
2. decalre b
3. assign a
4. assign b
5. declare c
6. jump to 1
7. execute 1
8. assign c
9. print c
10. return 0
'''

def run_simple():
    functionl = list()
    sum_ = functions.function('sum', 'int', parameters=[('int', 'x'), ('int', 'y')], line=1)
    functionl.append(sum_)
    env = environment.environment(-1)

    env.dec_variable('a', 'int')
    env.dec_variable('b', 'int')
    env.set_variable('a', 7)
    env.set_variable('b', 15)
    env.dec_variable('c', 'int')

    # function call
    env = env.new_env()
    param1, _ = env.find_name('a')
    param2, _ = env.find_name('b')
    env.dec_variable('a', 'int')
    env.dec_variable('b', 'int')
    env.set_variable('a', param1.value)
    env.set_variable('b', param2.value)
    env.set_return_to_name('c')
    print(env)
    # return here
    env = env.return_func(env.find_name('a')[0].value + env.find_name('b')[0].value)

    print(env.find_name('c')[0].value)
    env.set_variable('c', 8)
    env.set_variable('c', 9)
    env.trace_name('c')
    env.return_func(0)

    print('\n' + str(env))


if __name__ == '__main__':
    run_simple()
