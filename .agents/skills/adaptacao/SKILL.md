---
name: adaptacao
description: >
  Gera a versão adaptada (NEE/AEE) de cada questão regular no formato LaTeX
  do QuestBank. Use esta skill no Passo 3 do workflow, imediatamente após
  escrever o bloco regular, para criar o bloco \begin{questao}{A-NNNNNN}.
  Aplica simplificação de enunciado (máx. 3 frases), contextualização de
  imagens/tabelas sem revelar resposta, 3 alternativas e pergunta em negrito.
  Ativar também quando o usuário pedir "versão adaptada", "questão para NEE",
  "adaptação para aluno com laudo" ou similar.
---

# Adaptação de Questões para Alunos Atípicos (NEE/AEE)

## Objetivo

Transformar cada questão regular em uma versão acessível para alunos com
necessidades educacionais especiais (TEA, TDAH, dislexia, deficiência
intelectual, entre outros), seguindo as regras abaixo sem comprometer o
conteúdo avaliado.

A adaptada recebe o **mesmo ID aleatório com prefixo `A-`**:
- Regular `742831` → Adaptada `A-742831`

## Entradas esperadas

- Bloco regular já escrito no `questoes.tex` (com ID, metadados, enunciado, alternativas e gabarito)
- Imagens: mesmos nomes da regular mãe (`Imagem1.png`, etc.)

## Saída esperada

Bloco `\begin{questao}{A-NNNNNN}...\end{questao}` imediatamente após a regular,
com enunciado simplificado (máx. 3 frases), 3 alternativas e `\gabarito{A|B|C}`.

## Passo a passo

1. Copiar todos os `\meta{}` da regular, reduzindo `dificuldade` em um nível.
2. Preservar imagens, tabelas e textos motivadores; contextualizar cada um (1–2 frases, sem revelar resposta).
3. Reescrever o enunciado em no máximo 3 frases simples.
4. Formular pergunta direta em `\textbf{...}`.
5. Criar exatamente 3 alternativas (`A`, `B`, `C`) com linguagem simples — uma é a correta.
6. Preencher `\gabarito{}` com a letra correspondente à alternativa correta.
7. **Não** preencher `\meta{tags}` — deixar vazio.

---

## ⛔ REGRA CRÍTICA — nunca dar dicas nem respostas

A contextualização de imagens, gráficos e textos deve **explicar o elemento**,
mas **jamais** indicar a resposta ou sugerir raciocínio.

| ✓ Permitido | ✗ Proibido |
|---|---|
| "O gráfico mostra o custo em centavos de diferentes fontes de energia." | "O gráfico mostra que a energia eólica tem custo baixo." |
| "A tabela apresenta velocidade e tempo de um objeto em movimento." | "Perceba que a velocidade diminui — o objeto desacelera." |
| "O diagrama mostra dois blocos ligados por uma corda." | "Note que o bloco menor vai puxar o maior." |

---

## Regras de adaptação

### Regra 1 — Contextualizar TODOS os elementos visuais e motivadores

Para cada elemento abaixo, escreva **1–2 frases** logo depois dele:

| Elemento | O que escrever |
|---|---|
| `\imagem{...}` (foto, ilustração) | O que a imagem representa no contexto |
| `\imagem{...}` (gráfico) | Quais variáveis o gráfico relaciona |
| `\imagem{...}` (diagrama / esquema) | O que o diagrama representa |
| `\imagem{...}` (tabela visual) | O que a tabela organiza |
| `\begin{tabular}...\end{tabular}` | O que os dados representam |
| Texto motivador (trecho) | Uma frase resumindo o assunto, sem repetir |

```latex
% Exemplo correto:
\imagem{Imagem1.png}

O gráfico acima relaciona o custo (em centavos de real) e a quantidade de
carbono liberado por diferentes fontes de energia.
```

### Regra 2 — Manter textos motivadores, figuras e tabelas

- Textos motivadores → **preservar integralmente** antes do enunciado simplificado
- `\imagem{...}` → preservar, seguido de contextualização
- Tabelas → preservar, seguidas de contextualização

**Estrutura obrigatória do `\enunciado` adaptado:**

```
[imagem / tabela / texto motivador]
[contextualização: 1–2 frases, sem revelar resposta]
[enunciado simplificado — máx. 3 frases]
\textbf{[pergunta direta em negrito?]}
```

### Regra 3 — Enunciado curto (máx. 3 frases)

Elimine contexto longo, dados históricos e informações periféricas.
Mantenha apenas o essencial. Uma ideia por frase.

### Regra 4 — Pergunta direta e em negrito

- `\textbf{...}` obrigatório na pergunta
- Sem negações duplas, sem subordinadas complexas
- Prefira forma afirmativa

### Regra 5 — Apenas 3 alternativas (objetivas)

Exatamente `\alt{A}`, `\alt{B}`, `\alt{C}` — uma delas é a resposta correta.
Linguagem simples, sem pegadinhas, um aspecto por alternativa.
`\gabarito{A}` / `\gabarito{B}` / `\gabarito{C}` correspondente.

### Regra 6 — Questões discursivas

Uma pergunta única e clara. Se houver cálculo, explicite os dados.
Sem `\begin{alternativas}`. `\gabarito{...}` com a resposta esperada.

### Regra 7 e 8 — Metadados

Repita: `tipo`, `banca`, `ano`, `disciplina`, `topico`, `conteudo`, `assunto`.

| Campo | Mudança na adaptada |
|---|---|
| ID do bloco | prefixo `A-`, mesmo número da regular |
| `\meta{dificuldade}` | reduz um nível (`dificil`→`medio`, `medio`→`facil`) |
| `\meta{tags}` | **deixar em branco — não preencher** |
| `\enunciado{...}` | reescrito conforme esta skill |
| `\alt{...}` | 3 alternativas simplificadas (objetiva) |
| `\gabarito{...}` | A, B ou C (objetiva) ou resposta simplificada |

---

## Exemplo completo

```latex
% Regular
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
    atmosfera. Entretanto, diferentes usinas apresentam custos distintos.

    \imagem{Imagem1.png}

    Em relação aos custos, a energia obtida a partir do vento é
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

% Adaptada — mesmo ID com prefixo A-
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

    \textbf{Analisando o gráfico, o que podemos afirmar sobre a
    energia eólica (do vento)?}
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

## Checklist antes de gerar cada adaptada

- [ ] ID com prefixo `A-` e mesmo número da regular?
- [ ] Todos os metadados repetidos (tipo, banca, ano, disciplina, topico, conteudo, assunto)?
- [ ] `dificuldade` reduzida ou mantida conscientemente?
- [ ] `\meta{tags}` deixado em branco?
- [ ] `(BANCA - ANO)` **não** digitado no `\enunciado`?
- [ ] Cada `\imagem{}` usa o **mesmo nome** da regular mãe (`Imagem1.png`, etc.)?
- [ ] Cada `\imagem{}`, tabela ou texto motivador tem contextualização de 1–2 frases?
- [ ] A contextualização **não revela a resposta nem dá pistas**?
- [ ] Enunciado tem no máximo 3 frases?
- [ ] Pergunta em `\textbf{...}`?
- [ ] Exatamente 3 alternativas (A, B, C) nas objetivas?
- [ ] `\gabarito{...}` bate com uma `\alt{...}` existente?
- [ ] Barras LaTeX únicas (sem `\\`)?
