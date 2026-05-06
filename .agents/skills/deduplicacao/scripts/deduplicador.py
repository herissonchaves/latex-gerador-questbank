#!/usr/bin/env python3
"""
deduplicador.py — detecta questões que já existam no banco QuestBank.

Comandos (sempre a partir da raiz do projeto):
  python .agents/skills/deduplicacao/scripts/deduplicador.py discover
      Imprime no stdout o caminho do .questbank.json mais recente em backup/
      (ordenação cronológica pelo nome). Sai com código 1 se nenhum existir.

  python .agents/skills/deduplicacao/scripts/deduplicador.py build [<arquivo.questbank.json>]
      Lê o backup e gera 'saida/questbank_index.json' com chaves normalizadas.
      Se <arquivo> for omitido, usa o backup mais recente em backup/.

  python .agents/skills/deduplicacao/scripts/deduplicador.py check <banca> <ano> "<trecho>"
      Verifica UMA questão no índice gerado pelo 'build'.
      Responde no stdout: DUPLICATA:<id>  ou  NOVA

  python .agents/skills/deduplicacao/scripts/deduplicador.py check-batch
      Verifica VÁRIAS questões em uma única chamada (preferido para lotes >5).
      Lê JSON do stdin com a lista de questões e devolve JSON no stdout.

      Stdin:
        [
          {"ref": "q1", "banca": "ENEM",   "ano": "2020", "trecho": "..."},
          {"ref": "q2", "banca": "FUVEST", "ano": "2019", "trecho": "..."}
        ]

      Stdout:
        [
          {"ref": "q1", "status": "DUPLICATA", "id_banco": "00042"},
          {"ref": "q2", "status": "NOVA"}
        ]

      Custa apenas um cold start de Python para todo o lote (vs N starts).

Uso típico pelo agente (workflow padrão):
  1. python .agents/skills/deduplicacao/scripts/deduplicador.py build
  2. echo '[{"ref":"q1","banca":"ENEM","ano":"2020","trecho":"..."}]' \\
       | python .agents/skills/deduplicacao/scripts/deduplicador.py check-batch
"""

import sys
import json
import re
import os
import glob

INDEX_PATH  = "saida/questbank_index.json"
BACKUP_DIR  = "backup"

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

    # Remove HTML first
    texto_limpo = strip_html(texto_bruto)
    # Remove prefixo automático "(BANCA - ANO)" se presente no início
    texto_sem_prefixo = re.sub(
        r"^\s*\(\s*[^)]+\s*-\s*\d{4}\s*\)\s*", "", texto_limpo
    )
    # Remove simple (BANCA) prefix if present
    texto_sem_prefixo = re.sub(
        r"^\s*\(\s*[^)]+\s*\)\s*", "", texto_sem_prefixo
    )
    texto_norm = normalizar(texto_sem_prefixo)[:n]

    return f"{banca_norm}|{ano_norm}|{texto_norm}"


# --------------------------------------------------------------------------- #
# Subcomando: discover                                                         #
# --------------------------------------------------------------------------- #

def discover_backup() -> str:
    """
    Procura o .questbank.json mais recente em backup/.
    O nome padrão é 'questbank-backup-AAAA-MM-DD_HH-MM-SS.questbank.json',
    então ordenação alfabética = ordenação cronológica.

    Retorna o caminho do arquivo, ou None se nenhum existir.
    """
    if not os.path.isdir(BACKUP_DIR):
        return None

    candidatos = sorted(glob.glob(os.path.join(BACKUP_DIR, "*.questbank.json")))
    if not candidatos:
        return None

    # Mais recente = último na ordenação alfabética
    return candidatos[-1]


def discover():
    """Subcomando CLI: imprime o backup mais recente ou sai com código 1."""
    encontrado = discover_backup()
    if encontrado is None:
        print(
            f"ERRO: nenhum *.questbank.json encontrado em {BACKUP_DIR}/",
            file=sys.stderr,
        )
        sys.exit(1)
    print(encontrado)


# --------------------------------------------------------------------------- #
# Subcomando: build                                                             #
# --------------------------------------------------------------------------- #

