#!/usr/bin/env python -i

from time import sleep
from multiprocessing import Process, Value


def f(x):
    return not x


def g(x):
    while True:
        sleep(1)


def target(function, argument, global_result, count_finished):
    local_result = function(argument)

    with global_result.get_lock():
        global_result.value |= local_result

    with count_finished.get_lock():
        count_finished.value += 1


def main(functions, argument):
    expression = " || ".join(f"{function.__name__}({argument})" for function in functions)

    global_result = Value('b', False)
    count_finished = Value('i', 0)

    processes = [Process(target=target, args=(function, argument, global_result, count_finished)) for function in functions]

    for process in processes:
        process.start()

    stop = True

    while not global_result.value and count_finished.value < len(processes):
        for process in processes:
            process.join(timeout=1)

        if stop:
            mode = input("Continue [c], break [B] or run nonstop? [r] ")

            if mode == 'B':
                print(f"{expression} is undefined")

                for process in processes:
                    process.terminate()
                return

            if mode == 'r':
                stop = False
    else:
        print(f"{expression} == {global_result.value}")

        for process in processes:
            process.terminate()


if __name__ == '__main__':
    argument = bool(int(input("Enter argument [0/1]: ")))
    main([f, g], argument)
