#!/usr/bin/env python

from time import sleep
from multiprocessing import Process, Queue


# Function naming convention is as follows:
#   u - undefined, t - True, f - False
#   first letter = result if argument is True
#   second letter = result if argument is False


def uu(argument, processes_results_queue):
    while True:
        pass


def fu(argument, processes_results_queue):
    if argument:
        processes_results_queue.put(False)
    else:
        while True:
            pass


def uf(argument, processes_results_queue):
    if not argument:
        processes_results_queue.put(False)
    else:
        while True:
            pass


def ff(argument, processes_results_queue):
    processes_results_queue.put(False)


def tu(argument, processes_results_queue):
    if argument:
        processes_results_queue.put(True)
    else:
        while True:
            pass


def ut(argument, processes_results_queue):
    if not argument:
        processes_results_queue.put(True)
    else:
        while True:
            pass


def tt(argument, processes_results_queue):
    processes_results_queue.put(True)


def tf(argument, processes_results_queue):
    processes_results_queue.put(argument)


def ft(argument, processes_results_queue):
    processes_results_queue.put(not argument)


functions = [uu, fu, uf, ff, tu, ut, tt, tf, ft]


def main(first_function, second_function, argument):
    expression = f"{first_function.__name__}({argument}) || {second_function.__name__}({argument})"

    processes_results_queue = Queue()

    first_process = Process(target=first_function, args=(argument, processes_results_queue))
    second_process = Process(target=second_function, args=(argument, processes_results_queue))

    first_process.start()
    second_process.start()

    result = False

    stops = True

    while processes_results_queue.empty():
        first_process.join(timeout=1)
        second_process.join(timeout=1)
        if stops and processes_results_queue.empty():
            response = input("Continue [c], break [B] or run nonstop? [r] ")
            if response == 'B':
                print(f"{expression} is undefined")
                first_process.terminate()
                second_process.terminate()
                return
            if response == 'r':
                stops = False

    result |= processes_results_queue.get()

    if result:
        print(f"{expression} == {result}")
        first_process.terminate()
        second_process.terminate()
        return

    while processes_results_queue.empty():
        first_process.join(timeout=1)
        second_process.join(timeout=1)
        if stops and processes_results_queue.empty():
            response = input("Continue [c], break [B] or run nonstop? [r] ")
            if response == 'B':
                print(f"{expression} is undefined")
                first_process.terminate()
                second_process.terminate()
                return
            if response == 'r':
                stops = False

    result |= processes_results_queue.get()
    print(f"{expression} == {result}")


if __name__ == '__main__':
    # test code for all possible combinations of
    # (first_function, second_function, argument)
    for first_function in functions:
        for second_function in functions:
            for argument in (False, True):
                main(first_function, second_function, argument)
