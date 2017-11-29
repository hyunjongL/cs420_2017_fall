import environment

'''
int main(){                     0
    int i;                      1
    int counter;                2
    counter = 0;                3
    for(i = 0; i < 5; i++){     4
        counter = counter + i;  5
    }                           6
}                               7

    what to do when encountered a for loop
    0. 처음 들어왔을 때는 첫번째 statement 실행하고
    1. for루프에 들어왔음을 어디 적어둔다.
    2. 브래킷 다음 줄부터 쭉 실행
    3. 닫는 브래킷 만나면, 바로 루프의 줄 실행해보리기
    4. 일단 이 루프 안에 들어있다면 처음거 실행 안하고, 두번쨰 statement만 확인하면 될듯
    5. 확인해보고 맞으면 세번째 statement실행
    6. 확인해봤는데 틀리면, 브래킷의 다음 줄 넘겨줌 ㅇㅈ? ㅇㅇㅈ
'''

def run_simple():
    loop_in = False
    env = environment.environment(-1)

    env.dec_variable('i', 'int')
    env.dec_variable('counter', 'int')
    env.set_variable('counter', 0)

    while(True):
        if not loop_in:
            env.set_variable('i', 0)
            loop_in = True
        else:
            env.set_variable('i', env.get_variable('i') + 1)
        if not (env.get_variable('i') < 5):
            break
        env.set_variable('counter', env.get_variable('counter') + env.get_variable('i'))
    # met bracket -> jump to loop start
    '''
    if not loop_in:
        env.set_variable('i', 0)
    else:
        env.set_variable('i', env.get_variable('i') + 1)
    env.set_variable('counter', env.get_variable('counter') + env.get_variable('i'))


    if not loop_in:
        env.set_variable('i', 0)
    else:
        env.set_variable('i', env.get_variable('i') + 1)
    env.set_variable('counter', env.get_variable('counter') + env.get_variable('i'))

    if not loop_in:
        env.set_variable('i', 0)
    else:
        env.set_variable('i', env.get_variable('i') + 1)
    env.set_variable('counter', env.get_variable('counter') + env.get_variable('i'))

    if not loop_in:
        env.set_variable('i', 0)
    else:
        env.set_variable('i', env.get_variable('i') + 1)
    env.set_variable('counter', env.get_variable('counter') + env.get_variable('i'))
    '''
    loop_in = False




    print(env)
    # return here
    env.trace_name('counter')
    env.trace_name('i')
    env.return_func(0)

    print('\n' + str(env))


if __name__ == '__main__':
    run_simple()
