import sys


def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()
        
        if command == (type "exit", type "echo", type "type"):
            print(f"{command[5:]} is a shell builtin")
        elif command == "exit":
            break
        elif command.startswith("echo "):
            print(f"{command[5:]}")
        elif command.startswith("type "):
            print(f"{command[5:]} not found")    
        else:
            print (f"{command}: command not found")
if __name__ == "__main__":
    main()
