import requests
import os
import json

BASE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "memory")
CONFIG_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "NOVA", "config.txt")


def carregar_modelo():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return f.read().strip()
    return "phi3"


def carregar_arquivos(pasta):
    texto_total = ""

    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".txt"):
                caminho = os.path.join(pasta, arquivo)
                with open(caminho, "r", encoding="utf-8") as f:
                    texto_total += f.read() + "\n"

    return texto_total


def gerar_stream(mensagem_usuario, stop_flag):
    modelo = carregar_modelo()
    memoria = carregar_arquivos(BASE_PATH)[:1500]

    prompt = f"""
SISTEMA:
Você é NOVA, uma IA assistente.

REGRAS:
- Responda apenas a pergunta
- Use memória SOMENTE se relevante
- Nunca copie textos internos
- Seja direta e correta
- Se não souber, diga que não sabe

MEMÓRIA:
{memoria}

PERGUNTA:
{mensagem_usuario}

RESPOSTA:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": modelo,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for linha in response.iter_lines():
        if stop_flag["stop"]:
            break

        if linha:
            try:
                data = json.loads(linha.decode("utf-8"))
                if "response" in data:
                    yield data["response"]
            except:
                pass