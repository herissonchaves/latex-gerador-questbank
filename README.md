# Conversor de Questões → LaTeX QuestBank (Antigravity)

Converte provas em **PDF, Word ou imagens** em questões no **formato LaTeX do
QuestBank** (`.tex`), gerando automaticamente a versão **regular** e a versão
**adaptada (NEE/AEE)** de cada questão.

O entregável final é **`saida/questoes.zip`** — um ZIP dual-compatível:

| Sistema | O que usa | Como usa |
|---|---|---|
| **QuestBank** (app local) | `questoes.tex` | Servidor `questbank-server` converte `.tex` → JSON na importação |
| **Overleaf** (compilador online) | `main.tex` | Compila com pdflatex; `\input{questoes}` inclui as questões |

> O agente **não** gera JSON. O único formato de questões é o `.tex` (DSL do QuestBank).

---

## Por que LaTeX em vez de JSON?

- **Edição confortável** em qualquer editor antes de importar.
- **Backslash único** (`\frac`, `\text`) — sem o inferno de `\\` do JSON.
- **Fórmulas legíveis** e diff amigável no git.
- **Comentários** (`%`) permitidos — úteis para notas.
- **Imagens** por caminho relativo (`\imagem{grafico.png}`).

---

## Estrutura do projeto

```
conversor-questoes-questbank/
├── AGENT.md               ← orquestração do agente Antigravity
├── README.md              ← este arquivo
├── SKILL-latex.md         ← formato .tex + taxonomia + regras de metadados
├── SKILL-segmentador.md   ← como segmentar questões do texto extraído
├── SKILL-adaptacao.md     ← regras de adaptação NEE/AEE em LaTeX
├── construtor.py          ← extrator de texto (PDF/DOCX/imagem/HTML)
├── main.tex               ← wrapper LaTeX padrão para compilação no Overleaf
├── entrada/               ← coloque aqui seus arquivos de prova
└── saida/
    ├── questoes.tex       ← DSL QuestBank (gerado pelo agente)
    ├── main.tex           ← cópia do wrapper (gerada pelo agente)
    └── questoes.zip       ← entregável final (gerado pelo agente)
```

---

## Como usar

### 1. Configurar no Antigravity
- Crie um novo projeto no Google Antigravity.
- Faça upload de todos os arquivos desta pasta.

### 2. Adicionar as provas
- Coloque PDFs, DOCXs, imagens ou HTMLs na pasta `entrada/`.

### 3. Iniciar
No chat do Antigravity, basta dizer:

Leia o AGENT.md. Converta os arquivos da pasta entrada em questões LaTeX para o QuestBank.

Não é necessário informar nenhum ID — o agente gera IDs aleatórios automaticamente.

### 4. Resultado
- `saida/questoes.zip` — entregável final, dual-compatível com QuestBank e Overleaf.
- O ZIP contém `questoes.tex`, `main.tex` e todas as imagens encontradas.
- Questões com `\imagem{...}` cujos arquivos não foram localizados aparecem
  listadas no log; adicione as imagens ao ZIP manualmente antes de importar.

### 5. Importar no QuestBank
- Rode o servidor local `questbank-server`.
- No app, arraste `saida/questoes.zip` para o importador.
- O app extrai o `.tex`, envia ao servidor Python, converte para JSON, insere
  `(BANCA - ANO)` automaticamente e substitui os IDs aleatórios por IDs
  sequenciais definitivos a partir do último ID do banco.

### 5b. Abrir no Overleaf (opcional)
- Acesse overleaf.com → New Project → Upload Project.
- Envie `saida/questoes.zip`.
- O Overleaf compilará `main.tex` automaticamente → PDF com todas as questões.

---

## IDs das questões

O agente gera **IDs aleatórios de 6 dígitos** (100000–999999) para cada par
regular + adaptada. Os IDs são temporários — o QuestBank os substitui por
sequenciais definitivos a partir do último ID cadastrado no banco durante a
importação.

| Questão | ID no `.tex` (temporário) | ID após importação (definitivo) |
|---|---|---|
| Regular nº 1 | `742831` (aleatório) | sequencial do banco |
| Adaptada nº 1 | `A-742831` | `A` + ID da regular |
| Regular nº 2 | `193057` (aleatório) | sequencial do banco |
| Adaptada nº 2 | `A-193057` | `A` + ID da regular |

O prefixo `A-` é o sinal que o QuestBank usa para reconhecer a relação
filha-mãe entre a adaptada e a regular durante a importação.

---

## Formatos de arquivo suportados (entrada)

| Formato | Extensão | Texto extraído | Imagens |
|---|---|---|---|
| PDF | `.pdf` | ✅ | `[IMAGEM]` → `\imagem{...}` |
| Word | `.docx` `.doc` | ✅ | `[IMAGEM]` → `\imagem{...}` |
| Imagem | `.png` `.jpg` `.jpeg` etc. | OCR (Tesseract) | `[IMAGEM]` → `\imagem{...}` |
| HTML | `.html` `.htm` | ✅ | `[IMAGEM]` → `\imagem{...}` |

---

## Dependências Python (instaladas pelo `construtor.py`)

- `pymupdf` — extração fiel de PDF
- `python-docx` + `lxml` — leitura de DOCX (negrito, itálico, tabelas, equações)
- `beautifulsoup4` — HTML
- `pytesseract` — OCR
- `Pillow` — imagens
- `opencv-python-headless` + `numpy` — pré-processamento (CLAHE, Otsu)

## Dependência de sistema

- **Tesseract OCR** com pacote `por` (português):
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: `brew install tesseract tesseract-lang`
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-por`

O `construtor.py` detecta o Tesseract nos caminhos padrão (Program Files,
Homebrew, `/usr/bin`).

---

## Exemplo mínimo de saída (`questoes.tex`)

```latex
% ID 742831 foi gerado aleatoriamente para este par de questões.
% O QuestBank substituirá por ID sequencial definitivo na importação.

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
    O uso de equipamentos elétricos custa dinheiro e libera carbono.

    \imagem{grafico-energia.png}

    Em relação aos custos, a energia obtida a partir do vento é
  }

  \begin{alternativas}
    \alt{A}{mais cara que a nuclear.}
    \alt{B}{a segunda mais cara.}
    \alt{C}{mais cara que a solar.}
    \alt{D}{a mais barata e poluente.}
    \alt{E}{a mais barata e livre de emissões.}
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
  \meta{assunto}{Energia eólica}
  \meta{dificuldade}{facil}
  \meta{tags}{adaptada, NEE}

  \enunciado{
    \imagem{grafico-energia.png}

    O gráfico relaciona o custo e o carbono liberado por fontes de energia.

    \textbf{O que o gráfico indica sobre a energia eólica (do vento)?}
  }

  \begin{alternativas}
    \alt{A}{É a mais cara e não emite carbono.}
    \alt{B}{É a mais barata e não emite carbono.}
    \alt{C}{É mais barata que a nuclear, mas emite carbono.}
  \end{alternativas}

  \gabarito{B}
\end{questao}
```

O parser transforma o `questoes.tex` em HTML com `(ENEM - 2020)` já no início do enunciado.
# latex-gerador-questbank
