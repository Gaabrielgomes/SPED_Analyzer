import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox


def verify_requirements():
    # Check Python
    if not _check_python():
        messagebox.showerror(
            "Erro", "Python não está instalado ou não está no PATH.")
        return False

    # Check/install pip
    if not _check_pip():
        messagebox.showinfo("Aviso", "Pip não encontrado. Instalando...")
        if not _install_pip():
            messagebox.showerror("Erro", "Falha ao instalar o pip.")
            return False

    # Check/update libraries
    libraries = _load_requirements()
    if libraries is None:
        messagebox.showwarning(
            "Aviso", "Arquivo 'requirements.txt' não encontrado ou vazio.")
        return False
    elif not _check_and_install_libs(libraries):
        messagebox.showerror(
            "Erro", "Falha ao instalar/atualizar bibliotecas.")
        return False

    return True


def _check_python():
    try:
        subprocess.check_call([sys.executable, "--version"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def _check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def _install_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                              "--upgrade", "pip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def _load_requirements():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")

        if not os.path.exists(requirements_path):
            return None

        with open(requirements_path, "r") as file:
            libraries = [line.strip() for line in file if line.strip()
                         and not line.startswith("#")]
        return libraries
    except:
        return None


def _check_and_install_libs(libraries):
    if len(libraries) == 0:
        return True
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] +
                              libraries, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    if verify_requirements() == False:
        messagebox.showerror("Erro", "Consulte o desenvolvedor.", parent=root)
        sys.exit(1)
    else:
        messagebox.showinfo("Sucesso", "Todos os requisitos estão atendidos.", parent=root)
    root.destroy()