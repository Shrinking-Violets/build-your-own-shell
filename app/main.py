import sys


def main():
    for i in range(100):
        sys.stdout.write("$ ")
        pass
        command = input()
        
        if command == "exit":
            exit(0)
        elif command.startswith("echo "):
            print(f"{command[5:]}\n")
            break
        else:
            print (f"{command}: command not found")
if __name__ == "__main__":
    main()
