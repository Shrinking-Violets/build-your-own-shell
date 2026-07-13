import sys


def main():
    sys.stdout.write("$ ")


command = input()
error = print (f"{command}: command not found")
if __name__ == "__main__":
    main()
