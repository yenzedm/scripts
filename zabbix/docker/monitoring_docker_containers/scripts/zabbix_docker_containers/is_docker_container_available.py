#!/usr/bin/python3
import sys
import os


def status(name):
    containers = []
    with os.popen(f'docker ps --filter ancestor={name}') as file:
        for i in file:
            containers.append(i.split())
    if len(containers) >= 2:
        with os.popen('docker inspect --format {{.State.Running}} ' + containers[1][0]) as file:
            result = file.read().strip()
            if result == 'true':
                print(1)
                return 1
            else:
                print(0)
                return 0
    else:
        print(0)
        return 0


if __name__ == '__main__':
    try:
        name = sys.argv[1]
        status(name)
    except:
        print(0)
