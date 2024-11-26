#!C:\Users\admin\AppData\Local\Programs\Python\Python39\python.exe
import psutil
import json
from time import sleep


def get_list_idme_processes():
    # Get a list of all running processes
    idme_processes_tmp = []

    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            # Filter only 'runner' processes
            if 'runner' in proc.info['name']:
                process_name = proc.info['name'] + '_' + str(proc.info['pid']) 
                idme_processes_tmp.append({'{#NAME}': process_name})
                sleep(0.1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Convert the list of processes to JSON format
    return json.dumps(idme_processes_tmp, ensure_ascii=False)


if __name__ == '__main__':
    print(get_list_idme_processes())