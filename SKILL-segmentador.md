# SKILL — Segmentador de Questões

## O que esta skill faz

Identifica e segmenta questões individuais a partir do texto bruto dos
arquivos `saida/*_extraido.txt` (gerados pelo `construtor.py`).

O texto já virá com marcadores `[IMAGEM]` onde havia figuras/gráficos —
no `.tex` cada um vira um `\imagem{caminho}`.

---

## Como identificar questões

### Marcadores de início de questão

| Padrão | Exemplos |
|---|---|
| Número + ponto/parêntese | `1.` `2.` `3)` `01.` `02.` |
| "Questão" + número | `Questão 1` `QUESTÃO 01` |
| Número entre parênteses | `(1)` `(2)` |
| Numeração romana | `I.` `II.` `III.` |
| Variações | `Q1` `Q.01` `1-` |

Se não houver marcadores claros, use o padrão de alternativas como delimitador:
um bloco de `a)` / `b)` / `c)` indica o fim de uma questão.

---

## Componentes de cada questão

| Componente | Como identificar |
|---|---|
| **Enunciado** | Texto entre o marcador de início e as alternativas |
| **Marcador `[IMAGEM]`** | Já presente no texto extraído — vira `\imagem{nome.png}` |
| **Alternativas** | Linhas iniciadas por `a)`/`b)`/`c)`/`d)`/`e)` (maiúsc. ou minúsc.) |
| **Gabarito** | Ao final da prova ou em seção separada: `1-B`, `2.C`, `Gabarito: D` |
| **Tabelas de dados** | Texto com separadores `|` ou alinhamento — vira `\begin{tabular}` |

---

## ⚠️ Regra de fidelidade total — obrigatória

O texto extraído é a **fonte primária**. Ao converter cada questão para o bloco
`\enunciado{...}` do `.tex`, reproduza o conteúdo **exatamente** como está no
original. Isso significa:

| Elemento no original | Como representar em LaTeX |
|---|---|
| Texto em **negrito** | `\textbf{texto}` |
| Texto em *itálico* | `\textit{texto}` ou `\emph{texto}` |
| Sobrescrito (m²) | `m\textsuperscript{2}` ou `$m^2$` em contexto matemático |
| Subscrito (v₀) | `v\textsubscript{0}` ou `$v_0$` |
| Equação / fórmula inline | `$...$` |
| Equação / fórmula em bloco | `$$...$$` |
| Tabela de dados | `\begin{tabular}{ll...}...\end{tabular}` |
| Figura / gráfico / imagem | `\imagem{nome-descritivo.png}` |
| Texto motivador (trecho) | Preserve integralmente, antes da pergunta |
| Referência bibliográfica | Parágrafo próprio após o trecho citado |
| Travessão, meia-risca | `---` (—), `--` (–) |

**Nunca resuma, parafraseie ou omita** trechos do enunciado original.

> O prefixo `(BANCA - ANO)` é inserido **automaticamente** pelo parser QuestBank
> a partir dos `\meta{banca}` e `\meta{ano}`. NÃO digite manualmente.

---

## Tratamento de `[IMAGEM]`

O `construtor.py` insere `[IMAGEM]` onde havia figura/gráfico. No `.tex`,
converta cada ocorrência para:

```latex
\imagem{nome-descritivo.png}
```

Use um nome curto e descritivo (`grafico-energia.png`, `circuito.png`, etc.).
O usuário repõe as imagens reais com esses nomes depois — ou ajusta o caminho
antes de importar.

Nunca remova o marcador nem descreva o conteúdo da imagem.

---

## Tratamento de tabelas

Tabelas de dados aparecem no texto extraído como:

```
Velocidade (m/s) | Tempo (s) | Distância (m)
10               | 2         | 20
20               | 2         | 40
```

Converta para LaTeX:

```latex
\begin{tabular}{ccc}
Velocidade (m/s) & Tempo (s) & Distância (m) \\
10 & 2 & 20 \\
20 & 2 & 40 \\
\end{tabular}
```

A primeira linha vira cabeçalho (`<th>`) após a conversão HTML.

---

## Identificação de banca e ano

**Ordem de busca. Se nada for encontrado, use valores padrão. Jamais invente.**

1. **Texto extraído** — cabeçalho, rodapé, enunciados; procure nomes
   (`ENEM`, `FUVEST`, `UNICAMP`, `VUNESP`, `UERJ`, `ITA`, `IME`, etc.) e anos
   em 4 dígitos.

2. **Busca na internet** com fragmento único entre aspas (ex:
   `"Suponha que o robô da RioBotz tenha massa de 18 kg"`) para localizar a
   prova em sites oficiais. Consulte os sites listados em **SKILL-latex.md**
   ou outros sites institucionais (`.br`, `.gov.br`, `.edu.br`). Nunca fóruns
   nem blogs de gabarito.

3. **Não encontrado** → `\meta{banca}{Desconhecida}`, `\meta{ano}{0}`. Se ambos
   forem assim, o parser omite o prefixo `(BANCA - ANO)` automaticamente.

---

## Gabarito separado

Gabaritos ao final costumam aparecer como:

```
1-A  2-C  3-B  4-E  5-D
```
ou:
```
1. B    2. D    3. A
```

Associe cada gabarito à questão pelo número e preencha `\gabarito{LETRA}`
na objetiva correspondente.

---

## Checklist de segmentação

- [ ] Todas as questões foram identificadas?
- [ ] Cada questão tem enunciado, tipo e gabarito?
- [ ] `\imagem{...}` preserva a posição de cada `[IMAGEM]` do original?
- [ ] Objetivas têm todas as alternativas?
- [ ] Tabelas convertidas para `\begin{tabular}`?
- [ ] Gabaritos associados corretamente?
- [ ] Banca e ano identificados no texto ou pesquisados em site oficial?
- [ ] Se não encontrado, usou `Desconhecida` / `0` em vez de inventar?
- [ ] Não digitou `(BANCA - ANO)` manualmente no `\enunciado`?
