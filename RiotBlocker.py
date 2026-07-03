import sys
import ctypes
import subprocess
import os
import customtkinter
from tkinter import filedialog

# 1. AUTO-ELEVAÇÃO PARA ADMINISTRADOR
# O script precisa de privilégios elevados para interagir com o Firewall do Windows.
def admin_permission():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not admin_permission():
    # Executa novamente o script solicitando o prompt de Administrador do Windows (UAC)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit()


# CONFIGURAÇÕES E CONSTANTES
RULE_NAME = "RiotGames_Blocker_Rule"
DEFAULT_PATH = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
CONFIG_FILE = "blocker_config.txt"
CREATE_NO_WINDOW = 0x08000000  # Flag para ocultar o piscar de janelas do CMD


# FUNÇÕES DE LOGICA DO SISTEMA
def load_target_path():
    """Carrega o caminho do ficheiro salvo na configuração ou usa o padrão da Riot."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved_path = f.read().strip()
            if os.path.exists(saved_path):
                return saved_path
    if os.path.exists(DEFAULT_PATH):
        return DEFAULT_PATH
    return ""

def save_target_path(path):
    """Guarda o caminho do executável para persistência de dados."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(path)
    except Exception as e:
        print(f"Erro ao salvar configuração: {e}")

def block_net():
    """Cria a regra de bloqueio no Firewall impedindo o acesso à rede."""
    target_path = load_target_path()
    
    # Se não houver caminho padrão válido, solicita a localização
    if not target_path:
        status_label.configure(text="Localize o ficheiro .exe da Riot...", text_color="yellow")
        target_path = filedialog.askopenfilename(
            title="Selecione o executável do jogo ou Riot Client",
            filetypes=[("Arquivos Executáveis", "*.exe")]
        )
        if not target_path:
            status_label.configure(text="Operação cancelada.", text_color="white")
            return
        save_target_path(target_path)

    target_path = os.path.normpath(target_path)

    try:
        #evitar duplicação no Firewall
        cmd_delete = f'netsh advfirewall firewall delete rule name="{RULE_NAME}"'
        subprocess.run(cmd_delete, shell=True, creationflags=CREATE_NO_WINDOW)

        #Cria a nova regra de forma invisível 
        cmd_add = f'netsh advfirewall firewall add rule name="{RULE_NAME}" dir=out action=block program="{target_path}" enable=yes'
        result = subprocess.run(cmd_add, shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)

        if result.returncode == 0:
            status_label.configure(text=f"Bloqueado com sucesso:\n{os.path.basename(target_path)}", text_color="green")
        else:
            status_label.configure(text="Erro ao aplicar regra no Firewall.", text_color="red")
    except Exception as e:
        status_label.configure(text=f"Erro: {e}", text_color="red")

def unblock_net():
    """Remove a regra do Firewall restaurando a conexão do jogo."""
    try:
        # CORREÇÃO: Executa a remoção sem piscar a janela preta
        cmd = f'netsh advfirewall firewall delete rule name="{RULE_NAME}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)

        if result.returncode == 0:
            status_label.configure(text="Bloqueio de rede removido com sucesso!", text_color="green")
        else:
            status_label.configure(text="Erro ao remover ou nenhum bloqueio ativo.", text_color="yellow")
    except Exception as e:
        status_label.configure(text=f"Erro: {e}", text_color="red")

def change_path():
    """Permite ao utilizador reconfigurar manualmente o executável alvo."""
    target_path = filedialog.askopenfilename(
        title="Selecione o executável do jogo ou Riot Client",
        filetypes=[("Arquivos Executáveis", "*.exe")]
    )
    if target_path:
        save_target_path(target_path)
        status_label.configure(text=f"Novo alvo configurado:\n{os.path.basename(target_path)}", text_color="cyan")


# INTERFACE GRÁFICA (GUI)
if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.title("Riot Blocker")
    app.geometry("450x400")
    app.grid_columnconfigure(0, weight=1)
    
    title_label = customtkinter.CTkLabel(app, text="Controlo de Acesso - Riot Games", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, padx=20, pady=25)

    # Botões de Bloqueio e Desbloqueio
    button_block = customtkinter.CTkButton(app, text="Bloquear Acesso", command=block_net)
    button_block.grid(row=1, column=0, padx=20, pady=10)

    button_unblock = customtkinter.CTkButton(app, text="Desbloquear Acesso", command=unblock_net)
    button_unblock.grid(row=2, column=0, padx=20, pady=10)

    # Botão de Configuração
    button_change = customtkinter.CTkButton(app, text="Alterar Executável Alvo", command=change_path, fg_color="#333333", hover_color="#444444")
    button_change.grid(row=3, column=0, padx=20, pady=10)

    # Label de Feedback
    status_label = customtkinter.CTkLabel(app, text="Pronto para operar.", font=("Arial", 12))
    status_label.grid(row=4, column=0, padx=20, pady=20)

    # Mostra qual o jogo/cliente configurado assim que o app abre
    current_target = load_target_path()
    if current_target:
        status_label.configure(text=f"Alvo atual: {os.path.basename(current_target)}", text_color="gray")

    button_exit = customtkinter.CTkButton(app, text="Sair", command=app.destroy, fg_color="#555555")
    button_exit.grid(row=5, column=0, padx=20, pady=10)

    app.mainloop()