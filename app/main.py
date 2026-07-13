import sys


def main():
    for i in range(100):
        sys.stdout.write("$ ")
        pass
        command = input()
        print (f"{command}: command not found")
        if command == "exit":
            exit(0)
if __name__ == "__main__":
    main()
