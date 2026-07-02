import winreg
import sys
import ctypes

target_exe = "DiscordSetup.exe"
redirect_exe = 'cmd.exe /k echo [BLOQUEIO]!'
key_path = rf"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{target_exe}"

def admin_permission():
    try:
        // verifica se o script está sendo executado com privilégios de administrador
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_exe():
    if not admin_permission():
        print("Erro: Execute como administrador")
        return
    try:
        // cria a chave de registro para bloquear o executável
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) 

        // define o valor "Debugger" para redirecionar a execução do executável bloqueado
        winreg.SetValueEx(key, "Debugger", 0, winreg.REG_SZ, redirect_exe)
        
        // fecha a chave de registro
        winreg.CloseKey(key)

        print(f"Bloqueio de {target_exe} criado com sucesso!")    
    except Exception as e:
        print(f"Erro ao criar o bloqueio: {e}")

def unblock_exe():
    if not admin_permission():
        print("Erro: Execute como administrador")
        return
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        print(f"Bloqueio de {target_exe} removido com sucesso!")
    except FileNotFoundError:
        print(f"Erro: Nenhum bloqueio encontrado para {target_exe}.")
    except Exception as e:
        print(f"Erro ao remover o bloqueio: {e}")

if __name__ == "__main__":
    block_exe()
    input("Pressione Enter para remover o bloqueio...")
    unblock_exe()        


