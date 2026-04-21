# SKILL — Adaptação de Questões para Alunos Atípicos (NEE/AEE)

## O que esta skill faz

Transforma questões regulares em versões acessíveis para alunos com necessidades
educacionais especiais (NEE/AEE): TEA, TDAH, dislexia, deficiência intelectual,
entre outros.

A versão adaptada recebe o **mesmo ID aleatório com prefixo `A-`**:
- Regular `742831` → Adaptada `A-742831`

A adaptada é um **bloco LaTeX independente** (`\begin{questao}{A-XXXXX}...
\end{questao}`), colocado logo abaixo da regular no arquivo `saida/questoes.tex`.
Não há herança automática: **repita todos os metadados** no bloco adaptado
(ajustando apenas o que muda, tipicamente `dificuldade`).

---

## ⛔ REGRAS CRÍTICAS — leia antes de escrever qualquer adaptada

### A — Nunca dar dicas nem respostas

**Esta é a regra mais importante.**

O texto de contextualização de imagens, gráficos, diagramas e textos
motivadores deve **explicar o que o elemento representa**, mas **jamais**
indicar qual é a resposta correta, sugerir qual alternativa escolher ou dar
qualquer dica de raciocínio.

| ✓ Permitido | ✗ Proibido |
|---|---|
| "O gráfico mostra o custo em centavos de diferentes fontes de energia." | "O gráfico mostra que a energia eólica tem custo baixo." |
| "A tabela apresenta a velocidade e o tempo de um objeto em movimento." | "Perceba na tabela que a velocidade diminui, então o objeto desacelera." |
| "O diagrama mostra dois blocos ligados por uma corda sobre uma superfície." | "Note que o bloco menor vai puxar o maior." |
| "A figura mostra o esquema de um circuito elétrico com resistores." | "O circuito tem resistores em série, então some as resistências." |

### B — Não digite `(BANCA - ANO)` manualmente

O parser QuestBank insere automaticamente `(BANCA - ANO)` no início do
enunciado quando `\meta{banca}` e `\meta{ano}` estão preenchidos. **Nunca**
escreva o prefixo dentro de `\enunciado{...}`.

### C — LaTeX literal (sem `\\`)

No `.tex`, barras LaTeX são únicas:

```latex
% ✓ correto
$m = 2\,\text{kg}$

% ✗ errado
$m = 2\\,\\text{kg}$
```

---

## Regras obrigatórias de adaptação

### Regra 1 — Contextualizar TODOS os elementos visuais e motivadores

Para cada elemento abaixo presente na questão regular, escreva **1–2 frases**
logo depois dele explicando o que é — sem revelar a resposta nem dar pistas.

| Elemento | O que escrever |
|---|---|
| `\imagem{...}` (foto, ilustração) | O que a imagem representa no contexto da questão |
| `\imagem{...}` (gráfico) | Quais variáveis o gráfico relaciona e o que os eixos mostram |
| `\imagem{...}` (diagrama / esquema) | O que o diagrama representa (circuito, sistema, mecanismo) |
| `\imagem{...}` (tabela visual) | O que a tabela organiza (colunas e linhas) |
| `\begin{tabular}...\end{tabular}` | O que os dados da tabela representam |
| Texto motivador (trecho) | Uma frase resumindo o assunto, sem repetir o conteúdo |

**Exemplos corretos em LaTeX:**

```latex
\imagem{Imagem1.png}

O gráfico acima relaciona o custo (em centavos de real) e a quantidade de
carbono liberado por diferentes fontes de energia.
```

```latex
\imagem{Imagem2.png}

A figura representa um sistema com dois blocos conectados por uma corda sobre
uma superfície plana.
```

> **Nome de imagem na adaptada:** use **exatamente o mesmo** `\imagem{ImagemN.png}`
> da questão regular mãe — nunca crie um nome novo para a versão adaptada.

---

### Regra 2 — Manter textos motivadores, figuras e tabelas

- Textos motivadores (jornal, revista, livro, citação, charge) → **preservar
  integralmente** antes do enunciado simplificado, seguidos de contextualização.
- `\imagem{...}` → preservar, seguido de contextualização.
- Tabelas → preservar, seguidas de contextualização.

**Estrutura obrigatória do `\enunciado` adaptado:**

```
[imagem / tabela / texto motivador]
[contextualização: 1–2 frases, sem revelar resposta]
[enunciado simplificado — máx. 3 frases]
\textbf{[pergunta direta em negrito?]}
```

> Note: o prefixo `(BANCA - ANO)` é automático — NÃO digitar.

---

