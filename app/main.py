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
    args = []
    current = ""
    is_single_quote = False
    for ch in command:
        if ch == "'":
            is_single_quote = not is_single_quote
        elif is_single_quote:
            current += ch
        elif ch == " ":
            if current:
                args.append(current)  
                current = ""
        else:
            current += ch
    if current:
        args.append(current)

    return args

def main():
    builtin_comm = {"exit", "echo", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        args = parse_command(command)
        cmd = args
        if not cmd:
            continue
        cmd = args[0]

        if cmd == "exit":
            break
        elif cmd == "echo":
            print(*args[1:])

        elif cmd == "type":
            if cmd in builtin_comm:
                print(f"{cmd} is a shell builtin")
            else:
                path = get_path(args[1])
                if path:
                    print((args[0]) (args[1:]))
    
                else:
                    print(f"{cmd} not found")
        elif cmd == "pwd":
            curr_dir = os.getcwd()
            print(f"{curr_dir}")
        elif command == "cd ~":
            home = os.getenv('HOME')
            os.chdir(home)    
        elif cmd == "cd":
            cd_dir = args[1]
            if os.path.isdir(cd_dir):
               cd_change = os.chdir(cd_dir)
            else:
                print(f"{cmd}: {args[1]} No such file or directory")
        else:
            
            program = args[0]
            argu = args[1:]
            path = get_path(program)
            
            if path:
                subprocess.run([program] + argu, executable=path)
            else:
                print(f"{command}: command not found")
if __name__ == "__main__":
    main()
