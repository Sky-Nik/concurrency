#!/usr/bin/env python -i

from time import sleep
from multiprocessing import Process, Value


def f(x):
    return not x


def g(x):
    while True:
        sleep(1)


def proc(function, argument, global_result, count_finished):
    local_result = function(argument)
    with global_result.get_lock():
        global_result.value |= local_result
    with count_finished.get_lock():
        count_finished.value += 1


def main(f, g, x):
    expression = f"{f.__name__}({x}) || {g.__name__}({x})"

    global_result = Value('b', False)
    count_finished = Value('i', 0)

    first_process = Process(target=proc, args=(f, x, global_result, count_finished))
    second_process = Process(target=proc, args=(g, x, global_result, count_finished))

    first_process.start()
    second_process.start()

    stop = True

    while not global_result.value and count_finished.value < 2:
        first_process.join(timeout=1)
        second_process.join(timeout=1)
        if stop:
            mode = input("Continue [c], break [B] or run nonstop? [r] ")
            if mode == 'B':
                print(f"{expression} is undefined")
                first_process.terminate()
                second_process.terminate()
                return
            if mode == 'r':
                stop = False
    else:
        print(f"{expression} == {global_result.value}")
        first_process.terminate()
        second_process.terminate()


if __name__ == '__main__':
    x = bool(int(input("Enter x [0/1]: ")))
    main(f, g, x)
