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
    is_double_quote = False
    i = 0
    while i < len(command):
        ch = command[i]

        if ch == '\\':
            if not is_single_quote and not is_double_quote:
                if i + 1 < len(command):
                    current += command[i + 1]
                    i += 2
                    continue
            elif is_double_quote:
                if i + 1 < len(command):
                    next_ch = command[i + 1]
                    if next_ch in ['\\', '"', '$', '`']:
                        current += next_ch
                        i += 2
                        continue
        if is_single_quote:
            if ch == "'":
                is_single_quote = False
            else:
                current += ch
            i += 1
            continue
        if is_double_quote:
            if ch == '"':
                is_double_quote = False
            else:
                current += ch
            i += 1
            continue
        if ch == "'":
            is_single_quote = True
        elif ch == '"':
            is_double_quote = True
        elif ch == " ":
            if current:
                args.append(current)  
                current = ""
    
        else:
            current += ch
        i += 1
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
        
        idx = -1
        if ">" in args:
            idx = args.index(">")
        elif "1>" in args:
            idx = args.index("1>")

        filename = None
        if idx != -1:
            filename = args[idx + 1]
            args = args[:idx]

        cmd = args[0]

        if cmd == "exit":
            break
        elif cmd == "echo":
            output = " ".join(args[1:])

            if filename:
                with open(filename, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)

        elif cmd == "type":
                if len(args) == 1:
                    print(f"{cmd} is a shell builtin")
                else:
                    target = args[1]

                    if target in builtin_comm:
                        print(f"{target} is a shell builtin")
                    else:
                        path = get_path(target)
                        if path:
                            print(f"{target} is {path}")
                        else:
                            print(f"{target} not found")
        elif cmd == "pwd":
            curr_dir = os.getcwd()
            if filename:
                with open(filename, "w") as f:
                    f.write(curr_dir + "\n")
            else:
                print(curr_dir)
        elif cmd == "cd" and args[1] == "~":
            home = os.getenv('HOME')
            os.chdir(home)    
        elif cmd == "cd":
            cd_dir = args[1]
            if os.path.isdir(cd_dir):
               cd_change = os.chdir(cd_dir)
            else:
                print(f"{cmd}: {args[1]}: No such file or directory")
        else:
            
            program = args[0]
            argu = args[1:]
            path = get_path(program)
            
            if filename:
                with open(filename, "w") as f:
                    subprocess.run([program] + argu, executable=path, stdout=f)
            else:
                subprocess.run([program] + argu, executable=path)
if __name__ == "__main__":
    main()
