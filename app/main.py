import sys
buildin_fun = {
   "exit": lambda _: sys.exit(0),
    "echo": lambda _args: print(f"{' '.join(_args)}", flush=True),
    "type": lambda _args: print(f"{_args[0]} is a shell builtin", flush=True)
    if _args[0] in buildin_fun
    else print(f"{_args[0]}: not found", flush=True),
}

def runCommand(cmd: str, args):
    if cmd in buildin_fun:
        buildin_fun[cmd](args)
    elif cmd:
        print(f"{cmd}: command not found")


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()  
        line = sys.stdin.readline()
        if not line:  
            break
        line = line.strip()
        if not line: 
            continue
        parts = line.split()  
        cmd, *args = parts
        runCommand(cmd, args)
if __name__ == "__main__":
    main()
