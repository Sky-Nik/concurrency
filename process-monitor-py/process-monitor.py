#!/usr/bin/env python
import psutil
import time
import os

from prettytable import PrettyTable


def clear():
    if os.name == 'nt':  # win
        os.system('cls')
    else:  # mac/linux (here os.name is 'posix')
        os.system('clear')


# Battery Information
def print_battery():
    battery_table = PrettyTable()
    battery_table.title = 'Battery'
    battery_table.field_names = ['Percentage', 'Charging']
    battery_table.align = 'r'
    battery_stats = psutil.sensors_battery()
    battery_table.add_row([
        battery_stats.percent,
        battery_stats.power_plugged
    ])
    print(battery_table)


# Network Information
def print_network():
    network_table = PrettyTable()
    network_table.title = 'Network'
    network_table.field_names = ['Name', 'Status', 'Speed']
    network_table.align = 'r'
    network_table.align['Name'] = 'l'
    for network_name, network_stats in psutil.net_if_stats().items():
        network_table.add_row([
            network_name,
            'Up' if network_stats.isup else 'Down',
            network_stats.speed
        ])
    print(network_table.get_string(sortby='Speed', reversesort=True))


# Memory Information
def print_memory():
    memory_table = PrettyTable()
    memory_table.title = 'Memory, Mb'
    memory_table.field_names = ['Total', 'Used', 'Available', 'Percentage']
    memory_table.align = 'r'
    memory_stats = psutil.virtual_memory()
    mb = 1 << 20
    memory_table.add_row([
        memory_stats.total // mb,
        memory_stats.used // mb,
        memory_stats.available // mb,
        memory_stats.percent
    ])
    print(memory_table)


ACTIVE_PIDS = {}


# Process Information
def print_process():
    global ACTIVE_PIDS
    process_table = PrettyTable()
    process_table.title = 'Processes'
    process_table.field_names = ['PID', 'Name', 'Status', 'CPU', 'Memory', 'Threads']
    process_table.align = 'r'
    process_table.align['Name'] = 'l'
    NEW_PIDS = {}
    for process_id in psutil.pids():
        try:
            process = psutil.Process(process_id)
            if process.memory_percent() >= 1:  # no 'background' processes
                NEW_PIDS[process_id] = process.name()
                process_table.add_row([
                    f'{process_id}',
                    process.name(),
                    process.status(),
                    f'{process.cpu_percent(interval=0.1):.2f}%',
                    f'{process.memory_percent():.2f}%',
                    process.num_threads(),
                ])
        except Exception as e:  # the process finished before we could print its information
            pass
    print(process_table.get_string(sort_key=lambda row: float(row[5][:-1]), sortby='Memory', reversesort=True))
    for process_id in NEW_PIDS.keys() - ACTIVE_PIDS.keys():
        print(f'New process {process_id}, {NEW_PIDS[process_id]}')
    for process_id in ACTIVE_PIDS.keys() - NEW_PIDS.keys():
        print(f'Process {process_id}, {ACTIVE_PIDS[process_id]} has finished')
    ACTIVE_PIDS = NEW_PIDS


if __name__ == '__main__':
    while True:
        # clear()
        for print_function in (print_battery, print_network, print_memory, print_process):
            print_function()
            print()
        time.sleep(5)  # seconds
