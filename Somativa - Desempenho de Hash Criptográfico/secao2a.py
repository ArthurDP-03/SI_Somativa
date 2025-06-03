# Arthur de Oliveira e Leonardo Stall
#Grupo 10
import hashlib
import time
import itertools
import string
import json
from pathlib import Path
import os

# Caminho para o arquivo JSON com os usuários e hashes
json_path = Path(f"/mnt/data/base_usuarios2.json")

# Função de força bruta para descobrir senha
def brute_force_sha256(target_hash, max_len=4, charset=string.ascii_lowercase + string.digits):
    for length in range(1, max_len + 1):
        for attempt in itertools.product(charset, repeat=length):
            candidate = ''.join(attempt)
            hash_candidate = hashlib.sha256(candidate.encode()).hexdigest()
            if hash_candidate == target_hash:
                return candidate
    return None

# Carregar os dados do arquivo
caminho_arquivo = os.path.join(os.path.dirname(__file__), "base_usuarios2.json")

with open(caminho_arquivo, "r") as file:
    usuarios = json.load(file)

# Processar cada usuário
resultados = []
total_start = time.time()

for user in usuarios:
    nome = user["nome_usuario"]
    hash_senha = user["senha"]
    print(f"Processando {nome}...")
    start = time.time()
    senha_descoberta = brute_force_sha256(hash_senha)
    end = time.time()
    resultados.append({
        "usuario": nome,
        "hash_senha": hash_senha,
        "senha_encontrada": senha_descoberta,
        "tempo_segundos": round(end - start, 2)
    })

total_end = time.time()
tempo_total = round(total_end - total_start, 2)

print("\nResultados:")
for r in resultados:
    print(f"Usuário: {r['usuario']}")
    print(f"Hash: {r['hash_senha']}")
    print(f"Senha encontrada: {r['senha_encontrada']}")
    print(f"Tempo: {r['tempo_segundos']}s\n")

print(f"Tempo total: {tempo_total}s")