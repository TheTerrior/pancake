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

def help():
    print("usage:  pancake <option> [...]\n"
          + "options:\n"
          + "\t-h --help\n"
          + "\t-V --version\n"
          + "\t-s --install\t[packages]\n"
          + "\t-r --remove\t[packages]\n"
          + "\t-u --update\t\n"
          + "\t-q --query\t<package>\n"
          )

def version():
    print("pancake 0.0.1")


def main():
    update = False
    install = False
    remove = False
    query = False

    for arg in sys.argv[1:]:
        match arg:
            case "-h" | "--help":
                help()
                return
            case "-v" | "--version":
                version()
                return
            case "--update":
                update = True
            case "--install":
                install = True
            case "--remove":
                remove = True
            case "--query":
                query = True
            case _:
                if arg[0] == "-":
                    if len(arg) == 1:
                        print("error: invalid syntax")
                        return
                    for flag in arg[1:]:
                        match flag:
                            case "h":
                                help()
                                return
                            case "v":
                                version()
                                return
                            case "u":
                                update = True
                            case "s":
                                install = True
                            case "r":
                                remove = True
                            case "q":
                                query = True
                            case _:
                                print(f"error: unknown flag '{flag}'")
                else:
                    print("error: invalid syntax")
                    return

    # ensure there are no hanging flags/options
    # ensure there are no doubled flags/options (like install and remove)





        
if __name__ == "__main__":
    main()

