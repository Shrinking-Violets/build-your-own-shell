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
def parse_command(command):
    
    if args[0] == "echo":


def main():
    builtin_comm = {"exit", "echo", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        args = parse_command(command)
        cmds = args[0]

        if not cmds:
            continue
        if cmds == "exit":
            break
        elif cmds == "echo ":
            print(f"cmds")

        elif cmds == "type ":
            if cmds in builtin_comm:
                print(f"{cmds} is a shell builtin")
            else:
                path = get_path(cmds)
                if path:
                    print(f"{cmds} is {path}")
                    
                else:
                    print(f"{cmds} not found")
        elif cmds == "pwd"):
            curr_dir = os.getcwd()
            print(f"{curr_dir}")
        elif command == "cd ~":
            home = os.getenv('HOME')
            os.chdir(home)    
        elif cmds == "cd":
            cd_dir = cmds
            if os.path.isdir(cd_dir):
               cd_change = os.chdir(cd_dir)
            else:
                print(f"{cmds}: No such file or directory")
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
