#!C:\Users\admin\AppData\Local\Programs\Python\Python39\python.exe
import os
import sys

def get_folder_size(folder_path):
    """Function for calculating directory size."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
    except Exception as e:
        print(f"Error: {e}")
        return -1
    return total_size

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python folder_size.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("Error: Folder does not exist.")
        sys.exit(1)

    folder_size = get_folder_size(folder_path)
    print(folder_size)