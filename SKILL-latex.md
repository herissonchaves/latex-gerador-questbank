# SKILL — Formato LaTeX do QuestBank (`.tex`)

Esta skill define o formato de questões (`questoes.tex`) e o **entregável final**
do agente: `saida/questoes.zip`, um ZIP dual-compatível aceito tanto pelo
**QuestBank** quanto pelo **Overleaf** (compilador LaTeX online).

O `questoes.tex` usa uma **DSL customizada** convertida em JSON pelo servidor
local `questbank-server` no momento da importação no app — o agente NÃO gera JSON.

O ZIP também inclui `main.tex`, um wrapper LaTeX padrão que define todas as macros
da DSL e permite compilar o mesmo `questoes.tex` diretamente no Overleaf.

Vantagens do formato `.tex`:

- Edição confortável em qualquer editor LaTeX antes de importar.
- Backslash único (`\frac`, `\text`) — sem escaping duplo de JSON.
- Fórmulas legíveis, diff amigável no git.
- Imagens por caminho relativo.
- Comentários `%` para notas.

---

## ZIP dual-compatível (`saida/questoes.zip`)

### Estrutura do ZIP

```
questoes.zip/
  questoes.tex   ← DSL QuestBank — lida pelo servidor Python (app)
  main.tex       ← wrapper LaTeX padrão — compilado pelo Overleaf
  imagem1.png    ← imagens sempre na RAIZ do ZIP (sem subpastas)
  imagem2.png
```

### Como cada sistema usa o ZIP

| Sistema | Arquivo de entrada | O que faz |
|---|---|---|
| **QuestBank** | `questoes.tex` | Parser Python converte DSL → JSON e importa |
| **Overleaf** | `main.tex` | Compila com pdflatex; `\input{questoes}` inclui as questões |

### Regra de caminhos de imagem

- Em `questoes.tex`: sempre `\imagem{ImagemN.png}` — **só o nome do arquivo, nunca pasta**.
- Use **numeração sequencial global**: `Imagem1.png`, `Imagem2.png`, `Imagem3.png`…
  A contagem avança a cada nova imagem em todo o arquivo (não reinicia por questão).
- **Nunca** use nomes descritivos (`grafico-energia.png`, `circuito.png`, etc.).
- **Questões adaptadas reutilizam exatamente o mesmo nome** da imagem da regular mãe.
- No ZIP: todas as imagens na **raiz** (ao lado de `questoes.tex` e `main.tex`).
- O `main.tex` usa `\includegraphics{ImagemN.png}` — encontra a imagem na mesma pasta.
- O parser QuestBank indexa imagens por basename — encontra independente de subpasta.

### ⚠ Unicode matemático é proibido em `questoes.tex`

**NUNCA** cole símbolos Unicode matemáticos. Use sempre LaTeX puro:

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

Unicode matemático causa erros de compilação no Overleaf (`! LaTeX Error: Unicode
character … not set up for use with LaTeX`) e pode corromper o HTML gerado pelo parser.

---

## Estrutura do arquivo `.tex`

Um único arquivo (`saida/questoes.tex`) contém **todas** as questões, cada
uma em um bloco `\begin{questao}{ID}...\end{questao}`. Comentários `%` são
permitidos e ignorados pelo parser.

```latex
% arquivo: saida/questoes.tex

\begin{questao}{742831}
  \meta{tipo}{objetiva}
  \meta{banca}{ENEM}
  \meta{ano}{2020}
  \meta{disciplina}{Física}
  \meta{topico}{Energia}
  \meta{conteudo}{Fontes de energia}
  \meta{assunto}{Energia eólica}
  \meta{dificuldade}{medio}

  \enunciado{
    Texto do enunciado em LaTeX puro.

    Quebra de parágrafo com linha em branco.

    \imagem{Imagem1.png}

    Outro parágrafo após a imagem.
  }

  \begin{alternativas}
    \alt{A}{primeira alternativa}
    \alt{B}{segunda alternativa com $\frac{a}{b}$ inline}
    \alt{C}{terceira}
    \alt{D}{quarta}
    \alt{E}{quinta}
  \end{alternativas}

  \gabarito{E}
\end{questao}
```

### ID aleatório — como funciona

- Cada questão regular recebe um **número aleatório de 6 dígitos** (100000–999999),
  único dentro do arquivo.
- A versão adaptada recebe o **mesmo número com prefixo `A-`**.
- Esses IDs são temporários: o QuestBank os usa só para vincular filha → mãe
  durante a importação. Após a importação, o app substitui ambos por IDs
  sequenciais definitivos a partir do último ID cadastrado no banco.
- **Nunca use IDs sequenciais** (000001, 000002…) — podem colidir com IDs já
  existentes no banco do usuário.

Exemplo de geração (Python — execute antes de escrever o arquivo):

```python
import random
n = 10  # número de questões regulares
ids = random.sample(range(100000, 1000000), n)
print(ids)  # [742831, 193057, 856402, ...]
```

