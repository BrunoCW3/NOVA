import requests
import os
import json

def carregar_memorias():
    pasta = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "memory")

    memoria_total = ""

    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".txt"):
                caminho = os.path.join(pasta, arquivo)
                with open(caminho, "r", encoding="utf-8") as f:
                    memoria_total += f.read() + "\n"

    return memoria_total


def gerar_stream(mensagem_usuario):
    memoria = carregar_memorias()

    prompt = f"""
SISTEMA:
Você é NOVA, uma IA assistente.

MEMÓRIA DO SISTEMA:
{memoria}

REGRAS (OBRIGATÓRIO):
- Sempre siga a memória acima
- Nunca ignore a memória
- Não invente contexto
- Seja direta

CONVERSA:
Usuário: {mensagem_usuario}
NOVA:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for linha in response.iter_lines():
        if linha:
            try:
                data = json.loads(linha.decode("utf-8"))
                if "response" in data:
                    yield data["response"]
            except:
                pass