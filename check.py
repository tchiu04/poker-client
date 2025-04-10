import os
from config import OUTPUT_DIR_CONTAINER

def main():
    if os.path.exists(OUTPUT_DIR_CONTAINER) and os.path.isfile(OUTPUT_DIR_CONTAINER):
        with open(OUTPUT_DIR_CONTAINER, 'r') as file:
            content = file.readlines()
        if len(content) > 0:
            print(int(content[0].strip()))
        else:
            print("No result")
    else:
        print("No result")


if __name__ == "__main__":
    main()