---

## Macros reconhecidas

| Macro | Obrigatória? | Observação |
|---|---|---|
| `\begin{questao}{ID}` | sim | número aleatório de 6 dígitos (100000–999999); `A-NNNNNN` para adaptadas |
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
| `\gabarito{...}` | objetiva: letra; discursiva: resposta | |
| `\imagem{caminho}` | dentro de `\enunciado` | caminho relativo ao `.tex` |
| `\resolucao{url}` | não | |

---

## Conversões LaTeX → HTML (automáticas no parser)

Você **não precisa** escrever HTML. Use LaTeX puro; o parser converte:

| Em LaTeX você escreve | No HTML sai |
|---|---|
| Parágrafos separados por linha em branco | `<p>...</p>` |
| `$x$` e `$$x$$` | preservado (KaTeX renderiza) |
| `\textbf{x}` | `<strong>x</strong>` |
| `\textit{x}`, `\emph{x}` | `<em>x</em>` |
| `\textsuperscript{2}` | `<sup>2</sup>` |
| `\textsubscript{0}` | `<sub>0</sub>` |
| `\imagem{foto.png}` | `<p>[IMAGEM]</p>` + registra em `imagens` |
| `\begin{tabular}{cc}...\end{tabular}` | `<table>` com 1ª linha `<th>` |
| `---`, `--` | `—`, `–` |
| `\_\_\_\_` | `____` (linha de resposta em discursivas) |

### O prefixo `(BANCA - ANO)` é automático

O parser insere `(BANCA - ANO)` no início do enunciado quando `\meta{banca}`
e `\meta{ano}` estão presentes e válidos. **Não adicione manualmente.**
Se banca é `Desconhecida` ou ano é `0`, o prefixo é omitido.

---

## Regras de fidelidade

- Enunciado deve reproduzir o original **exatamente** (mesmo texto, ordem,
  formatação). Não resuma, não parafraseie, não omita.
- Siga **SKILL-segmentador.md** para identificar onde começa e termina cada
  questão e como tratar tabelas, negritos, fórmulas, etc.
- Siga **SKILL-adaptacao.md** para gerar a versão adaptada — cada adaptada é
  um bloco `\begin{questao}{A-XXXXX}...\end{questao}` logo após a regular.
  **Não herda metadados** — repita-os (ajuste apenas o que muda, como
  `dificuldade` e o próprio enunciado).

### LaTeX matemático — sem escape duplo

Aqui você escreve LaTeX **literal**:

```latex
% ✓ correto (uma barra só)
$m = 18\,\text{kg}$

% ✗ errado — não use \\ no .tex
$m = 18\\,\\text{kg}$
```

### Notação científica

```latex
$3{,}6 \times 10^{10}\,\text{Pa}$
```

### Vírgula decimal dentro de `$...$`

Use `{,}` para evitar espaçamento estranho:

```latex
$9{,}8\,\text{m/s}^2$
```

### Unidades em prosa (fora de `$...$`)

Texto comum — sem LaTeX:

```latex
\enunciado{
  Um corpo com 18 kg e velocidade de 15 m/s...
}
```

Potências em prosa: `m\textsuperscript{2}` ou, se já estiver em contexto
matemático, coloque dentro de `$...$`.

---

## Taxonomia e metadados

### `disciplina`
`Física` · `Química` · `Matemática` · `Biologia` · `Ciências` · `Geografia` ·
`História` · `Português` · `Inglês`

### `topico`
Tópico amplo. Exemplos para Física: `Mecânica`, `Termodinâmica`, `Óptica`,
`Eletromagnetismo`, `Ondulatória`, `Física Moderna`, `Energia`, `Fluidos`.

### `conteudo`
Conteúdo específico. Ex: `Cinemática`, `Leis de Newton`, `Fontes de Energia`,
`Calorimetria`.

### `assunto`
Assunto pontual. Ex: `MRU`, `Segunda Lei de Newton`, `Impactos Ambientais`,
`Calor Sensível`.

### `dificuldade`
- `facil` — uma etapa, sem cálculo complexo
- `medio` — mais de uma etapa ou conceito
- `dificil` — múltiplas etapas, integração de conceitos

### `banca` e `ano`
Ex. de bancas: `ENEM`, `FUVEST`, `UNICAMP`, `VUNESP`, `UERJ`, `ITA`, `IME`.
Ano como inteiro (ex: `2023`).

---

## Preenchimento de metadados — ordem de busca

1. **Texto do próprio documento** — cabeçalho, rodapé, enunciados.
2. **Busca na internet** com fragmento do enunciado entre aspas. Apenas sites
   oficiais (domínios `.br`, `.gov.br`, `.edu.br`, sites institucionais de
   universidades e bancas). **Nunca fóruns, blogs ou sites de gabarito**.
3. **Não encontrado** → valores padrão abaixo. **Jamais invente.**

