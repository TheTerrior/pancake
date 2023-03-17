import subprocess
from subprocess import Popen

x: str = "discord"
process = Popen(['flatpak', 'list', '--app'], stdout = subprocess.PIPE)
output_bytes = subprocess.check_output(['grep', x], stdin = process.stdout)
process.wait()
output = output_bytes.decode('utf-8')

options = []
#for i in output:
    #options.append()

print(output)
