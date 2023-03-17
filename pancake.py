import subprocess
import sys
from subprocess import Popen

def testing():
    x: str = "discord"
    process = Popen(['flatpak', 'list', '--app'], stdout = subprocess.PIPE)
    output_bytes = subprocess.check_output(['grep', x], stdin = process.stdout)
    process.wait()
    output = output_bytes.decode('utf-8')

    options = []
    #for i in output:
            #options.append()

    print(output)

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("error: no operation specified (use -h for help)")
    elif "-v" in args or "--version" in args:
        print("pancake 0.0.1")
    elif "-h" in args or "--help" in args:
        print("usage:  pancake <option> [...]\n"
              + "options:\n"
              + "\t-h --help\n"
              + "\t-V --version\n"
              + "\t-s --install\t[packages]\n"
              + "\t-r --remove\t[packages]\n"
              + "\t-u --update\t\n"
              + "\t-q --query\t<package>\n"
              )

