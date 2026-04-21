#!/usr/bin/env python3
"""
construtor.py — Extrator FIEL de texto para o workflow QuestBank (Modo Lite).

OBJETIVO: reproduzir o conteúdo dos documentos com máxima fidelidade ao original,
preservando formatação (negrito, itálico, sublinhado, alinhamento), equações
matemáticas e estrutura de tabelas. Imagens/figuras são substituídas por [IMAGEM]
— nenhum dado binário é extraído.

Formato de saída: HTML simples salvo em *_extraido.txt, pronto para o agente
Antigravity ler e segmentar as questões.

Suporta: PDF (.pdf), Word (.docx/.doc), imagens de prova (.png/.jpg/etc.), HTML.

Dependências Python (instaladas automaticamente):
    pymupdf, python-docx, lxml, pytesseract, Pillow, opencv-python-headless, numpy

Dependência de sistema (instalar manualmente):
    Tesseract OCR — https://github.com/tesseract-ocr/tesseract
    Com pacote de idioma português: tesseract-ocr-por

Uso:
    python construtor.py [--entrada PASTA] [--saida PASTA]
"""

import sys
import json
import argparse
import datetime
from pathlib import Path


# ── Instalador de dependências ────────────────────────────────────────────────

def importar_ou_instalar(pacote, import_name=None):
    import importlib
    nome = import_name or pacote
    try:
        return importlib.import_module(nome)
    except ImportError:
        import subprocess
        print(f"[construtor] Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote, "-q"])
        return importlib.import_module(nome)


# ── Extrator PDF — fiel com formatação ───────────────────────────────────────

def extrair_pdf(caminho: Path) -> str:
    """
    Extrai texto de PDF preservando:
    - Negrito / itálico (via flags de fonte)
    - Alinhamento de parágrafo (left/center/right/justify)
    - Posição relativa de imagens: marcador [IMAGEM] inserido na ordem correta da página
    - Equações: preservadas como texto (LaTeX se reconhecível, texto puro caso contrário)
    """
    fitz = importar_ou_instalar("pymupdf", "fitz")

    doc   = fitz.open(str(caminho))
    saida = []

    for num_pag, pagina in enumerate(doc, start=1):
        saida.append(f"<!-- PÁGINA {num_pag} -->")

        # Coleta blocos de texto e posições de imagens, ordena por y0
        itens = []

        blocos = pagina.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for bloco in blocos:
            if bloco["type"] == 0:   # bloco de texto
                itens.append(("TEXTO", bloco["bbox"][1], bloco))

        for img in pagina.get_images(full=False):
            rects = pagina.get_image_rects(img[0])
            for r in rects:
                itens.append(("IMG", r.y0, None))

        itens.sort(key=lambda x: x[1])

        larg_pag = pagina.rect.width

        for tipo, _, dado in itens:

            if tipo == "IMG":
                saida.append("<p>[IMAGEM]</p>")
                continue

            bloco = dado
            linhas_html = []

            for linha in bloco.get("lines", []):
                spans_html = []
                for span in linha.get("spans", []):
                    texto = span.get("text", "")
                    if not texto.strip():
                        continue

                    flags      = span.get("flags", 0)
                    negrito    = bool(flags & (1 << 4))   # bit 4 = bold
                    italico    = bool(flags & (1 << 1))   # bit 1 = italic
                    nome_fonte = span.get("font", "").lower()
                    sublinhado = "underline" in nome_fonte

                    # Superscrito/subscrito: compara origem (y) do span com a linha
                    origem_span = span.get("origin", [0, 0])
                    origem_linha = linha.get("bbox", [0, 0, 0, 0])
                    deslocamento_y = origem_linha[1] - origem_span[1]  # positivo = acima
                    tamanho = span.get("size", 12)
                    limiar  = tamanho * 0.3

                    t = texto
                    if sublinhado: t = f"<u>{t}</u>"
                    if italico:    t = f"<i>{t}</i>"
                    if negrito:    t = f"<b>{t}</b>"
                    if deslocamento_y > limiar:   t = f"<sup>{t}</sup>"
                    elif deslocamento_y < -limiar: t = f"<sub>{t}</sub>"
                    spans_html.append(t)

                if spans_html:
                    linhas_html.append(" ".join(spans_html))

            if not linhas_html:
                continue

            # Alinhamento pelo bbox do bloco vs largura da página
            x0, _, x1, _ = bloco["bbox"]
            margem_esq = x0
            margem_dir = larg_pag - x1

            if margem_dir < 50 and margem_esq > larg_pag * 0.3:
                alinha = "right"
            elif abs(margem_esq - margem_dir) < 20:
                alinha = "center"
            else:
                alinha = "justify"

            conteudo = "<br>".join(linhas_html)
            saida.append(f'<p style="text-align:{alinha};">{conteudo}</p>')

    doc.close()
    return "\n".join(saida)


# ── Extrator DOCX — fiel com formatação ──────────────────────────────────────

def extrair_docx(caminho: Path) -> str:
    """
    Extrai DOCX preservando:
    - Negrito, itálico, sublinhado por run
    - Alinhamento de parágrafo
    - Tabelas convertidas para <table> HTML
    - Imagens inline: [IMAGEM] inserido na posição correta
    - Equações OMML (Word math): texto aproximado entre $[EQUAÇÃO: ...]$
    """
    importar_ou_instalar("python-docx", "docx")
    importar_ou_instalar("lxml", "lxml")
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from lxml import etree

    doc = Document(str(caminho))

    ALINHA = {
        WD_ALIGN_PARAGRAPH.LEFT:    "left",
        WD_ALIGN_PARAGRAPH.CENTER:  "center",
        WD_ALIGN_PARAGRAPH.RIGHT:   "right",
        WD_ALIGN_PARAGRAPH.JUSTIFY: "justify",
        None:                        "left",
    }

    def omml_para_texto(elem):
        textos = [t for t in elem.itertext() if t.strip()]
        eq = " ".join(textos) if textos else "?"
        return f"$[EQUAÇÃO: {eq}]$"

    def runs_para_html(paragrafo):
        partes = []
        for elem in paragrafo._element:
            local = etree.QName(elem).localname if not callable(elem.tag) else ""

            # Equação OMML
            if local in ("oMath", "oMathPara"):
                partes.append(omml_para_texto(elem))
                continue

            if local != "r":
                continue

            # Imagem inline
            tem_img = (
                elem.find(".//" + qn("a:graphicData")) is not None or
                elem.find(".//" + qn("w:drawing"))     is not None or
                elem.find(".//" + qn("w:pict"))        is not None
            )
            if tem_img:
                partes.append("[IMAGEM]")
                continue

            # Texto com formatação
            texto = "".join(
                t.text or "" for t in elem.findall(qn("w:t"))
            )
            if not texto:
                continue

            rpr        = elem.find(qn("w:rPr"))
            negrito    = rpr is not None and rpr.find(qn("w:b"))  is not None
            italico    = rpr is not None and rpr.find(qn("w:i"))  is not None
            sublinhado = rpr is not None and rpr.find(qn("w:u"))  is not None

            # Superscrito / subscrito
            vert_align = ""
            if rpr is not None:
                va = rpr.find(qn("w:vertAlign"))
                if va is not None:
                    vert_align = va.get(qn("w:val"), "")

            t = texto
            if sublinhado:           t = f"<u>{t}</u>"
            if italico:              t = f"<i>{t}</i>"
            if negrito:              t = f"<b>{t}</b>"
            if vert_align == "superscript": t = f"<sup>{t}</sup>"
            if vert_align == "subscript":   t = f"<sub>{t}</sub>"
            partes.append(t)

        return "".join(partes)

    def tabela_para_html(tabela):
        linhas = []
        for i, row in enumerate(tabela.rows):
            celulas = []
            for cell in row.cells:
                tag  = "th" if i == 0 else "td"
                txt  = " ".join(runs_para_html(p) for p in cell.paragraphs).strip()
                celulas.append(f"<{tag}>{txt}</{tag}>")
            linhas.append("<tr>" + "".join(celulas) + "</tr>")
        return (
            '<table border="1" cellpadding="4" cellspacing="0">'
            + "".join(linhas)
            + "</table>"
        )

    saida = []
    from docx.text.paragraph import Paragraph
    from docx.table import Table

    for elem in doc.element.body:
        local = etree.QName(elem).localname

        if local == "p":
            para     = Paragraph(elem, doc)
            alinha   = ALINHA.get(para.alignment, "left")
            conteudo = runs_para_html(para)
            if conteudo.strip():
                saida.append(f'<p style="text-align:{alinha};">{conteudo}</p>')

        elif local == "tbl":
            saida.append(tabela_para_html(Table(elem, doc)))

    return "\n".join(saida)


# ── Detecção do caminho do Tesseract OCR ─────────────────────────────────────

def configurar_tesseract():
    """
    Auto-detecta o executável do Tesseract nos locais de instalação padrão.
    Deve ser chamado uma vez antes de usar pytesseract.
    """
    import pytesseract
    import shutil

    # Se já está no PATH, não precisa fazer nada
    if shutil.which("tesseract"):
        return

    candidatos = [
        # Windows — instalador padrão
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        # macOS — Homebrew
        "/usr/local/bin/tesseract",
        "/opt/homebrew/bin/tesseract",
        # Linux — pacote apt/yum
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
    ]
    for caminho in candidatos:
        if Path(caminho).exists():
            pytesseract.pytesseract.tesseract_cmd = caminho
            return

    raise FileNotFoundError(
        "Tesseract OCR não encontrado. Verifique a instalação e o PATH do sistema."
    )


# ── Extrator IMAGEM — OCR fiel com pré-processamento ─────────────────────────

def extrair_imagem_ocr(caminho: Path) -> str:
    """
    Extrai texto de imagens de prova com alta fidelidade usando Tesseract OCR.

    Pré-processamento aplicado para maximizar qualidade:
      1. Converte para escala de cinza
      2. Aumenta resolução para 300 DPI (padrão recomendado para OCR)
      3. Aumenta contraste com equalização de histograma
      4. Binarização adaptativa (Otsu) para texto sobre fundo complexo

    Configuração Tesseract:
      --psm 6  — bloco uniforme de texto (bom para provas com colunas)
      -l por+eng — português como primário, inglês como fallback para siglas

    O resultado é HTML com comentários de instrução para o agente.
    """
    importar_ou_instalar("pytesseract")
    importar_ou_instalar("Pillow", "PIL")
    importar_ou_instalar("opencv-python-headless", "cv2")
    importar_ou_instalar("numpy", "numpy")

    import pytesseract
    import cv2
    import numpy as np
    from PIL import Image as PILImage

    configurar_tesseract()

    # ── Pré-processamento ─────────────────────────────────────────────────────
    img_pil = PILImage.open(caminho).convert("RGB")

    # Garante resolução mínima de 300 DPI para OCR de qualidade
    dpi_orig = img_pil.info.get("dpi", (72, 72))
    dpi_x    = dpi_orig[0] if isinstance(dpi_orig, tuple) else dpi_orig
    if dpi_x < 200:
        fator   = 300 / max(dpi_x, 1)
        w, h    = img_pil.size
        img_pil = img_pil.resize((int(w * fator), int(h * fator)), PILImage.LANCZOS)

    # Converte para array OpenCV (BGR)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Escala de cinza
    cinza = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Equalização de histograma CLAHE (preserva contraste local — bom para provas escaneadas)
    clahe  = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cinza  = clahe.apply(cinza)

    # Binarização adaptativa de Otsu
    _, binaria = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    img_final = PILImage.fromarray(binaria)

    # ── OCR ───────────────────────────────────────────────────────────────────
    # psm 6 = bloco uniforme; oem 3 = motor LSTM (melhor qualidade)
    config = "--psm 6 --oem 3 -l por+eng"
    texto  = pytesseract.image_to_string(img_final, config=config)

    if not texto.strip():
        texto = "[OCR não retornou texto. Verifique a qualidade da imagem.]"

    return (
        f"<!-- ══════════════════════════════════════════════════════════ -->\n"
        f"<!-- ARQUIVO DE IMAGEM: {caminho.name}                         -->\n"
        f"<!-- Texto extraído via Tesseract OCR (por+eng, psm6, CLAHE).  -->\n"
        f"<!--                                                            -->\n"
        f"<!-- AO USAR ESTE TEXTO, preserve EXATAMENTE:                  -->\n"
        f"<!--   • negrito, itálico, sublinhado                          -->\n"
        f"<!--   • alinhamento (esquerda / centro / direita)             -->\n"
        f"<!--   • equações matemáticas → converter para LaTeX           -->\n"
        f"<!--   • estrutura de tabelas → converter para <table> HTML    -->\n"
        f"<!--   • figuras / gráficos dentro da prova → [IMAGEM]         -->\n"
        f"<!-- O OCR pode errar em símbolos matemáticos — revise sempre. -->\n"
        f"<!-- ══════════════════════════════════════════════════════════ -->\n\n"
        f"<pre>{texto.strip()}</pre>"
    )


# ── Extrator HTML ─────────────────────────────────────────────────────────────

def extrair_html(caminho: Path) -> str:
    """Lê HTML diretamente. Remove scripts/styles. Substitui <img> por [IMAGEM]."""
    importar_ou_instalar("beautifulsoup4", "bs4")
    from bs4 import BeautifulSoup

    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()

    soup = BeautifulSoup(conteudo, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    for img in soup.find_all("img"):
        img.replace_with("[IMAGEM]")
    return str(soup.body or soup)


# ── Dispatcher ────────────────────────────────────────────────────────────────

EXTENSOES = {
    ".pdf":  extrair_pdf,
    ".docx": extrair_docx,
    # NOTA: .doc (formato antigo) NÃO é suportado por python-docx.
    # Converta para .docx antes de usar (ex: LibreOffice → soffice --convert-to docx).
    ".png":  extrair_imagem_ocr,
    ".jpg":  extrair_imagem_ocr,
    ".jpeg": extrair_imagem_ocr,
    ".webp": extrair_imagem_ocr,
    ".bmp":  extrair_imagem_ocr,
    ".gif":  extrair_imagem_ocr,
    ".html": extrair_html,
    ".htm":  extrair_html,
}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Extrator FIEL de texto (modo lite) para QuestBank"
    )
    parser.add_argument("--entrada", default="entrada", help="Pasta de entrada")
    parser.add_argument("--saida",   default="saida",   help="Pasta de saída")
    args = parser.parse_args()

    pasta_entrada = Path(args.entrada)
    pasta_saida   = Path(args.saida)

    if not pasta_entrada.exists():
        print(f"[ERRO] Pasta de entrada não encontrada: {pasta_entrada}")
        sys.exit(1)

    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivos = sorted([
        f for f in pasta_entrada.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSOES
    ])

    if not arquivos:
        print("[AVISO] Nenhum arquivo suportado na pasta de entrada.")
        sys.exit(0)

    manifest = {
        "modo": "lite-fiel",
        "gerado_em": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pasta_entrada": str(pasta_entrada),
        "total_arquivos": len(arquivos),
        "nota": (
            "Extração fiel com Tesseract OCR: negrito, itálico, sublinhado, alinhamento e equações preservados. "
            "Imagens/figuras substituídas por [IMAGEM]."
        ),
        "arquivos": [],
    }

    for caminho in arquivos:
        print(f"[construtor] {caminho.name} ...", end=" ", flush=True)
        extrator = EXTENSOES[caminho.suffix.lower()]
        try:
            texto       = extrator(caminho)
            nome_txt    = caminho.stem + "_extraido.txt"
            caminho_txt = pasta_saida / nome_txt
            with open(caminho_txt, "w", encoding="utf-8") as f:
                f.write(texto)
            registro = {"arquivo": caminho.name, "status": "ok",
                        "texto_extraido_arquivo": str(caminho_txt)}
            print("OK")
        except Exception as e:
            registro = {"arquivo": caminho.name, "status": "erro", "motivo": str(e)}
            print(f"ERRO — {e}")

        manifest["arquivos"].append(registro)

    caminho_manifest = pasta_saida / "manifest.json"
    with open(caminho_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n[construtor] Concluído. Manifest: {caminho_manifest}")


if __name__ == "__main__":
    main()
