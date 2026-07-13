import sys


def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()
        
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(f"{command[5:]}")
        elif command.startswith("type "):
            print(f"{command[5:]} is a shell built-in command")
        else:
            print (f"{command}: command not found")
if __name__ == "__main__":
    main()
