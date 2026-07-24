import sys
import os
import subprocess
import readline
import glob

def get_path(command):
    path_env = os.environ.get("PATH", "")

    dictionaries = path_env.split(os.pathsep)
    ext = [""]

    if sys.platform == "win32":
        ext = [".exe", ".bat", ".cmd", ""]
    
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
def print_error(message, stderr_filename, append = False):
    mode = "a" if append else "w"
    if stderr_filename:
        with open(stderr_filename, mode) as f:
            print(message, file=f)
    else:
        print(message, file=sys.stderr)
def print_output(message, stdout_filename, append = False):
    mode = "a" if append else "w"
    if stdout_filename:
        with open(stdout_filename, mode) as f:
            print(message, file=f)
    else:
        print(message)
def create_stderr_file(stderr_filename, append = False):
    if stderr_filename:
        mode = "a" if append else "w"
        open(stderr_filename, mode).close()
#def list_completer(text, state):
    #command = ["echo ", "exit "]
    #options = [cmd for cmd in command if cmd.startswith(text)]
    #if state < len(options):
     #   return options[state]
    #else:
     #   return None
#readline.set_completer(list_completer)
#readline.parse_and_bind("tab: complete")
def path_completer(text, state):
    path_env = os.environ.get("PATH", "")
    directories = path_env.split(os.pathsep)
    command = ["echo ", "exit "]
    matches = set()

    for cmd in command:
        if cmd.startswith(text):
            matches.add(cmd)

    for directory in directories:
        if not os.path.isdir(directory):
            continue

        for file in os.listdir(directory):
            if file.startswith(text):
                full_path = os.path.join(directory, file)

                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    matches.add(file)
    matches = sorted(matches)
    if state < len(matches):
        match = matches[state]
        return match + " "
    else:
        return None

readline.set_completer(path_completer)
readline.parse_and_bind("tab: complete")

def main():
    builtin_comm = {"exit", "echo", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        args = parse_command(command)
        if not args:
            continue

        cmd = args[0]
        if not cmd:
            continue
        stdout_idx = -1
        stderr_idx = -1
        stdout_filename = None
        stderr_filename = None
        append_stdout = False
        append_stderr = False
        if ">" in args:
            stdout_idx = args.index(">")
        elif "1>" in args:
            stdout_idx = args.index("1>")
        if "2>>" in args:
            stderr_idx = args.index("2>>")
            append_stderr = True
        elif "2>" in args:
            stderr_idx = args.index("2>")
        if  ">>" in args :
            stdout_idx = args.index(">>")
            append_stdout = True         
        elif "1>>" in args:
            stdout_idx = args.index("1>>")
            append_stdout = True
        
        if stdout_idx != -1:
            stdout_filename = args[stdout_idx + 1]
            
        if stderr_idx != -1:
            stderr_filename = args[stderr_idx +1]
            
        for idx in sorted(
            [i for i in [stdout_idx, stderr_idx] if i != -1],
            reverse=True,
        ):
            del args[idx:idx+2]
       

        if cmd == "exit":
            break
        elif cmd == "echo":
            output = " ".join(args[1:])
            create_stderr_file(stderr_filename, append_stderr)
            print_output(output, stdout_filename, append_stdout)
            
        elif cmd == "type":
                create_stderr_file(stderr_filename, append_stderr)
                if len(args) == 1:
                    print(f"{cmd} is a shell builtin")
                else:
                    target = args[1]

                    if target in builtin_comm:
                        print_output(f"{target} is a shell builtin", stdout_filename)
                    elif (path := get_path(target)):
                        print_output(f"{target} is {path}", stdout_filename)
                    else:
                        print_output(f"{target} not found", stdout_filename)
        elif cmd == "pwd":
            curr_dir = os.getcwd()
            create_stderr_file(stderr_filename, append_stderr)
            print_output(curr_dir, stdout_filename, append_stdout)
            
        elif cmd == "cd":
            message = "cd: missing argument"
            if len(args) < 2:
                print_error(f"{program}: command not found", stderr_filename, append_stderr)    
            elif args[1] == "~":
                home = os.getenv('HOME')
                os.chdir(home)
            else:
                cd_dir = args[1]
                message = f"cd: {args[1]}: No such file or directory"
                if os.path.isdir(cd_dir):
                    os.chdir(cd_dir)
                else:
                    print_error(message, stderr_filename, append_stderr)
        else:
            
            program = args[0]
            argu = args[1:]
            path = get_path(program)

            if path is None:
                print_error(f"{program}: command not found", stderr_filename, append_stderr)
            else:
                mode = "a" if append_stdout else "w"
                stderr_mode = "a" if append_stderr else "w"
                stdout_file = open(stdout_filename, mode) if stdout_filename else None
                stderr_file = open(stderr_filename, stderr_mode) if stderr_filename else None

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