### Sites oficiais preferenciais

| O que buscar | Sites |
|---|---|
| ENEM | `enem.inep.gov.br` |
| FUVEST | `fuvest.br` |
| UNICAMP | `comvest.unicamp.br` |
| VUNESP | `vunesp.com.br` |
| UERJ | `vestibular.uerj.br` |
| ITA / IME | `ita.br` · `ime.eb.br` |
| PUC-Rio | `puc-rio.br` |
| UEA | `uea.edu.br` |
| UEL | `uel.br` |
| FAMEMA | `famema.br` |
| FMJ | `fmj.br` |
| Outras universidades | Site institucional oficial (domínio `.br`) |

### Valores padrão quando não encontrado

| Campo | Valor |
|---|---|
| `banca` | `Desconhecida` |
| `ano` | `0` |
| `disciplina` / `topico` / `conteudo` / `assunto` | omitir `\meta{...}` ou usar string vazia |
| `dificuldade` | `medio` (padrão conservador) |

---

## Exemplo de arquivo completo

```latex
% saida/questoes.tex — gerado pelo agente
% 1 questão regular + 1 adaptada
% IDs aleatórios: 742831 (regular) e A-742831 (adaptada filha)
% O QuestBank substituirá esses IDs por sequenciais definitivos na importação.

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
    O uso de equipamentos elétricos custa dinheiro e libera carbono na
    atmosfera. Entretanto, diferentes usinas de energia apresentam custos
    econômicos e ambientais distintos.

    \imagem{Imagem1.png}

    Em relação aos custos associados às fontes energéticas apresentadas,
    a energia obtida a partir do vento é
  }

  \begin{alternativas}
    \alt{A}{mais cara que a energia nuclear e emite maior carbono.}
    \alt{B}{a segunda fonte mais cara e é livre de emissões.}
    \alt{C}{mais cara que a energia solar e ambas são livres.}
    \alt{D}{mais barata que as demais e emite grandes quantidades.}
    \alt{E}{a fonte mais barata e livre de emissões de carbono.}
  \end{alternativas}

  \gabarito{E}
\end{questao}

\begin{questao}{A-742831}
  \meta{tipo}{objetiva}
  \meta{banca}{ENEM}
  \meta{ano}{2020}
  \meta{disciplina}{Física}
  \meta{topico}{Energia}
  \meta{conteudo}{Fontes de energia}
  \meta{assunto}{Energia eólica e impacto ambiental}
  \meta{dificuldade}{facil}
  \meta{tags}{adaptada, NEE}

  \enunciado{
    \imagem{Imagem1.png}

    O gráfico acima relaciona o custo (em centavos de real) e a quantidade
    de carbono liberado por diferentes fontes de energia.

    \textbf{Analisando o gráfico, o que podemos afirmar sobre a energia
    eólica (do vento)?}
  }

  \begin{alternativas}
    \alt{A}{É a energia mais cara do gráfico e não emite carbono.}
    \alt{B}{É a energia mais barata do gráfico e não emite carbono.}
    \alt{C}{É mais barata que a nuclear, mas emite muito carbono.}
  \end{alternativas}

  \gabarito{B}
\end{questao}
```

---

## Checklist antes de entregar `saida/questoes.tex`

- [ ] Todas as questões com `\begin{questao}{ID}...\end{questao}` balanceado?
- [ ] IDs aleatórios de 6 dígitos (100000–999999), únicos dentro do arquivo?
- [ ] Cada adaptada tem prefixo `A-` seguido do mesmo número da sua regular mãe?
- [ ] Nenhum ID sequencial com zeros à esquerda (000001, 000052…)?
- [ ] Cada `\meta{}` com dois argumentos (campo e valor)?
- [ ] `\meta{tipo}` é `objetiva` ou `discursiva`?
- [ ] Objetivas têm `\begin{alternativas}` e `\gabarito{LETRA}`?
- [ ] Letra do `\gabarito` bate com uma `\alt{LETRA}{...}`?
- [ ] Discursivas têm `\gabarito{resposta}` (ou vazio)?
- [ ] Fórmulas em `$...$` ou `$$...$$` fechadas?
- [ ] Barras LaTeX únicas (sem `\\` no fonte)?
- [ ] Imagens via `\imagem{ImagemN.png}` — numeração sequencial global (`Imagem1.png`, `Imagem2.png`…)?
- [ ] Nenhuma imagem com nome descritivo (`grafico-energia.png`, etc.)?
- [ ] Questões adaptadas usam **o mesmo nome de imagem** da sua regular mãe?
- [ ] Metadados preenchidos por pesquisa (nunca inventados)?
- [ ] Não digitou `(BANCA - ANO)` manualmente (é automático)?
- [ ] Nenhum símbolo Unicode matemático no `.tex` (₀ ≈ √ ° × π…)?
- [ ] `saida/questoes.zip` gerado com `questoes.tex` + `main.tex` + imagens?
