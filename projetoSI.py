# Arthur de Oliveira e Leonardo Stall

import json
from getpass import getpass
import pprint

def menuPrincipal():
    print("Bem-vindo ao sistema de login e cadastro!\n")
    print("Faça seu Login:\n")
    # Entrada de login
    usuario = input("Digite seu usuário: ").strip()        
    senha = getpass("Digite a sua senha: ").strip()
        
    while verificar_senha_usuario(usuario, senha) == False:
        usuario = input("Digite seu usuário novamente: ").strip()        
        senha = getpass("Digite a sua senha novamente: ").strip()
        
        if verificar_senha_usuario(usuario, senha): # Se o login for bem-sucedido, verifica autorização
            break  # Sai do loop se a autorização for bem-sucedida
        else:
            print("Tentativa de login falhou. Tente novamente.\n")
    opcoesMenu(usuario)       

def opcoesMenu(usuario):
    with open("base_autorizacoes.json", "r") as arquivo_json:
        autorizacoes = json.load(arquivo_json)
        # Verifica se o usuário tem permissão
        usuario_encontrado = next((u for u in autorizacoes if u["nome_usuario"] == usuario), None)
        if usuario_encontrado:
            # Exibe as permissões do usuário
            print(f"Permissões do usuário {usuario}:")
            opcoes_disponiveis = {}  
            n = 1 
            for permissao, opcao in usuario_encontrado["permissoes"].items():
                if opcao: 
                    print(f"{n}- {permissao}")
                    opcoes_disponiveis[str(n)] = permissao 
                    n += 1
            recurso = input("Escolha uma opção: ").strip()  
            while recurso not in opcoes_disponiveis:
                print("Opção inválida. Tente novamente.")
                recurso = input("Escolha uma opção novamente: ").strip()
            if recurso in opcoes_disponiveis:
                permissao_escolhida = opcoes_disponiveis[recurso]
                if permissao_escolhida == "Cadastrar_usuario":
                    cadastrar_usuario()
                elif permissao_escolhida == "Editar_usuario":
                    editar_usuario()
                elif permissao_escolhida == "Excluir_usuario":
                    excluir_usuario()
                elif permissao_escolhida == "Listar_usuarios":
                    listar_usuarios()
                else:
                    print("Permissão não implementada.\n")
            else:
                print("Opção inválida. Tente novamente.\n")        

def cadastrar_usuario():
    usuario = input("Digite o nome do novo usuário: ").strip()
    #
    with open("base_autorizacoes.json", "r") as arquivo_json:
        usuarios = json.load(arquivo_json)
        novo_usuario_autorizacao = {
            "nome_usuario": usuario,
            "permissoes": {
                "Cadastrar_usuario": False,
                "Editar_usuario": False,
                "Excluir_usuario": False,
                "Listar_usuarios": False
            }
        }
        novo_usuario = {
            "nome_usuario": usuario,
            "senha": "senha_nova"
        }   

        usuarios.append(novo_usuario_autorizacao)
        with open("base_autorizacoes.json", "w") as arquivo_json:
            json.dump(usuarios, arquivo_json, indent=4)
    
    with open("base_usuarios.json", "r") as arquivo_json:
        usuarios = json.load(arquivo_json)
        novo_usuario = {
                "nome_usuario": usuario,
                "senha": "senha_nova"
            }   

        usuarios.append(novo_usuario)
        with open("base_usuarios.json", "w") as arquivo_json:
            json.dump(usuarios, arquivo_json, indent=4)
    print(f"Usuário {usuario} cadastrado com sucesso!\n")

def editar_usuario():
    print("Funcao editar_usuario() ainda não implementada.")

def excluir_usuario():
    print("Funcao excluir_usuario() ainda não implementada.")

def listar_usuarios():
    print("Funcao listar_usuarios() ainda não implementada.")  
          
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

