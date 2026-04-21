---
name: formatador-latex
description: >
  Define o formato DSL LaTeX do QuestBank e todas as regras para escrever
  blocos \begin{questao}...\end{questao} válidos. Use esta skill no Passo 3
  para escrever questoes.tex e no Passo 5 para gerar questoes.zip via script.
  Consulte também para: macros disponíveis, taxonomia de metadados, Unicode
  proibido, conversões LaTeX→HTML, regras de imagem, checklist de validação
  e lista de sites oficiais para pesquisa de banca/ano.
---

# Formato LaTeX do QuestBank (`questoes.tex`)

## Objetivo

Escrever `saida/questoes.tex` com blocos `\begin{questao}` válidos para cada
questão segmentada e gerar `saida/questoes.zip` dual-compatível com o app
QuestBank e o Overleaf. O agente **não** gera JSON — único formato de saída
é o `.tex` (DSL customizada convertida pelo servidor `questbank-server`).

## Entradas esperadas

- Lista de questões segmentadas (Passo 2 / Passo 2.5)
- `main.tex` na raiz do projeto (wrapper Overleaf — não editar)
- Imagens referenciadas pelos marcadores `[IMAGEM]` nos textos extraídos

---

## ZIP dual-compatível (`saida/questoes.zip`)

### Estrutura do ZIP

```
questoes.zip/
  questoes.tex   ← DSL QuestBank — lida pelo servidor Python (app)
  main.tex       ← wrapper LaTeX padrão — compilado pelo Overleaf
  Imagem1.png    ← imagens sempre na RAIZ do ZIP (sem subpastas)
  Imagem2.png
```

### Regra de caminhos de imagem

- Em `questoes.tex`: sempre `\imagem{ImagemN.png}` — **só o nome, nunca pasta**
- Use **numeração sequencial global**: `Imagem1.png`, `Imagem2.png`…
  A contagem avança a cada nova imagem em todo o arquivo (não reinicia por questão)
- **Nunca** use nomes descritivos (`grafico-energia.png`, `circuito.png`, etc.)
- **Questões adaptadas reutilizam exatamente o mesmo nome** da regular mãe

### ⚠ Unicode matemático é proibido em `questoes.tex`

| ✗ Errado (Unicode) | ✓ Correto (LaTeX) |
|---|---|
| `₀` | `$_0$` ou `\textsubscript{0}` |
| `²` | `$^2$` ou `\textsuperscript{2}` |
| `≈` | `$\approx$` |
| `√` | `$\sqrt{x}$` |
| `×` | `$\times$` |
| `°` | `$^{\circ}$` |
| `π` | `$\pi$` |
| `μ` | `$\mu$` |

---

## Estrutura do arquivo `.tex`

```latex
% arquivo: saida/questoes.tex

\begin{questao}{742831}
  \meta{tipo}{objetiva}
  \meta{banca}{ENEM}
  \meta{ano}{2020}
  \meta{disciplina}{Física}
  \meta{topico}{Energia}
  \meta{conteudo}{Fontes de energia}
  \meta{assunto}{Energia eólica e impacto ambiental}
  \meta{dificuldade}{medio}

  \enunciado{
    Texto do enunciado em LaTeX puro.

    \imagem{Imagem1.png}

    Outro parágrafo após a imagem.
  }

  \begin{alternativas}
    \alt{A}{primeira alternativa}
    \alt{B}{segunda com $\frac{a}{b}$ inline}
    \alt{C}{terceira}
    \alt{D}{quarta}
    \alt{E}{quinta}
  \end{alternativas}

  \gabarito{E}
\end{questao}
```

### IDs aleatórios — como funciona

- Regular → **número aleatório de 6 dígitos** (100000–999999), único no arquivo
- Adaptada → **mesmo número com prefixo `A-`**
- **Nunca** use IDs sequenciais (000001…) — podem colidir com IDs do banco

```python
import random
n = 10  # número de questões regulares
ids = random.sample(range(100000, 1000000), n)
```

---

## Macros reconhecidas

| Macro | Obrigatória? | Observação |
|---|---|---|
| `\begin{questao}{ID}` | sim | 6 dígitos aleatórios; `A-NNNNNN` para adaptadas |
| `\meta{tipo}{...}` | sim | `objetiva` ou `discursiva` |
| `\meta{banca}{...}` | recomendada | `Desconhecida` se omitida |
| `\meta{ano}{...}` | recomendada | inteiro; `0` se omitida |
| `\meta{disciplina}{...}` | sim | ver taxonomia abaixo |
| `\meta{topico}{...}` | sim | |
| `\meta{conteudo}{...}` | sim | |
| `\meta{assunto}{...}` | sim | |
| `\meta{dificuldade}{...}` | sim | `facil` / `medio` / `dificil` |
| `\meta{tags}{a, b, c}` | não | **deixar em branco — não preencher** |
| `\enunciado{...}` | sim | texto em LaTeX puro |
| `\begin{alternativas}...\end{alternativas}` | se objetiva | |
| `\alt{LETRA}{texto}` | dentro do bloco | letra maiúscula |
| `\gabarito{...}` | sim | objetiva: letra; discursiva: resposta |
| `\imagem{ImagemN.png}` | dentro de `\enunciado` | só nome do arquivo |
| `\resolucao{url}` | não | |

