#!/usr/bin/env python3
"""
gerar_zip.py — monta saida/questoes.zip (dual-compatível QuestBank + Overleaf).

Uso:
  python .agents/skills/formatador-latex/scripts/gerar_zip.py

Estrutura do ZIP gerado:
  questoes.zip/
    questoes.tex   ← DSL QuestBank (lido pelo app via questbank-server)
    main.tex       ← wrapper Overleaf (compilado pelo pdflatex)
    Imagem1.png    ← imagens referenciadas em \imagem{}, na raiz do ZIP
    Imagem2.png
    ...
"""

import zipfile
import os
import re
import shutil

TEX_PATH  = "saida/questoes.tex"
MAIN_SRC  = "main.tex"        # template na raiz do projeto
MAIN_DEST = "saida/main.tex"
ZIP_PATH  = "saida/questoes.zip"

# Pastas onde o script procura arquivos de imagem
SEARCH_DIRS = [".", "saida", "entrada", "imagens"]


def main():
    if not os.path.exists(TEX_PATH):
        print(f"ERRO: {TEX_PATH} não encontrado. Execute o Passo 3 primeiro.")
        raise SystemExit(1)

    if not os.path.exists(MAIN_SRC):
        print(f"ERRO: {MAIN_SRC} não encontrado na raiz do projeto.")
        raise SystemExit(1)

    # 1. Copiar main.tex para saida/
    shutil.copy(MAIN_SRC, MAIN_DEST)
    print(f"✓ {MAIN_SRC} copiado para {MAIN_DEST}")

    # 2. Encontrar imagens referenciadas em questoes.tex
    with open(TEX_PATH, encoding="utf-8") as f:
        tex = f.read()

    imagens = list(dict.fromkeys(re.findall(r"\\imagem\{([^}]+)\}", tex)))
    print(f"  Imagens referenciadas: {len(imagens)}")

    # 3. Localizar arquivos de imagem
    found_imgs: dict[str, str] = {}   # basename → caminho real
    missing_imgs: list[str] = []

    for img in imagens:
        basename = os.path.basename(img)
        achou = False
        for d in SEARCH_DIRS:
            for candidate in [os.path.join(d, img), os.path.join(d, basename)]:
                if os.path.exists(candidate):
                    found_imgs[basename] = candidate
                    achou = True
                    break
            if achou:
                break
        if not achou:
            missing_imgs.append(img)

    # 4. Montar o ZIP
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(TEX_PATH,  "questoes.tex")
        zf.write(MAIN_DEST, "main.tex")
        for basename, path in found_imgs.items():
            zf.write(path, basename)

    print(f"\n✓ ZIP criado: {ZIP_PATH}")
    print(f"  questoes.tex + main.tex + {len(found_imgs)} imagem(ns)")

    if missing_imgs:
        print(f"\n⚠ Imagens NÃO encontradas ({len(missing_imgs)}) — adicione ao ZIP manualmente:")
        for m in missing_imgs:
            print(f"  - {m}")
    else:
        print("  Todas as imagens encontradas.")


if __name__ == "__main__":
    main()
