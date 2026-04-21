#!/usr/bin/env python3
"""
deduplicador.py — detecta questões que já existam no banco QuestBank.

Comandos (sempre a partir da raiz do projeto):
  python .agents/skills/deduplicacao/scripts/deduplicador.py build <arquivo.questbank.json>
      Lê o backup e gera 'saida/questbank_index.json' com chaves normalizadas.

  python .agents/skills/deduplicacao/scripts/deduplicador.py check <banca> <ano> "<trecho>"
      Verifica se a questão já existe no índice gerado pelo 'build'.
      Responde: DUPLICATA:<id>  ou  NOVA

Uso típico pelo agente:
  1. python .agents/skills/deduplicacao/scripts/deduplicador.py build backup.questbank.json
  2. python .agents/skills/deduplicacao/scripts/deduplicador.py check "ENEM" "2020" "Um dos animais"
"""

import sys
import json
import re
import os

INDEX_PATH = "saida/questbank_index.json"

# --------------------------------------------------------------------------- #
# Utilitários                                                                  #
# --------------------------------------------------------------------------- #

def strip_html(text: str) -> str:
    """Remove tags HTML e normaliza espaços."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalizar(text: str) -> str:
    """Lowercase, remove pontuação extra, normaliza espaços."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # remove pontuação
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chave(banca: str, ano, texto_bruto: str, n: int = 120) -> str:
    """
    Gera uma chave de comparação para uma questão.
    Usa banca + ano + primeiros N caracteres do texto normalizado.
    """
    banca_norm = normalizar(str(banca or ""))
    ano_norm   = str(ano or "").strip()

    # Remove prefixo automático "(BANCA - ANO)" se presente no início
    texto_sem_prefixo = re.sub(
        r"^\s*\(\s*[^)]+\s*-\s*\d{4}\s*\)\s*", "", texto_bruto
    )
    texto_norm = normalizar(strip_html(texto_sem_prefixo))[:n]

    return f"{banca_norm}|{ano_norm}|{texto_norm}"


# --------------------------------------------------------------------------- #
# Subcomando: build                                                             #
# --------------------------------------------------------------------------- #

def build(backup_path: str):
    if not os.path.exists(backup_path):
        print(f"ERRO: arquivo não encontrado: {backup_path}", file=sys.stderr)
        sys.exit(1)

    with open(backup_path, encoding="utf-8") as f:
        backup = json.load(f)

    questions = backup.get("data", {}).get("questions", [])

    index = []
    for q in questions:
        qid       = q.get("id", "")
        banca     = q.get("banca", "")
        ano       = q.get("ano", "")
        enunciado = q.get("enunciado", "")
        k         = chave(banca, ano, enunciado)
        index.append({"id": qid, "banca": banca, "ano": ano, "chave": k})

    os.makedirs("saida", exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"✓ Índice gerado: {INDEX_PATH} ({len(index)} questões)")


# --------------------------------------------------------------------------- #
# Subcomando: check                                                             #
# --------------------------------------------------------------------------- #

def check(banca: str, ano: str, trecho: str):
    if not os.path.exists(INDEX_PATH):
        print(f"ERRO: índice não encontrado. Execute 'build' primeiro.", file=sys.stderr)
        sys.exit(1)

    with open(INDEX_PATH, encoding="utf-8") as f:
        index = json.load(f)

    k_entrada = chave(banca, ano, trecho)

    for item in index:
        # Comparação exata da chave normalizada
        if item["chave"] == k_entrada:
            print(f"DUPLICATA:{item['id']}")
            return

        # Comparação parcial: texto da entrada contido na chave do banco
        # (cobre casos de enunciados mais longos no banco)
        texto_entrada = k_entrada.split("|", 2)[-1]
        texto_banco   = item["chave"].split("|", 2)[-1]
        banca_entrada = k_entrada.split("|")[0]
        banca_banco   = item["chave"].split("|")[0]
        ano_entrada   = k_entrada.split("|")[1]
        ano_banco     = item["chave"].split("|")[1]

        if (banca_entrada == banca_banco
                and ano_entrada == ano_banco
                and len(texto_entrada) >= 40
                and (texto_entrada in texto_banco or texto_banco in texto_entrada)):
            print(f"DUPLICATA:{item['id']}")
            return

    print("NOVA")


# --------------------------------------------------------------------------- #
# Entry point                                                                  #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "build":
        if len(sys.argv) < 3:
            print("Uso: python .agents/skills/deduplicacao/scripts/deduplicador.py build <arquivo.questbank.json>")
            sys.exit(1)
        build(sys.argv[2])

    elif cmd == "check":
        if len(sys.argv) < 5:
            print('Uso: python .agents/skills/deduplicacao/scripts/deduplicador.py check <banca> <ano> "<trecho>"')
            sys.exit(1)
        check(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print(f"Comando desconhecido: {cmd}")
        print(__doc__)
        sys.exit(1)
