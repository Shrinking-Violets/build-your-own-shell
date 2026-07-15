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
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
    return None        
def main():
    builtin_comm = {"exit", "echo", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()

        if not command:
            continue
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(f"{command[5:]}")

        elif command.startswith("type "):
            cmd = command[5:]

            if cmd in builtin_comm:
                print(f"{cmd} is a shell builtin")
            else:
                path = get_path(cmd)
                if path:
                    print(f"{cmd} is {path}")
                    
                else:
                    print(f"{command[5:]} not found")
        elif command.startswith("pwd"):
            curr_dir = os.getcwd()
            print(f"{curr_dir}")
        elif command.startswith("cd"):
            if os.path.isdir(command[3:]):
               cd_change = os.chdir(command[3:])
               print(f"{cd_change}")
            else:
                print(f"{command[3:]}: No such file or directory")
        else:
            parts = command.split()
            program = parts[0]
            args = parts[1:]
            path = get_path(program)
            
            if path:
                subprocess.run([program] + args, executable=path)
            else:
                print(f"{command}: command not found")
if __name__ == "__main__":
    main()