def build(backup_path: str = None):
    # Auto-descoberta se nenhum caminho foi passado
    if backup_path is None:
        backup_path = discover_backup()
        if backup_path is None:
            print(
                f"ERRO: nenhum *.questbank.json em {BACKUP_DIR}/ e nenhum "
                f"caminho passado como argumento.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"[build] usando backup auto-descoberto: {backup_path}")

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
# Subcomando: check (uma questão de cada vez)                                  #
# --------------------------------------------------------------------------- #

def _carregar_indice():
    if not os.path.exists(INDEX_PATH):
        print(f"ERRO: índice não encontrado. Execute 'build' primeiro.", file=sys.stderr)
        sys.exit(1)
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


def _classificar(banca: str, ano: str, trecho: str, index: list):
    """
    Classifica UMA questão contra o índice já carregado.
    Retorna ("DUPLICATA", id_banco) ou ("NOVA", None).
    """
    k_entrada = chave(banca, ano, trecho)

    for item in index:
        # Comparação exata da chave normalizada
        if item["chave"] == k_entrada:
            return ("DUPLICATA", item["id"])

        # Comparação parcial: texto da entrada contido na chave do banco
        # (cobre casos de enunciados mais longos no banco)
        texto_entrada = k_entrada.split("|", 2)[-1]
        texto_banco   = item["chave"].split("|", 2)[-1]
        banca_entrada = k_entrada.split("|")[0]
        banca_banco   = item["chave"].split("|")[0]
        ano_entrada   = k_entrada.split("|")[1]
        ano_banco     = item["chave"].split("|")[1]

        if (banca_entrada == banca_banco
                and (ano_entrada == ano_banco or ano_entrada == "0" or ano_banco == "0" or ano_entrada == "" or ano_banco == "")
                and len(texto_entrada) >= 40
                and (texto_entrada in texto_banco or texto_banco in texto_entrada)):
            return ("DUPLICATA", item["id"])

    return ("NOVA", None)


def check(banca: str, ano: str, trecho: str):
    index = _carregar_indice()
    status, id_banco = _classificar(banca, ano, trecho, index)
    if status == "DUPLICATA":
        print(f"DUPLICATA:{id_banco}")
    else:
        print("NOVA")


# --------------------------------------------------------------------------- #
# Subcomando: check-batch (várias questões em uma chamada)                     #
# --------------------------------------------------------------------------- #

def check_batch():
    """
    Lê JSON do stdin com lista de questões. Devolve JSON no stdout com
    a classificação de cada uma. Carrega o índice apenas uma vez.
    """
    raw = sys.stdin.read()
    if not raw.strip():
        print("ERRO: stdin vazio. Envie um JSON com a lista de questões.", file=sys.stderr)
        sys.exit(1)

    try:
        entradas = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERRO: JSON inválido no stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(entradas, list):
        print("ERRO: JSON do stdin deve ser uma lista de objetos.", file=sys.stderr)
        sys.exit(1)

    index = _carregar_indice()

    resultados = []
    for entrada in entradas:
        ref    = entrada.get("ref", "")
        banca  = entrada.get("banca", "")
        ano    = entrada.get("ano", "")
        trecho = entrada.get("trecho", "")

        status, id_banco = _classificar(banca, ano, trecho, index)
        item = {"ref": ref, "status": status}
        if id_banco is not None:
            item["id_banco"] = id_banco
        resultados.append(item)

    json.dump(resultados, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


# --------------------------------------------------------------------------- #
# Entry point                                                                  #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "discover":
        discover()

    elif cmd == "build":
        # Argumento opcional: se omitido, auto-descobre em backup/
        backup_arg = sys.argv[2] if len(sys.argv) >= 3 else None
        build(backup_arg)

    elif cmd == "check":
        if len(sys.argv) < 5:
            print('Uso: python .agents/skills/deduplicacao/scripts/deduplicador.py check <banca> <ano> "<trecho>"')
            sys.exit(1)
        check(sys.argv[2], sys.argv[3], sys.argv[4])

    elif cmd == "check-batch":
        check_batch()

    else:
        print(f"Comando desconhecido: {cmd}")
        print(__doc__)
        sys.exit(1)
