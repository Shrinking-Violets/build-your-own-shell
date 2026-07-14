import sys
import os
import subprocess

def get_path(command):
    path_env = os.environ.get("PATH", "")

    dictionaries = path_env.split(os.pathsep)
    ext = [""]

    if sys.platform == "win32":
        ext = [".exe", ".bat", ".cmd", ""]
    found = False
    for dictionary in dictionaries:
        for ex in ext:
            full_path = os.path.join(dictionary, f"{command}{ex}")
            return full_path
def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        builtin_comm = {"exit", "echo", "type"}
       
        if command.startswith("echo "):
            print(f"{command[5:]}")
        elif command.startswith("type "):
            if command[5:] in builtin_comm:
                print(f"{command[5:]} is a shell builtin")
            else:
                path = get_path(command[5:])
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    print(f"{command[5:]} is {path}")
                    
                else:
                    print(f"{command[5:]} not found")

        elif command == "exit":
            break
        elif command == (""):

            path = command.split()
            args = get_path(path)
            if os.path.isfile(path) and os.access(path, os.X_OK):
                 subprocess.run([path] + args)
                 
            else:
               print(f"{command[5:]} not found") 
        else:
            print(f"{command}: command not found")
if __name__ == "__main__":
    main()
