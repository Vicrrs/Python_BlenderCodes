import subprocess
import sys

def install_blender_package(package):
    python_exe = "C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python\\bin\\python.exe"
    subprocess.check_call([python_exe, "-m", "pip", "install", package])

install_blender_package("bpycv")
