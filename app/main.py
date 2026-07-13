import sys


def main():
    sys.stdout.write("$ ")
    pass

command = {input()}
error = print ({command: "command not found"})
if __name__ == "__main__":
    main()
