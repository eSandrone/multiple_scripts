import time
import subprocess

print("Sending message to teams")
comando = "ps aux"
process = subprocess.Popen(comando.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
