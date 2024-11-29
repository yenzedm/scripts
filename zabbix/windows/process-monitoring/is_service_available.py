#!C:\Users\admin\AppData\Local\Programs\Python\Python39\python.exe
import psutil
import sys


def status(name):
    for proc in psutil.process_iter(['name', 'status']):
        try:
            if name == proc.info['name']:
                return 1 if proc.info['status'] == 'running' else 0
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return 0

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print(0)
        else:
            service_name = sys.argv[1]
            print(status(service_name))
    except Exception as e:
        print(0)