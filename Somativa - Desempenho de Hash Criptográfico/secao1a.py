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
    senha = ""  # Inicialize a variável senha antes de usá-la
    while len(usuario) != 4:
        usuario = input("Digite seu usuário (4 caracteres): ").strip()
        if len(usuario) != 4:
            print("O usuário deve ter 4 caracteres. Tente novamente.")

    while len(senha) != 4:
        senha = getpass("Digite a sua senha (4 caracteres): ").strip()
        if len(senha) != 4:
            print("A senha deve ter 4 caracteres. Tente novamente.")

    caminho_arquivo = os.path.join(os.path.dirname(__file__), "base_usuarios2.json")
    try:
        with open(caminho_arquivo, "r") as arquivo_json:
            usuarios = json.load(arquivo_json)
    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_usuarios2.json' não foi encontrado.")
        return False
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_usuarios2.json' está corrompido.")
        return False

    # Verifica se o usuário e a senha estão corretos
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    for u in usuarios:
        if u["nome_usuario"] == usuario and u["senha"] == senha_hash:
            print(f"✅ Usuário '{usuario}' autenticado com sucesso!")
            return True

    print("❌ Usuário ou senha incorretos. Tente novamente.")
    return False

def CadastrarUsuario():
    usuario = ""
    senha = ""  
    while len(usuario) != 4:
        usuario = input("Digite seu usuário (4 caracteres): ").strip()
        if len(usuario) != 4:
            print("O usuário deve ter 4 caracteres. Tente novamente.")

    while len(senha) != 4:
        senha = getpass("Digite a sua senha (4 caracteres): ").strip()
        if len(senha) != 4:
            print("A senha deve ter 4 caracteres. Tente novamente.")

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