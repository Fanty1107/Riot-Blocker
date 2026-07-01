import winreg
import sys
import ctypes

targetExe = "RiotClient.exe"
redirectExe = 'cmd.exe /k echo [BLOQUEIO]!'
key_path = rf"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{TARGET_EXE}"

def admin_permission():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_exe():
    if not admin_permission():
        print("Erro: Execute como administrador")
        return
    try:
        chave = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)        

