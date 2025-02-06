import json
import glob
from sys import argv
import os


def merge_json(*args):
    tech = args[0]
    oswin = args[1]
    product = args[2]
    region = args[3]
    destination = args[4]
    
    files = [
        fr"{tech}",
        fr"{oswin}",
        fr"{product}",
        fr"{region}"
    ]

    for i in files:
        print(i)
        if not os.path.exists(i):
            print(f"file not foudn {i}")
            return

    merged_data = {}

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)  # Loading JSON from a file
            merged_data.update(data)  # Combining data

    # Write the combined JSON to a file
    with open(fr"{destination}", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    tech = argv[1]
    oswin = argv[2]
    product = argv[3]
    region = argv[4]
    destination = argv[5]
    merge_json(tech, oswin, product, region, destination)