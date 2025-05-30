# Arthur de Oliveira e Leonardo Stall
# Bem vindo professor Pedro! Para o senhor cadastrar novos usuários, 
# basta usar o USUÁRIO: Pedro e a SENHA: admin.


import json
from getpass import getpass
import pprint
    
def MenuPrincipal():
    print("Bem-vindo ao sistema de login!\n")
    print("Faça seu Login!")

    while True:
        usuario = input("Digite seu usuário: ").strip()        
        senha = getpass("Digite a sua senha: ").strip()

        if VerificarSenhaUsuario(usuario, senha): 
            opcoesMenu(usuario) 
        else:
            print("⚠️  Tentativa de login falhou. Tente novamente.\n")

def opcoesMenu(usuario):
    with open("base_autorizacoes.json", "r") as arquivo_json:
        autorizacoes = json.load(arquivo_json)

    usuario_encontrado = next((u for u in autorizacoes if u["nome_usuario"] == usuario), None)

    if not usuario_encontrado:
        print(f"⚠️  Usuário '{usuario}' não foi encontrado na base de autorizações. Retornando ao menu principal.")
        MenuPrincipal()

    while True:
        print(f"\nPermissões do usuário {usuario}:")
        opcoes_disponiveis = {}  
        n = 1 

        for permissao, opcao in usuario_encontrado["permissoes"].items():
            if opcao: 
                permissao_formatada = permissao.replace('_', ' ')
                print(f"| {n} - {permissao_formatada}")
                opcoes_disponiveis[str(n)] = permissao 
                n += 1

        print(f"| {n} - Sair")
        opcoes_disponiveis[str(n)] = "Sair"

        recurso = input("Escolha uma opção: ").strip()  
        while recurso not in opcoes_disponiveis:
            print("❗ Erro: Opção inválida. Tente novamente.")
            recurso = input("Escolha uma opção novamente: ").strip()

        if recurso in opcoes_disponiveis:
            permissao_escolhida = opcoes_disponiveis[recurso]

            if permissao_escolhida == "Sair":
                print("Saindo da conta.\n")
                return
            elif permissao_escolhida == "Cadastrar_usuarios":
                CadastrarNovosUsuarios_Escrever()
            elif permissao_escolhida == "Editar_usuarios":
                EditarUsuarios_EscreverAtualziar(usuario)
            elif permissao_escolhida == "Excluir_usuarios":
                ExcluirUsuarios_Apagar(usuario)
            elif permissao_escolhida == "Visualizar_usuarios":
                ListarUsuarios_Ler(usuario)
            elif permissao_escolhida == "Visualizar_autorizacoes_usuarios":
                ListarAutorizacoesUsuarios_Ler()
            else:
                print("Permissão não implementada.\n")
        else:
            print("❗ Erro: Opção inválida. Tente novamente.\n")
            
def CadastrarNovosUsuarios_Escrever():
    try:
        usuario = input("\nDigite o nome do novo usuário: ").strip()
        
        with open("base_usuarios.json", "r") as arquivo_json:
            usuarios = json.load(arquivo_json)

        with open("base_autorizacoes.json", "r") as arquivo_json:
            autorizacoes = json.load(arquivo_json)


        # ve se o usuario está ja cadstrado na base de usuarios
        if any(u["nome_usuario"] == usuario for u in usuarios):
            print(f"❗ Erro: Usuário '{usuario}' já existe na base de usuários.")
            return
        
        # ve se o usuario está ja cadstrado na base de autorizações
        if any(u["nome_usuario"] == usuario for u in autorizacoes):
            print(f"❗ Erro: Usuário '{usuario}' já existe na base de autorizações.")
            return
        
        novo_usuario_autorizacao = {
            "nome_usuario": usuario,
            "permissoes": {
                "Cadastrar_usuarios": False,
                "Editar_usuarios": False,
                "Excluir_usuarios": False,
                "Visualizar_usuarios": False,
                "Visualizar_autorizacoes_usuarios": False
            }
        }

        novo_usuario = {
            "nome_usuario": usuario,
            "senha": "senha_nova"
        }   

        # insere na base de usuários
        usuarios.append(novo_usuario)
        with open("base_usuarios.json", "w") as arquivo_json:
            json.dump(usuarios, arquivo_json, indent=4)

        # insere na base de autorizações
        autorizacoes.append(novo_usuario_autorizacao)
        with open("base_autorizacoes.json", "w") as arquivo_json:
            json.dump(autorizacoes, arquivo_json, indent=4)

        print(f"Usuário '{usuario}' cadastrado com sucesso!\n")

    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' está corrompido.")

