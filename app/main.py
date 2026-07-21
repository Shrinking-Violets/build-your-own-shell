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
        stdout_idx = -1
        stderr_idx = -1
        stdout_filename = None
        stderr_filename = None

        if ">" in args:
            stdout_idx = args.index(">")
        elif "1>" in args:
            stdout_idx = args.index("1>")
        if "2>" in args:
            stderr_idx = args.index("2>")

        if stdout_idx != -1:
            stdout_filename = args[stdout_idx + 1]
            
        if stderr_idx != -1:
            stderr_filename = args[stderr_idx +1]
            
        for idx in sorted(
            [i for i in [stdout_idx, stderr_idx] if i != -1],
            reverse=True,
        ):
            del args[idx:idx+2]
        cmd = args[0]

        if cmd == "exit":
            break
        elif cmd == "echo":
            output = " ".join(args[1:])
            if stderr_filename:
                open(stderr_filename, "w").close()
            if stdout_filename:
                with open(stdout_filename, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif cmd == "type":
                if stderr_filename:
                    open(stderr_filename, "w").close()
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
            if stderr_filename:
                open(stderr_filename, "w").close()
            if stdout_filename:
                with open(stdout_filename, "w") as f:
                    f.write(curr_dir + "\n")
            else:
                print(curr_dir)
        elif cmd == "cd":
            message = "cd: missing argument"
            if len(args) < 2:
                if stderr_filename:
                    with open(stderr_filename, "w") as f:
                        print(message, file=f)
                else:
                    print(message, file=sys.stderr)
            elif args[1] == "~":
                home = os.getenv('HOME')
                os.chdir(home)
            else:
                cd_dir = args[1]
                message = f"cd: {args[1]}: No such file or directory"
                if os.path.isdir(cd_dir):
                    os.chdir(cd_dir)
                else:
                    if stderr_filename:
                        with open(stderr_filename, "w") as f:
                            print(message, file=f)
                    else:
                        print(message, file=sys.stderr)
        else:
            
            program = args[0]
            argu = args[1:]
            path = get_path(program)

            if path is None:
                message = f"{program}: command not found"

                if stderr_filename:
                    with open(stderr_filename, "w") as f:
                        print(message, file=f)
                else:
                    print(message, file=sys.stderr)
            else:
                stdout_file = open(stdout_filename, "w") if stdout_filename else None
                stderr_file = open(stderr_filename, "w") if stderr_filename else None

                try:
                    subprocess.run(
                        [program] + argu,
                        executable=path,
                        stdout=stdout_file,
                        stderr=stderr_file,
                    )
                finally:
                    if stdout_file:
                        stdout_file.close()
                    if stderr_file:
                        stderr_file.close()
if __name__ == "__main__":
    main()