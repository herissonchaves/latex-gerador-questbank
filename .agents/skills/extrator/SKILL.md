---
name: extrator
description: >
  Extrai texto e estrutura dos arquivos de prova depositados em entrada/.
  Use esta skill no Passo 1 do workflow para processar PDFs, DOCXs, imagens
  e HTMLs, gerando os arquivos *_extraido.txt e o manifest.json em saida/.
  Ativar sempre que o usuário depositar novos arquivos em entrada/ e pedir
  para iniciar o processamento, ou ao começar um novo lote de questões.
---

# Extrator de Texto (construtor.py)

## Objetivo

Processar os arquivos brutos em `entrada/` e gerar texto extraído com
fidelidade máxima ao original, pronto para a skill `segmentador` ler.

## Entradas esperadas

- Pasta `entrada/` contendo PDFs, DOCXs, imagens ou HTMLs das provas
- Nenhuma configuração manual necessária — o script varre a pasta automaticamente

## Como executar

```bash
python .agents/skills/extrator/scripts/construtor.py
```

Opções disponíveis (rode `--help` para ver todas):

```bash
python .agents/skills/extrator/scripts/construtor.py --help
```

## O que o script faz

1. Varre `entrada/` em busca de arquivos suportados
2. Extrai texto preservando: negrito, itálico, tabelas, fórmulas matemáticas
3. Substitui figuras/gráficos por `[IMAGEM]`
4. Salva cada arquivo como `saida/<nome>_extraido.txt`
5. Gera `saida/manifest.json` com a lista de arquivos processados

## Formatos suportados

| Formato | Extensões |
|---|---|
| PDF | `.pdf` |
| Word | `.docx`, `.doc` |
| Imagens de prova | `.png`, `.jpg`, `.jpeg`, `.webp` |
| HTML | `.html`, `.htm` |

## Saídas geradas

```
saida/
  manifest.json          ← lista de arquivos processados
  <nome>_extraido.txt    ← texto extraído (um por arquivo de entrada)
```

Leia o `manifest.json` após a execução para saber quais arquivos foram
processados com sucesso e quais falharam.

## Dependências

O script instala automaticamente as dependências Python na primeira execução.
Requer **Tesseract OCR** instalado no sistema para processar imagens:
- Download: https://github.com/tesseract-ocr/tesseract
- Com pacote de português: `tesseract-ocr-por`

## Regras e restrições

- Se um arquivo não puder ser lido (corrompido, senha, formato inválido):
  registre o erro no `manifest.json` e continue processando os demais.
- Não interrompa o processamento por falha em arquivo individual.
- Nunca converta ou renomeie imagens extraídas — use o marcador `[IMAGEM]`.
- Não gere LaTeX nesta etapa — a saída é sempre texto plano.

## Checklist

- [ ] Arquivos de prova estão em `entrada/`?
- [ ] Script executado sem erros?
- [ ] `saida/manifest.json` gerado?
- [ ] Pelo menos um `*_extraido.txt` gerado por arquivo de entrada?
- [ ] Arquivos com falha registrados e reportados ao usuário?
