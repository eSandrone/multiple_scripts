import time
import subprocess

print("Sending message to teams")
comando = "touch file.txt"
process = subprocess.Popen(comando.split(), shell=True)
comando = "touch file_2.txt"
process = subprocess.run(comando.split(), shell=True)
#output, error = process.communicate()
