import time

def print_file(filename):
    with open(filename) as file:
        for line in file:
            print(line)
    file.close()

# print_file("/home/jjherskow/HUJI/nand2tetris/pathHelper/txt1")

def sum_to_n(n):
    result = 0
    for i in range(1,n+1):
        result=result+i
    print(result)

def fast_sum_to_n(n):
    print((n**2+n)/2)


def time_func(func,input):
    x = time.time()
    func(input)
    print("took  " + str(time.time() - x))

a=1000000000

time_func(fast_sum_to_n, a)
time_func(sum_to_n, a)


