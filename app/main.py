import sys
import os

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        builtin_comm = {"exit", "echo", "type"}

        if command.startswith("echo "):
            print(f"{command[5:]} is a shell builtin")
        elif command.startswith("type "):
            if command[5:] in builtin_comm:
                print(f"{command[5:]} is a shell builtin")
            else:
                path_env = os.environ.get("PATH", "")

                dictionaries = path_env.split(os.pathsep)
                ext = [""]

                if sys.platform == "win32":
                    ext = [".exe", ".bat", ".cmd", ""]
                found = False

                for dictionary in dictionaries:
                    for ex in ext:
                        full_path = os.path.join(dictionary, f"{command[5:]}{ex}")

                        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                            print(f"{command[5:]} is {full_path}")
                            found = True
                if not found:
                    print(f"{command[5:]} not found")

        elif command.startswith("exit "):
            exit(0)
if __name__ == "__main__":
    main()
