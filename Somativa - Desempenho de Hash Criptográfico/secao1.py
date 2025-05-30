# Arthur de Oliveira e Leonardo Stall

import json
from getpass import getpass
import hashlib
import os
    
def MenuPrincipal():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Autenticar Usuário")
        print("2. Cadastrar Usuário")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            if AutenticarUsuario():
                break
        elif opcao == "2":
            CadastrarUsuario()
        elif opcao == "3":
            print("Saindo do programa...")
            break
        else:
            print("⚠️  Opção inválida. Tente novamente.")
    
def AutenticarUsuario():
    usuario = ""
    while len(usuario) != 4:  
        usuario = input("Digite seu usuário (4 caracteres): ").strip()
        if len(usuario) != 4:
            print("⚠️  O usuário deve ter 4 caracteres. Tente novamente.")  
    
    while len(senha) != 4:      
        senha = getpass("Digite a sua senha (4 caracteres): ").strip()
        if len(senha) != 4:
            print("⚠️  A senha deve ter 4 caracteres. Tente novamente.")

    if VerificarSenhaUsuario(usuario, senha): 
        print("\n Login realizado com sucesso!")
        print("Você está logado como:", usuario)
        return True
    else:
        print("⚠️  Tentativa de login falhou. Tente novamente.\n")
        return False

def VerificarSenhaUsuario(usuario, senha):
        try:
            with open("base_usuarios2.json", "r") as arquivo_json:
                usuarios = json.load(arquivo_json)  # Carrega os usuários do arquivo JSON

                # Verifica se o usuário e a senha correspondem
                usuario_encontrado = next((u for u in usuarios if u["nome_usuario"] == usuario), None)
                if usuario_encontrado:
                    if usuario_encontrado["senha"] == senha:
                        print("Login realizado com sucesso!")
                        return True
                    
                print("\n ⚠️  Usuário ou senha incorretos.") # retorno ambíguo para evitar possiveis casos de 'tenattiva e erro '
                return False
        except FileNotFoundError:
            print("\n❗ Erro: O arquivo 'base_usuarios2.json' não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print("\n❗ Erro: O arquivo 'base_usuarios2.json' está corrompido.")
            return False

def CadastrarUsuario():
    usuario = input("Digite seu usuário: ").strip()        
    senha = getpass("Digite a sua senha: ").strip()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Caminho correto baseado na mesma pasta do script
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "base_usuarios2.json")

    try:
        with open(caminho_arquivo, "r") as arquivo_json:
            usuarios = json.load(arquivo_json)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = []

    if any(u["nome_usuario"] == usuario for u in usuarios):
        print(f"! Erro: Usuário {usuario} já existe na base de dados.\n")
        return

    novo_usuario = {
        "nome_usuario": usuario,
        "senha": senha_hash
    }

    usuarios.append(novo_usuario)

    with open(caminho_arquivo, "w") as arquivo_json:
        json.dump(usuarios, arquivo_json, indent=4)

    print(f"Usuário {usuario} cadastrado com sucesso!\n")

MenuPrincipal()