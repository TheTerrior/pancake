import subprocess
import sys
from subprocess import Popen
from functools import reduce

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


def flatpak_list_apps():
    results: list[str] = []
    output_bytes = subprocess.check_output(['flatpak', 'list', '--app'])
    output = output_bytes.decode('utf-8')
    if len(output) == 0:
        print("No apps installed")
        return
    splits = output.splitlines()
    for line in splits:
        results.append(line.split("\t")[1])
    print(results)
    return


def flatpak_install(install: list[str]):
    results: list[str] = []

    # first retrieve all queries
    for query in install:
        output_bytes = subprocess.check_output(['flatpak', 'search', query])
        line = output_bytes.decode('utf-8').splitlines()[0]
        splits = line.split('\t')
        if len(splits) != 6:
            print(f"error: no matches found for '{query}'")
            return
        results.append(splits[2])
    #for i in range(25):
    #    results.append("*" * i)
    max_length_raw: int = reduce(lambda accum, item: len(item) if isinstance(accum, int) and len(item) > accum else accum, results, 0)
    max_length = max_length_raw // 8 + 2
    #note: length of a tab is 8 in the console


    # print the results and prompt
    print(f"Package ({len(results)})\n")
    for result in results:
        num_tabs = max_length - (len(result) // 8)
        print(result + '\t' * num_tabs + 'a')
    print()
    user_input = input("Proceed with installation? [Y/n] ")
    if user_input.lower().strip() != "y":
        return


def flatpak_query(query: str):
    process = Popen(['flatpak', 'search', query])
    process.wait()


def flatpak_update():
    process = Popen(['flatpak', 'update'])
    process.wait()


def help():
    print("usage:  pancake <option> [...]\n"
          + "options:\n"
          + "\t-h --help\n"
          + "\t-V --version\n"
          + "\t-s --install\t[packages]\n"
          + "\t-r --remove\t[packages]\n"
          + "\t   --uninstall\t[packages]\n"
          + "\t-u --update\t\n"
          + "\t-q --query\t<package>\n"
          + "\t-l --symlinks\n"
          )

def version():
    print("pancake 0.0.1")


def main():
    update = False
    install = False
    remove = False
    query = False
    symlinks = False
    inputs: list[str] = []

    for arg in sys.argv[1:]:

        if (not install and remove and query) or \
                (install and not remove and query) or \
                (install and remove and not query) or \
                (install and remove and query):
            print("error: conflicting options/flags")
            return

        # handle input case
        if query and len(inputs) == 0:
            inputs.append(arg)
            continue
        elif query:
            print("error: too many queries")
            return
        if install or remove:
            inputs.append(arg)
            continue

        # handle usual case
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
            case "--remove" | "--uninstall":
                remove = True
            case "--query":
                query = True
            case "--symlinks":
                symlinks = True
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
                            case "l":
                                symlinks = True
                            case _:
                                print(f"error: unknown flag '{flag}'")
                                return
                else:
                    print("error: invalid syntax")
                    return

    # ensure there are no hanging flags/options
    # ensure there are no doubled flags/options (like install and remove)
    if (not install and remove and query) or \
            (install and not remove and query) or \
            (install and remove and not query) or \
            (install and remove and query):
        print("error: conflicting options/flags")
        return

    if (install or remove or query) and len(inputs) == 0:
        print("error: missing inputs")
        return

    if update:
        flatpak_update()
    if symlinks: #temporary
        #flatpak_symlinks()
        flatpak_list_apps()
    if query:
        flatpak_query(inputs[0])
    elif install:
        flatpak_install(inputs)
    #elif remove:
        #flatpak_uninstall(inputs)

        
if __name__ == "__main__":
    main()

