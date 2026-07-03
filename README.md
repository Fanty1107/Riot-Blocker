# Riot Network Blocker

Uma ferramenta com interface gráfica desenvolvida em Python para bloquear e desbloquear rapidamente o acesso à internet de qualquer aplicativo (.exe). 

Este projeto foi criado com o objetivo principal de bloquear jogos competitivos (como League of Legends ou Valorant) para foco e produtividade, utilizando uma abordagem 100% segura contra sistemas anti-cheat de nivel de kernel (como o Riot Vanguard). Em vez de manipular processos ou a memoria do jogo, a ferramenta atua diretamente no Firewall do Windows.

## Download

Para baixar a versão compilada e pronta para uso (sem necessidade de instalar o Python), acesse o link abaixo:

[Baixar a versão mais recente (.exe)](https://github.com/Fanty1107/Riot-Blocker/releases/latest)

## Por que usar este metodo?
Tentativas de bloquear executaveis de jogos utilizando manipulacao do registro do Windows (como "Image File Execution Options") ou fechamento forcado de processos podem ser interpretadas por sistemas anti-cheat modernos como injeção ou software malicioso, resultando em banimento permanente de conta ou hardware (HWID). 

Este script utiliza comandos nativos de rede (`netsh`) para criar regras de saida no Firewall do Windows. O jogo abrira normalmente, mas nao conseguira se comunicar com os servidores, retornando apenas um erro de conexao sem levantar suspeitas do anti-cheat.

## Funcionalidades
* Bloqueio e desbloqueio instantaneo via regras de Firewall.
* Funciona com qualquer arquivo .exe que dependa da internet (Steam, navegadores, jogos, discord, etc).
* Auto-elevação de privilegios: solicita automaticamente permissao de Administrador ao ser aberto.
* Interface grafica limpa e moderna utilizando CustomTkinter.
* Persistencia: salva automaticamente o ultimo caminho do executavel escolhido para usos futuros.
* Execucao silenciosa: sem telas pretas do prompt de comando (console flash) durante a aplicacao das regras.

## Pre-requisitos (Para rodar o codigo fonte)
Certifique-se de ter o Python instalado no seu sistema.

Instale a biblioteca necessaria:
```bash
pip install customtkinter
```
## Notas Importantes
Windows Defender (SmartScreen)
Ao enviar o arquivo .exe compilado para outros computadores, o Windows exibira um aviso azul do "Windows Protect Your PC" (SmartScreen). Isso ocorre porque o executavel foi gerado localmente e nao possui uma assinatura digital comercial. Para abrir, clique em "Mais informacoes" e depois em "Executar assim mesmo".

## .exe não dependentes de internet
Esta ferramenta corta exclusivamente a comunicacao de rede externa. Se voce bloquear um aplicativo que nao precisa de internet para funcionar (como o Bloco de Notas ou um emulador offline), ele continuara abrindo e funcionando normalmente.

## Aviso Legal
Este projeto foi desenvolvido com fins educacionais e de produtividade pessoal. Nao me responsabilizo por regras de firewall aplicadas incorretamente a processos criticos do sistema operacional.
