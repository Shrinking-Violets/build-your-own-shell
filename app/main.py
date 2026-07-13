import sys
buildin_fun = ["echo", "exit", "type"]
exit = exit(0)
echo = lambda x: print()
type = lambda x: print()
def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()

        if command == "exit":
            break
        elif command.startswith("echo "):
            print(f"{command[5:]}")
        elif command.startswith("type echo"):
            print(f"{command[5:]} is a shell builtin")
        elif command.startswith("type exit"):
            print(f"{command[5:]} is a shell builtin")
        elif command.startswith("type type"):
            print(f"{command[5:]} is a shell builtin")
        elif command.startswith("type "):
            print(f"{command[5:]} not found")    
        else:
            print (f"{command}: command not found")
if __name__ == "__main__":
    main()