---

## Conversões LaTeX → HTML (automáticas no parser)

| Em LaTeX você escreve | No HTML sai |
|---|---|
| Parágrafos com linha em branco | `<p>...</p>` |
| `$x$` e `$$x$$` | preservado (KaTeX renderiza) |
| `\textbf{x}` | `<strong>x</strong>` |
| `\textit{x}`, `\emph{x}` | `<em>x</em>` |
| `\textsuperscript{2}` | `<sup>2</sup>` |
| `\textsubscript{0}` | `<sub>0</sub>` |
| `\imagem{Imagem1.png}` | `<p>[IMAGEM]</p>` + registra em `imagens` |
| `\begin{tabular}{cc}...\end{tabular}` | `<table>` com 1ª linha `<th>` |
| `---`, `--` | `—`, `–` |
| `\_\_\_\_` | `____` (linha de resposta em discursivas) |

> O parser insere `(BANCA - ANO)` automaticamente. **Não adicione manualmente.**

---

## Regras de LaTeX puro

```latex
% ✓ correto (uma barra só)
$m = 18\,\text{kg}$

% ✗ errado — não use \\ no .tex
$m = 18\\,\\text{kg}$
```

Notação científica: `$3{,}6 \times 10^{10}\,\text{Pa}$`

Vírgula decimal: `$9{,}8\,\text{m/s}^2$`

---

## Taxonomia e metadados

### `disciplina`
`Física` · `Química` · `Matemática` · `Biologia` · `Ciências` · `Geografia` ·
`História` · `Português` · `Inglês`

### `dificuldade`
- `facil` — uma etapa, sem cálculo complexo
- `medio` — mais de uma etapa ou conceito
- `dificil` — múltiplas etapas, integração de conceitos

### Preenchimento de metadados — ordem de busca

1. **Texto do documento** — cabeçalho, rodapé, enunciados
2. **Busca na internet** com fragmento único entre aspas em sites oficiais:

| O que buscar | Sites |
|---|---|
| ENEM | `enem.inep.gov.br` |
| FUVEST | `fuvest.br` |
| UNICAMP | `comvest.unicamp.br` |
| VUNESP | `vunesp.com.br` |
| UERJ | `vestibular.uerj.br` |
| ITA / IME | `ita.br` · `ime.eb.br` |
| Outras | Site institucional oficial (`.br`, `.gov.br`, `.edu.br`) |

3. **Não encontrado** → `Desconhecida` / `0`. **Jamais invente.**

---

## Gerar o ZIP (Passo 5)

Execute o script dedicado:

```bash
python .agents/skills/formatador-latex/scripts/montador.py
```

O script lê `saida/questoes.tex`, encontra as imagens referenciadas, copia
`main.tex` e monta o ZIP em `saida/questoes.zip`.

---

## Checklist antes de entregar `saida/questoes.tex`

- [ ] Todos os blocos `\begin{questao}{ID}...\end{questao}` balanceados?
- [ ] IDs aleatórios de 6 dígitos (100000–999999), únicos no arquivo?
- [ ] Cada adaptada tem prefixo `A-` com o mesmo número da regular mãe?
- [ ] Nenhum ID sequencial com zeros à esquerda (000001…)?
- [ ] Cada `\meta{}` com dois argumentos (campo e valor)?
- [ ] `\meta{tipo}` é `objetiva` ou `discursiva`?
- [ ] Objetivas têm `\begin{alternativas}` e `\gabarito{LETRA}`?
- [ ] Letra do `\gabarito` bate com uma `\alt{LETRA}{...}`?
- [ ] Imagens via `\imagem{ImagemN.png}` — numeração sequencial global?
- [ ] Nenhuma imagem com nome descritivo?
- [ ] Adaptadas reutilizam o mesmo nome de imagem da regular mãe?
- [ ] Fórmulas em `$...$` ou `$$...$$` fechadas?
- [ ] Barras LaTeX únicas (sem `\\`)?
- [ ] Nenhum símbolo Unicode matemático (₀ ≈ √ ° × π…)?
- [ ] `(BANCA - ANO)` não digitado manualmente?
- [ ] Metadados pesquisados (nunca inventados)?
- [ ] Nenhuma questão duplicada incluída no arquivo?
