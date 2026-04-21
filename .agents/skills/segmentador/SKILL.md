---
name: segmentador
description: >
  Identifica e segmenta questões individuais a partir dos arquivos de texto
  extraídos pelo construtor.py. Use esta skill no Passo 2 do workflow para
  converter cada *_extraido.txt em blocos de questão prontos para LaTeX.
  Aplica regra de fidelidade total: preserva negritos, itálicos, tabelas,
  fórmulas, imagens ([IMAGEM]) e gabaritos exatamente como no original.
  Também responsável por identificar banca, ano e tipo de cada questão.
---

# Segmentador de Questões

## Objetivo

Ler os arquivos `saida/*_extraido.txt` e identificar cada questão individual,
extraindo enunciado, alternativas, gabarito, tipo e metadados de banca/ano.
A saída é uma lista mental de questões segmentadas, pronta para o Passo 3
(escrita do `.tex`).

## Entradas esperadas

- `saida/manifest.json` — gerado pela skill `extrator` (Passo 1)
- `saida/*_extraido.txt` — um arquivo por prova processada

## Saída esperada

Lista interna de questões segmentadas, cada uma contendo:
`banca`, `ano`, `tipo` (`objetiva`/`discursiva`), `enunciado` (LaTeX),
`alternativas` (lista), `gabarito` (letra ou texto), `imagens` (posições).
Esta lista alimenta diretamente o Passo 3 (escrita do `questoes.tex`).

## Passo a passo

### 1. Identificar marcadores de início de questão

| Padrão | Exemplos |
|---|---|
| Número + ponto/parêntese | `1.` `2.` `3)` `01.` `02.` |
| "Questão" + número | `Questão 1` `QUESTÃO 01` |
| Número entre parênteses | `(1)` `(2)` |
| Numeração romana | `I.` `II.` `III.` |
| Variações | `Q1` `Q.01` `1-` |

Se não houver marcadores claros, use o padrão de alternativas como delimitador:
um bloco `a)` / `b)` / `c)` indica o fim de uma questão.

### 2. Extrair componentes de cada questão

| Componente | Como identificar |
|---|---|
| **Enunciado** | Texto entre o marcador de início e as alternativas |
| **Marcador `[IMAGEM]`** | Já presente no texto extraído |
| **Alternativas** | Linhas iniciadas por `a)`/`b)`/`c)`/`d)`/`e)` (maiúsc. ou minúsc.) |
| **Gabarito** | Ao final da prova ou em seção separada: `1-B`, `2.C`, `Gabarito: D` |
| **Tabelas de dados** | Texto com separadores `|` ou alinhamento em colunas |

### 3. ⚠️ Regra de fidelidade total — obrigatória

O texto extraído é a **fonte primária**. Reproduza o conteúdo **exatamente**
como está no original:

| Elemento no original | Representação em LaTeX |
|---|---|
| Texto em **negrito** | `\textbf{texto}` |
| Texto em *itálico* | `\textit{texto}` ou `\emph{texto}` |
| Sobrescrito (m²) | `m\textsuperscript{2}` ou `$m^2$` |
| Subscrito (v₀) | `v\textsubscript{0}` ou `$v_0$` |
| Equação inline | `$...$` |
| Equação em bloco | `$$...$$` |
| Tabela de dados | `\begin{tabular}{ll...}...\end{tabular}` |
| Figura / gráfico / imagem | `\imagem{ImagemN.png}` (numeração sequencial global) |
| Texto motivador | Preserve integralmente, antes da pergunta |
| Referência bibliográfica | Parágrafo próprio após o trecho citado |
| Travessão, meia-risca | `---` (—), `--` (–) |

**Nunca resuma, parafraseie ou omita** trechos do enunciado original.

> `(BANCA - ANO)` é automático — o parser QuestBank insere a partir dos
> `\meta{banca}` e `\meta{ano}`. **Nunca** escreva manualmente no `\enunciado`.

### 4. Converter imagens e tabelas

Converta cada `[IMAGEM]` para `\imagem{ImagemN.png}` com **numeração sequencial
global** (não reinicia por questão): `Imagem1.png`, `Imagem2.png`…
**Nunca** use nomes descritivos. Adaptadas reutilizam o **mesmo nome** da regular mãe.

**Tabelas:**

Texto extraído com colunas alinhadas → converta para:

```latex
\begin{tabular}{ccc}
Velocidade (m/s) & Tempo (s) & Distância (m) \\
10 & 2 & 20 \\
20 & 2 & 40 \\
\end{tabular}
```

A primeira linha vira cabeçalho no HTML gerado pelo parser.

### 5. Identificar banca e ano

Ordem de busca (jamais invente — use padrão se não encontrar):

1. **Texto extraído** — cabeçalho, rodapé, enunciados
2. **Busca na internet** com trecho único entre aspas em sites oficiais
   (ver lista na skill `formatador-latex`). Nunca fóruns ou blogs de gabarito
3. **Não encontrado** → `\meta{banca}{Desconhecida}`, `\meta{ano}{0}`

### 6. Associar gabaritos separados

Gabaritos ao final costumam aparecer como `1-A  2-C  3-B` ou `1. B    2. D`.
Associe cada gabarito à questão pelo número e preencha `\gabarito{LETRA}`.

## Regras e restrições

- **Nunca** resuma, parafraseie ou omita trechos do enunciado original.
- `[IMAGEM]` → `\imagem{ImagemN.png}` com numeração **sequencial global** (não reinicia por questão).
- Nomes de imagem: apenas `Imagem1.png`, `Imagem2.png`… — nunca nomes descritivos.
- Questões adaptadas reutilizam o **mesmo nome** de imagem da regular mãe.
- Banca e ano: buscar no texto ou em sites oficiais — **jamais inventar**.
- `(BANCA - ANO)` **nunca** escrito manualmente dentro de `\enunciado{...}`.

## Checklist de segmentação

- [ ] Todas as questões foram identificadas?
- [ ] Cada questão tem enunciado, tipo e gabarito?
- [ ] `\imagem{ImagemN.png}` preserva a posição de cada `[IMAGEM]`?
- [ ] Numeração de imagens é sequencial global (não reinicia por questão)?
- [ ] Objetivas têm todas as alternativas?
- [ ] Tabelas convertidas para `\begin{tabular}`?
- [ ] Gabaritos associados corretamente?
- [ ] Banca e ano identificados ou usando valores padrão?
- [ ] `(BANCA - ANO)` **não** foi digitado manualmente no `\enunciado`?