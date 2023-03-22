import subprocess
import sys
import os
from subprocess import Popen
from functools import reduce


config: dict[str, str] = dict()

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


def pancake_generate_symlinks():
    global config

    results: list[str] = []
    output_bytes = subprocess.check_output(['flatpak', 'list', '--app'])
    output = output_bytes.decode('utf-8')
    if len(output) == 0:
        print("No apps installed")
        return
    splits = output.splitlines()
    for line in splits:
        results.append(line.split("\t")[1])
    print(f"Installed apps: {results}")
    print("TODO, feature not implemented yet")
    return

    #for pair in config.items():


def pancake_read_config():
    global config

    home = os.path.expanduser('~')
    try:
        with open(home + "/.config/pancake/symlinks.ini", "r") as file:
            raw_config = file.readlines()
        splitted = filter(lambda x: len(x) == 2 and x[0][0] != '#', map(lambda x: x.strip().split(), raw_config))
        config = {x[0]: x[1] for x in splitted}
    except IOError:
        pass


def pancake_write_config():
    global config

    configpath = os.path.expanduser('~') + "/.config/pancake"
    os.makedirs(configpath, exist_ok = True)

    names: list[str] = []
    for pair in config.items():
        names.append(pair[0])
    max_length_raw: int = reduce(lambda accum, item: len(item) if isinstance(accum, int) and len(item) > accum else accum, names, 0)
    max_length = max_length_raw + 4 + (4 - max_length_raw % 4) #length of a tab is 4 in a file

    with open(configpath + "/symlinks.ini", "w+") as file:
        file.write("# This file is automatically formatted.\n# Any manual formatting will be ignored.\n\n")
        for pair in config.items():
            num_tabs = max_length - len(pair[0])
            file.write(pair[0] + " "*num_tabs + pair[1] + "\n")
        file.write("\n")


def flatpak_install(install: list[str]):
    global config

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
    max_length_raw: int = reduce(lambda accum, item: len(item) if isinstance(accum, int) and len(item) > accum else accum, install, 0)
    max_length = max_length_raw // 8 + 2 #length of a tab is 8 in the terminal

    # print the results and prompt
    header = f"Package ({len(results)})"
    num_tabs = max_length - (len(header) // 8)
    print(header + '\t'*num_tabs + "Application ID\n")
    for i in range(len(install)):
        name = install[i]
        num_tabs = max_length - (len(name) // 8)
        print(name + '\t'*num_tabs + results[i])
    print() #newline

    user_input = input("Proceed with installation? [Y/n] ")
    if user_input.lower().strip() != "y":
        return

    # install
    process = Popen(['flatpak', 'install'] + results)
    process.wait()

    user_input = input("\nCreate symlinks? [Y/n] ")
    if user_input.lower().strip() != "y":
        return

    # update config
    for i in range(len(results)):
        config[install[i]] = results[i]
    pancake_write_config()

    # create symlinks
    for i in range(len(results)):
        process = Popen('echo "flatpak run ' + results[i] + '" | sudo tee /usr/local/bin/' + install[i], shell = True)
        process.wait()
        process1 = Popen('sudo chmod +x /usr/local/bin/' + install[i], shell = True)
        process1.wait()

    print("\nPlease restart your session or open a new terminal for changes to take place")


def flatpak_remove(remove: list[str]):
    global config

    results: list[str] = [] 

    # find all mappings
    for i in range(len(remove)):
        if remove[i] in config:
            results.append(config[remove[i]])
        else:
            print(f"error: no matches found for '{remove[i]}'")
            return
    max_length_raw: int = reduce(lambda accum, item: len(item) if isinstance(accum, int) and len(item) > accum else accum, remove, 0)
    max_length = max_length_raw // 8 + 2 #length of a tab is 8 in the terminal

    # print the results and prompt
    header = f"Package ({len(results)})"
    num_tabs = max_length - (len(header) // 8)
    print(header + '\t'*num_tabs + "Application ID\n")
    for i in range(len(remove)):
        name = remove[i]
        num_tabs = max_length - (len(name) // 8)
        print(name + '\t'*num_tabs + results[i])
    print() #newline

    user_input = input(":: Do you want to remove these packages? [Y/n] ")
    if user_input.lower().strip() != "y":
        return

    # uninstall
    process = Popen(['flatpak', 'uninstall'] + results)
    process.wait()

    user_input = input("\nRemove symlinks? [Y/n] ")
    if user_input.lower().strip() != "y":
        return

    # update config
    for i in range(len(results)):
        config.pop(remove[i])
    pancake_write_config()

    # remove symlinks
    for i in range(len(results)):
        contents_raw = subprocess.check_output(['cat', '/usr/local/bin/' + remove[i]])
        contents: str = contents_raw.decode('utf-8').strip()
        if contents == "flatpak run " + results[i]:
            process = Popen('sudo rm /usr/local/bin/' + remove[i], shell = True)
            process.wait()
            print(f"Removed symlink for '{remove[i]}'")
        else:
            print(f"error: contents of '{remove[i]}' were:\n{contents}\n===END===")

    print("\nPlease restart your session or open a new terminal for changes to take place")


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

    pancake_read_config()
    pancake_write_config()

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
    if symlinks:
        pancake_generate_symlinks()
    if query:
        flatpak_query(inputs[0])
    elif install:
        flatpak_install(inputs)
    elif remove:
        flatpak_remove(inputs)

        
if __name__ == "__main__":
    main()

