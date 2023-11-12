import subprocess
import sys

def install_package_in_blender_snap(package_name):
    try:
        # Comando para abrir o shell do snap do Blender
        snap_shell_command = "snap run --shell blender"

        # Comando para instalar o pacote usando o Python do Blender
        pip_install_command = f"/snap/blender/4116/3.6/python/bin/python3.10 -m pip install {package_name}"

        # Executando o shell do snap do Blender
        snap_shell_process = subprocess.Popen(snap_shell_command, stdin=subprocess.PIPE, shell=True)

        # Executando o comando de instalação dentro do shell do snap
        snap_shell_process.stdin.write(pip_install_command.encode())
        snap_shell_process.stdin.close()

        snap_shell_process.wait()

        if snap_shell_process.returncode == 0:
            print(f"Instalação bem-sucedida: {package_name}")
        else:
            print(f"Falha na instalação: {package_name}")
    except Exception as e:
        print(f"Erro: {e}")

# Exemplo de uso
install_package_in_blender_snap("bpycv")