### Regra 3 — Enunciado curto (máx. 3 frases)

- Elimine contexto longo, dados históricos e informações periféricas.
- Mantenha apenas o essencial para entender o que está sendo pedido.
- Uma ideia por frase.

### Regra 4 — Pergunta direta e em negrito

- `\textbf{...}` obrigatório na pergunta.
- Direta, sem negações duplas, sem subordinadas complexas.
- Prefira forma afirmativa.

### Regra 5 — Apenas 3 alternativas (objetivas)

- Exatamente **3 alternativas** (`\alt{A}`, `\alt{B}`, `\alt{C}`).
- Uma é a resposta correta — nunca omita.
- Linguagem simples, sem pegadinhas, sem dupla negação, um aspecto por alternativa.
- `\gabarito{A}` / `\gabarito{B}` / `\gabarito{C}` correspondente.

### Regra 6 — Questões discursivas

- Uma pergunta única e clara.
- Se houver cálculo, explicite os dados a usar.
- Sem bloco `\begin{alternativas}`.
- `\gabarito{...}` com a resposta esperada.

### Regra 7 — Metadados iguais à regular (com exceções)

Repita: `tipo`, `banca`, `ano`, `disciplina`, `topico`, `conteudo`, `assunto`.

### Regra 8 — Metadados que mudam

| Campo | Mudança |
|---|---|
| ID do bloco | prefixo `A-`, mesmo número aleatório da regular (ex: `A-742831`) |
| `\meta{dificuldade}` | geralmente reduz um nível (`dificil` → `medio`, `medio` → `facil`) |
| `\meta{tags}` | **deixar em branco — não preencher** |
| `\enunciado{...}` | reescrito conforme esta skill |
| `\alt{...}` | 3 alternativas simplificadas (objetiva) |
| `\gabarito{...}` | A, B ou C (objetiva) ou resposta simplificada (discursiva) |

---

## Exemplo completo em LaTeX

### Regular

```latex
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

    CAVALCANTE, R. O vilão virou herói. Superinteressante, jul. 2007.

    Em relação aos custos associados às fontes energéticas apresentadas,
    a energia obtida a partir do vento é
  }

  \begin{alternativas}
    \alt{A}{mais cara que a nuclear e emite mais carbono.}
    \alt{B}{a segunda fonte mais cara e livre de carbono.}
    \alt{C}{mais cara que a solar e ambas livres de carbono.}
    \alt{D}{mais barata e emite muito carbono.}
    \alt{E}{a mais barata e livre de carbono.}
  \end{alternativas}

  \gabarito{E}
\end{questao}
```

### Adaptada

```latex
\begin{questao}{A-742831}
  \meta{tipo}{objetiva}
  \meta{banca}{ENEM}
  \meta{ano}{2020}
  \meta{disciplina}{Física}
  \meta{topico}{Energia}
  \meta{conteudo}{Fontes de energia}
  \meta{assunto}{Energia eólica e impacto ambiental}
  \meta{dificuldade}{facil}

  \enunciado{
    \imagem{Imagem1.png}

    O gráfico acima relaciona o custo (em centavos de real) e a quantidade
    de carbono liberado por diferentes fontes de energia.

    CAVALCANTE, R. O vilão virou herói. Superinteressante, jul. 2007.

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

> A contextualização explica **o que o gráfico mostra** (custo × carbono ×
> fontes), mas **não menciona** qual fonte é mais cara nem dá qualquer pista.

---

## Checklist antes de gerar cada adaptada

- [ ] ID do bloco tem prefixo `A-`?
- [ ] Todos os metadados repetidos (tipo, banca, ano, disciplina, topico, conteudo, assunto)?
- [ ] `dificuldade` reduzida ou mantida conscientemente?
- [ ] `\meta{tags}` deixado em branco (não preencher)?
- [ ] **Não** digitou `(BANCA - ANO)` dentro de `\enunciado{}`?
- [ ] Cada `\imagem{}` usa o **mesmo nome** (`Imagem1.png`, etc.) da questão regular mãe?
- [ ] Cada `\imagem{}`, tabela ou texto motivador tem contextualização de 1–2 frases?
- [ ] A contextualização **não revela a resposta nem dá pistas de raciocínio**?
- [ ] Enunciado simplificado tem no máximo 3 frases?
- [ ] Pergunta em `\textbf{...}`?
- [ ] Exatamente 3 alternativas (A, B, C) nas objetivas?
- [ ] `\gabarito{...}` bate com uma `\alt{...}` existente?
- [ ] Barras LaTeX únicas (sem `\\`)?
