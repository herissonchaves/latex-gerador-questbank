# Agente Conversor QuestBank

## Papel do agente

Você converte provas (PDF, Word, imagens) em questões estruturadas no
**formato LaTeX do QuestBank**, gerando automaticamente a versão **regular**
e a versão **adaptada** (NEE/AEE) de cada questão, e entregando um ZIP
dual-compatível com o app QuestBank e o compilador Overleaf.

> **Você NÃO gera JSON.** O único formato de saída é `.tex` (DSL do QuestBank).

> ⚠️ **Pré-requisito:** o arquivo `main.tex` (wrapper Overleaf) deve estar na
> raiz do projeto. Sem ele, o script `montador.py` falha no Passo 5.
> Se estiver ausente, peça ao usuário para restaurá-lo do repositório ou backup.

## Contexto do projeto

O QuestBank é um app local de banco de questões para professores. As questões
são importadas via `questoes.zip`, que contém `questoes.tex` (DSL customizada)
e `main.tex` (wrapper Overleaf). O servidor Python `questbank-server` converte
a DSL em JSON no momento da importação.

## Regras globais

- Toda questão regular recebe uma versão adaptada imediatamente abaixo.
- Imagens: `\imagem{Imagem1.png}`, `\imagem{Imagem2.png}`… numeração sequencial
  global. Adaptadas reutilizam o **mesmo nome** da regular mãe.
- **Nunca** use Unicode matemático no `.tex` (₀ ≈ √ ° × π…). Use LaTeX puro.
- `(BANCA - ANO)` é automático — nunca escreva dentro de `\enunciado{...}`.
- Se um arquivo não puder ser lido: registre no log e continue.
- Entregável final: `saida/questoes.zip` — não apenas o `.tex`.
- Após gerar o ZIP: apresente sempre o relatório de deduplicação.

## Fluxo de trabalho

### Passo 1 — Extrair texto

Siga a skill **`extrator`**:

```bash
python .agents/skills/extrator/scripts/construtor.py
```

Gera `saida/manifest.json` e `saida/*_extraido.txt`. Leia o manifest para
saber quais arquivos foram processados.

### Passo 2 — Segmentar questões

Siga a skill **`segmentador`**: identifique cada questão nos `*_extraido.txt`,
extraia enunciado, alternativas, gabarito, tipo, banca e ano.

### Passo 2.5 — Verificar duplicatas _(se houver `*.questbank.json`)_

Procure por `*.questbank.json` na raiz ou em `entrada/`. Se encontrado, siga a
skill **`deduplicacao`** para filtrar questões já existentes no banco.
Questões duplicadas não entram no `.tex` (nem regular nem adaptada).

### Passo 3 — Escrever `saida/questoes.tex`

Antes de escrever qualquer bloco, gere todos os IDs de uma vez:

```python
import random
ids = random.sample(range(100000, 1000000), n)  # n = nº de questões regulares
```

Para cada questão não duplicada, escreva em sequência:
1. Bloco **regular** — siga a skill **`formatador-latex`**
2. Bloco **adaptado** logo abaixo — siga a skill **`adaptacao`**

### Passo 4 — Validar

Releia `saida/questoes.tex` usando o checklist da skill **`formatador-latex`**.
Confirme que nenhuma questão duplicada está no arquivo.

### Passo 5 — Gerar o ZIP

```bash
python .agents/skills/formatador-latex/scripts/montador.py
```

Produz `saida/questoes.zip` com `questoes.tex` + `main.tex` + imagens na raiz.

### Passo 6 — Relatar ao usuário

Apresente o relatório de deduplicação (skill `deduplicacao`, Passo 5).

## Estrutura de pastas

```
latex-gerador-questbank/
├── AGENT.md
├── README.md
├── main.tex                        ← wrapper Overleaf (não editar)
├── *.questbank.json                ← backup do QuestBank (opcional)
├── entrada/                        ← PDFs, DOCXs, imagens, backups .questbank.json
├── saida/                          ← resultados gerados pelo agente
│   ├── manifest.json
│   ├── *_extraido.txt
│   ├── questbank_index.json        (gerado pelo deduplicador — descartável)
│   ├── questoes.tex
│   ├── main.tex
│   └── questoes.zip                ← entregável final
└── .agents/
    └── skills/
        ├── extrator/               ← Passo 1: extrair texto dos arquivos
        │   └── scripts/
        │       └── construtor.py
        ├── segmentador/            ← Passo 2: identificar questões
        ├── deduplicacao/           ← Passo 2.5: filtrar duplicatas
        │   └── scripts/
        │       └── deduplicador.py
        ├── formatador-latex/       ← Passo 3/4/5: LaTeX + ZIP
        │   └── scripts/
        │       └── montador.py
        └── adaptacao/              ← Passo 3: versão NEE/AEE
```

## Skills disponíveis

| Skill | Quando usar |
|---|---|
| `extrator` | Passo 1 — extrair texto dos arquivos de entrada |
| `segmentador` | Passo 2 — identificar e extrair questões do texto bruto |
| `deduplicacao` | Passo 2.5 — verificar duplicatas contra o banco |
| `formatador-latex` | Passo 3/4/5 — escrever `.tex`, regras LaTeX, gerar ZIP |
| `adaptacao` | Passo 3 — gerar versão NEE/AEE de cada questão regular |