def EditarUsuarios_EscreverAtualziar(usuario_atual):
    try:
        usuario_antigo = input("\nDigite o nome do usuário que deseja editar: ").strip()

        if usuario_antigo == usuario_atual:
            print("❗ Erro: Você não pode editar seu próprio usuário.")
            return
        
        with open("base_usuarios.json", "r") as arquivo_json:
            usuarios = json.load(arquivo_json)

        with open("base_autorizacoes.json", "r") as arquivo_json:
            autorizacoes = json.load(arquivo_json)

        # verifica se o usuário existe na base de usuários
        usuario_existe = any(u["nome_usuario"] == usuario_antigo for u in usuarios)

        if not usuario_existe:
            print(f"❗ Erro: Usuário '{usuario_antigo}' não encontrado na base de usuários.")
            return

        novo_usuario = input("Digite o NOVO nome para o usuário: ").strip()

        # verifica se o novo nome já existe nas bases
        if any(u["nome_usuario"] == novo_usuario for u in usuarios):
            print(f"❗ Erro: Usuário '{novo_usuario}' já existe na base de usuários.")
            return
        
        if any(u["nome_usuario"] == novo_usuario for u in autorizacoes):
            print(f"❗ Erro: Usuário '{novo_usuario}' já existe na base de autorizações.")
            return

        # atualiza na base de usuários
        for u in usuarios:
            if u["nome_usuario"] == usuario_antigo:
                u["nome_usuario"] = novo_usuario
                break

        with open("base_usuarios.json", "w") as arquivo_json:
            json.dump(usuarios, arquivo_json, indent=4)

        # atualiza na base de autorizações
        for a in autorizacoes:
            if a["nome_usuario"] == usuario_antigo:
                a["nome_usuario"] = novo_usuario
                break

        with open("base_autorizacoes.json", "w") as arquivo_json:
            json.dump(autorizacoes, arquivo_json, indent=4)

        print(f"Usuário '{usuario_antigo}' alterado para '{novo_usuario}' com sucesso!\n")

    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' está corrompido.")

def ExcluirUsuarios_Apagar(usuario_atual):
    try:
        usuario_excluir = input("\nDigite o nome do usuário que deseja excluir: ").strip()
        
        if usuario_excluir == usuario_atual:
            print("❗ Erro: Você não pode excluir seu próprio usuário.")
            return
        
        with open("base_usuarios.json", "r") as arquivo_json:
            usuarios = json.load(arquivo_json)

        with open("base_autorizacoes.json", "r") as arquivo_json:
            autorizacoes = json.load(arquivo_json)

        # verifica se o usuário existe na base usuários
        if not any(u["nome_usuario"] == usuario_excluir for u in usuarios):
            print(f"❗ Erro: Usuário '{usuario_excluir}' não encontrado na base de usuários.")
            return

        confirmacao1 = input(f"Tem certeza que deseja excluir o usuário '{usuario_excluir}'? (s/n): ").strip().lower()
        if confirmacao1 != 's':
            print("Operação de exclusão cancelada.")
            return

        confirmacao2 = input(f"Digite 'CONFIRMAR' para excluir definitivamente o usuário '{usuario_excluir}': ").strip()
        if confirmacao2 != 'CONFIRMAR':
            print("Operação de exclusão cancelada.")
            return

        # remove das bases
        usuarios = [u for u in usuarios if u["nome_usuario"] != usuario_excluir]
        with open("base_usuarios.json", "w") as arquivo_json:
            json.dump(usuarios, arquivo_json, indent=4)

        autorizacoes = [a for a in autorizacoes if a["nome_usuario"] != usuario_excluir]
        with open("base_autorizacoes.json", "w") as arquivo_json:
            json.dump(autorizacoes, arquivo_json, indent=4)

        print(f"Usuário '{usuario_excluir}' foi excluído com sucesso!\n")

    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' ou 'base_autorizacoes.json' está corrompido.")

def ListarUsuarios_Ler(usuario_atual):
    try:
        with open("base_usuarios.json", "r") as arquivo_json:
            usuarios = json.load(arquivo_json)
        
        print("\nLista de usuários:")
        print("-" * 30)
        
        for usuario in usuarios:
            nome_usuario = usuario["nome_usuario"]

            if nome_usuario == usuario_atual:
                print(f"- {nome_usuario} (usuário atual)")
            else:
                print(f"- {nome_usuario}")
        
        print("-" * 30)
        print(f"Total de usuários: {len(usuarios)}\n")

    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_usuarios.json' está corrompido.")

def ListarAutorizacoesUsuarios_Ler():
    try:
        with open("base_autorizacoes.json", "r") as arquivo_json:
            autorizacoes = json.load(arquivo_json)
        
        print("\nLista de Autorizações dos Usuários:")
        print("=" * 50)
        
        for usuario in autorizacoes:
            print(f"\nUsuário: {usuario['nome_usuario']}")
            print("-" * 30)
            print("Permissões:")
            
            for permissao, status in usuario['permissoes'].items():
                status_formatado = "Ativada" if status else "Desativada"
                print(f"  {permissao.replace('_', ' ')}: {status_formatado}")
        
        print("\n" + "=" * 50)
        print(f"\nTotal de usuários listados: {len(autorizacoes)}\n")

    except FileNotFoundError:
        print("\n❗ Erro: O arquivo 'base_autorizacao.json' não foi encontrado.")
    except json.JSONDecodeError:
        print("\n❗ Erro: O arquivo 'base_autorizacao.json' está corrompido.")

def VerificarSenhaUsuario(usuario, senha):
        try:
            with open("base_usuarios.json", "r") as arquivo_json:
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
            print("\n❗ Erro: O arquivo 'base_usuarios.json' não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print("\n❗ Erro: O arquivo 'base_usuarios.json' está corrompido.")
            return False

MenuPrincipal()