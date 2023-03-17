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
    print(sys.argv)

