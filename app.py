# Importamos librerias
import os

from subprocess import call
os.system("sudo apt update")
os.system("sudo apt-get install -y python3-pip")

call(["sudo","git","clone","https://github.com/mitre/caldera.git", "--recursive", "--branch", "4.0.0-beta"])
os.system("sudo apt update")
os.system("sudo apt install -y upx")


os.system("wget https://dl.google.com/go/go1.17.7.linux-amd64.tar.gz") 

os.system("sudo tar -C /usr/local -xzf go1.17.7.linux-amd64.tar.gz")
os.chdir('/home/vagrant')
with open(".bashrc", "a") as a_file:
  a_file.write("\n")
  a_file.write("export PATH=$PATH:/usr/local/go/bin")

os.system("source ~/.bashrc")
os.chdir('caldera')
os.system("sudo su")
os.system("pip3 install -r requirements.txt")

