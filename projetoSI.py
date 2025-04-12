# Arthur de Oliveira e Leonardo Stall

import json
from getpass import getpass
import pprint

def menuPrincipal():
    while True:
        print("Bem-vindo ao sistema de login e cadastro!\n")
        # Entrada de login
        usuario = input("Digite seu usuário: ").strip()
        senha = getpass("Digite a sua senha: ").strip()
        
        if verificar_senha_usuario(usuario, senha):
            print_autorizacoes(usuario) # Se o login for bem-sucedido, verifica autorização
            break  # Sai do loop se a autorização for bem-sucedida
        else:
            print("Tentativa de login falhou. Tente novamente.\n")
            
# Funcao para teste!!!!!            
def print_autorizacoes(usuario):
    try:
        with open("base_autorizacoes.json", "r") as arquivo_json:
            autorizacoes = json.load(arquivo_json)  # Carrega os dados de autorização

            # Verifica se o usuário tem permissão
            usuario_encontrado = next((u for u in autorizacoes if u["nome_usuario"] == usuario), None)
            if usuario_encontrado:
                #printa as informções json do usuario["permissoes"]
                pprint.pprint(usuario_encontrado["permissoes"])  # Usuário encontrado e autorizado
            else:
                print("Usuário não autorizado.\n")
    
    except FileNotFoundError:
        print("\nErro: O arquivo 'base_autorizacao.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\nErro: O arquivo 'base_autorizacao.json' está corrompido.")
    

def verificar_senha_usuario(usuario, senha):
        try:
            with open("base_usuarios.json", "r") as arquivo_json:
                usuarios = json.load(arquivo_json)  # Carrega os usuários do arquivo JSON

                # Verifica se o usuário e a senha correspondem
                usuario_encontrado = next((u for u in usuarios if u["nome_usuario"] == usuario), None)
                if usuario_encontrado:
                    if usuario_encontrado["senha"] == senha:
                        print("Login realizado com sucesso!")
                        return True
                    else:
                        print("Senha incorreta.\n")
                        return False
                else:
                    print("Usuário não encontrado.\n")
                    return False
        except FileNotFoundError:
            print("\nErro: O arquivo 'base_usuarios.json' não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print("\nErro: O arquivo 'base_usuarios.json' está corrompido.")
            return False

menuPrincipal()