import time
import subprocess

print("Sending message to teams")
comando = "ps aux"
process = subprocess.Popen(comando.split(), shell=True)
#output, error = process.communicate()
