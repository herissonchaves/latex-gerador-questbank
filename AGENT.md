# Agente Conversor QuestBank — Saída LaTeX (`.tex`)

## Missão
Você é um agente especialista em converter provas (**PDF, Word, imagens**) em
questões estruturadas no **formato LaTeX do QuestBank**, gerando automaticamente
a versão **regular** e a versão **adaptada** (NEE/AEE) de cada questão.

O **entregável final é `saida/questoes.zip`** — um arquivo ZIP dual-compatível:

| Sistema | Como usa o ZIP |
|---|---|
| **QuestBank** (app local) | Lê `questoes.tex` via servidor `questbank-server` → importa JSON |
| **Overleaf** (compilador LaTeX online) | Compila `main.tex`, que faz `\input{questoes}` |

> **Você NÃO gera JSON.** O único formato de questões é o `.tex` (DSL do QuestBank).

---

## Divisão de responsabilidades

| Tarefa | Quem faz |
|---|---|
| Extrair texto dos arquivos | `construtor.py` |
| Identificar e segmentar questões | **Agente** |
| Preencher metadados (banca, ano, disciplina…) | **Agente** (pesquisa na internet se necessário) |
| Escrever enunciados em **LaTeX puro** | **Agente** |
| Adaptar questões para NEE/AEE | **Agente** |
| Gerar IDs aleatórios únicos (par regular + adaptada) | **Agente** |
| Salvar `saida/questoes.tex` | **Agente** |
| Copiar `main.tex` para `saida/main.tex` | **Agente** |
| Gerar `saida/questoes.zip` (ZIP dual-compatível) | **Agente** (via script Python) |

---

## Fluxo de trabalho

### Passo 1 — Executar o extrator
```bash
python construtor.py
```
Gera `saida/manifest.json` e arquivos `saida/*_extraido.txt` a partir dos
arquivos em `entrada/` (PDF, DOCX, imagens, HTML).

Leia o `manifest.json` para saber quais arquivos foram processados.

### Passo 2 — Segmentar as questões
Para cada `*_extraido.txt`, identifique cada questão seguindo a
**SKILL-segmentador.md** — inclui as regras de fidelidade obrigatórias
(negrito, itálico, tabelas, fórmulas, imagens, gabarito).

### Passo 3 — Escrever `saida/questoes.tex`

#### Geração de IDs aleatórios

Cada par regular + adaptada compartilha um **ID aleatório de 6 dígitos**,
gerado exclusivamente para esse par. O app QuestBank usa o prefixo `A-` para
reconhecer que uma questão é a versão adaptada filha da questão regular com
o mesmo número, e depois substitui ambos os IDs por IDs sequenciais definitivos
com base no último ID já cadastrado no banco.

**Regra de geração:**

1. Antes de escrever qualquer bloco, gere a lista completa de IDs aleatórios —
   um por questão regular. Use o script Python abaixo ou gere mentalmente números
   de 6 dígitos (100000–999999) sem repetição dentro do mesmo arquivo.

   ```python
   import random
   n = <número de questões regulares>
   ids = random.sample(range(100000, 1000000), n)
   # exemplo: [742831, 193057, 856402, ...]
   ```

2. Atribua um ID a cada questão regular na ordem em que aparecem no arquivo.

3. A versão adaptada da mesma questão recebe **exatamente o mesmo número com
   o prefixo `A-`**.

**Exemplo com 3 questões:**

| Questão | ID no `.tex` |
|---|---|
| Regular nº 1 | `742831` |
| Adaptada nº 1 | `A-742831` |
| Regular nº 2 | `193057` |
| Adaptada nº 2 | `A-193057` |
| Regular nº 3 | `856402` |
| Adaptada nº 3 | `A-856402` |

> **Por que aleatório?**  
> Os IDs no `.tex` são temporários — o QuestBank os descarta após a importação
> e atribui IDs sequenciais definitivos a partir do último ID do banco.  
> O número aleatório serve apenas para vincular a filha adaptada à sua mãe
> regular durante a importação. Usando números aleatórios, evita-se colisão
> com IDs já existentes no banco e elimina-se a necessidade de perguntar ao
> usuário qual é o próximo ID disponível.

---

Para cada questão, escreva no arquivo:

1. O bloco **regular** seguindo a **SKILL-latex.md**:

   ```latex
   \begin{questao}{742831}
     \meta{tipo}{objetiva}
     \meta{banca}{...}
     \meta{ano}{...}
     \meta{disciplina}{...}
     \meta{topico}{...}
     \meta{conteudo}{...}
     \meta{assunto}{...}
     \meta{dificuldade}{...}

     \enunciado{ ... }

     \begin{alternativas}
       \alt{A}{...}
       \alt{B}{...}
       ...
     \end{alternativas}

     \gabarito{LETRA}
   \end{questao}
   ```

2. Logo abaixo, o bloco **adaptado** seguindo a **SKILL-adaptacao.md**:

   ```latex
   \begin{questao}{A-742831}
     ... (metadados repetidos, enunciado simplificado, 3 alternativas)
   \end{questao}
   ```

3. Concatene todos os pares regular+adaptada em **um único arquivo**
   `saida/questoes.tex`.

#### Regras essenciais de conteúdo

- **Fidelidade obrigatória**: o enunciado da regular reproduz o original
  exatamente — mesmo texto, mesma formatação, mesma ordem dos elementos.
  Consulte a tabela de fidelidade em **SKILL-segmentador.md**.
- **LaTeX puro**, não HTML. Toda `\` é única (sem `\\` do JSON).
- **`(BANCA - ANO)` é automático** — o parser insere a partir de `\meta{banca}`
  e `\meta{ano}`. NÃO digite manualmente no `\enunciado`.
- **Imagens** → `\imagem{ImagemN.png}` com **numeração sequencial global**
  (`Imagem1.png`, `Imagem2.png`…). Nunca use nomes descritivos.
  Questões adaptadas reutilizam o mesmo nome da regular mãe.
  O usuário repõe os arquivos físicos com esses nomes depois.
- **Tabelas de dados** → `\begin{tabular}{...}...\end{tabular}`.
- **Textos motivadores** (citação, trecho de jornal/revista) → preserve
  integralmente antes do enunciado e mantenha a referência bibliográfica.
- **Metadados**: (1) leia o texto extraído, (2) se necessário pesquise em
  sites oficiais listados na SKILL-latex.md (ou outros `.br`, `.gov.br`,
  `.edu.br`, institucionais) — nunca em fóruns ou blogs de gabarito, (3) se
  não encontrar, use os padrões (`Desconhecida`, `0`). **Jamais invente.**

### Passo 4 — Validar
Releia `saida/questoes.tex` conferindo o **checklist final da SKILL-latex.md**
(blocos balanceados, IDs únicos e aleatórios, prefixo `A-` nas adaptadas,
gabaritos consistentes, barras simples, etc.)
antes de prosseguir para o Passo 5.

### Passo 5 — Gerar o ZIP dual-compatível

Execute o script abaixo para criar `saida/questoes.zip`:

```python
import zipfile, os, re, shutil

TEX_PATH  = 'saida/questoes.tex'
MAIN_SRC  = 'main.tex'          # template na raiz do projeto
MAIN_DEST = 'saida/main.tex'
ZIP_PATH  = 'saida/questoes.zip'

# 1. Copiar main.tex (wrapper Overleaf) para saida/
shutil.copy(MAIN_SRC, MAIN_DEST)

# 2. Encontrar imagens referenciadas em questoes.tex
with open(TEX_PATH, encoding='utf-8') as f:
    tex = f.read()

imagens = list(dict.fromkeys(re.findall(r'\\imagem\{([^}]+)\}', tex)))

# 3. Localizar arquivos de imagem (busca em pastas comuns)
SEARCH_DIRS = ['.', 'saida', 'entrada', 'imagens']
found_imgs   = {}   # basename → caminho real
missing_imgs = []

for img in imagens:
    basename = os.path.basename(img)
    for d in SEARCH_DIRS:
        for candidate in [os.path.join(d, img), os.path.join(d, basename)]:
            if os.path.exists(candidate):
                found_imgs[basename] = candidate
                break
        if basename in found_imgs:
            break
    else:
        missing_imgs.append(img)

# 4. Montar o ZIP
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(TEX_PATH,  'questoes.tex')   # DSL QuestBank (lido pelo app)
    zf.write(MAIN_DEST, 'main.tex')       # wrapper Overleaf (entrada do compilador)
    for basename, path in found_imgs.items():
        zf.write(path, basename)           # imagens na raiz do ZIP

print(f"✓ ZIP criado: {ZIP_PATH}")
print(f"  questoes.tex + main.tex + {len(found_imgs)} imagem(ns)")
if missing_imgs:
    print(f"\n⚠ Imagens NÃO encontradas ({len(missing_imgs)}) — adicione ao ZIP manualmente:")
    for m in missing_imgs:
        print(f"  - {m}")
```

> **Regra de caminhos de imagem no ZIP**
> Todas as imagens ficam na **raiz do ZIP** (sem subpastas).
> Em `questoes.tex` use sempre `\imagem{nome-do-arquivo.png}` — nunca
> `\imagem{pasta/nome.png}`.  
> O `main.tex` usa `\includegraphics{nome-do-arquivo.png}`, que acha a imagem
> na mesma pasta do `.tex` — compatível com Overleaf e com o parser do QuestBank.

---

## Regras gerais

- Toda questão regular recebe uma versão adaptada imediatamente abaixo.
- Se um arquivo de entrada não puder ser lido, registre no log e continue com
  os demais.
- O entregável final é **`saida/questoes.zip`** — não apenas o `.tex`.
- **NUNCA use símbolos Unicode matemáticos** em `questoes.tex` (₀, ≈, √, °, ×…).
  Use sempre LaTeX puro: `$_0$`, `$\approx$`, `$\sqrt{}$`, `$^{\circ}$`, `$\times$`.
  Unicode matemático causa erros de compilação no Overleaf e pode corromper a importação.

---

## Estrutura de pastas

```
conversor-questoes-questbank/
├── AGENT.md               ← este arquivo
├── README.md              ← visão geral e instruções de uso
├── SKILL-latex.md         ← formato .tex + taxonomia + regras de metadados
├── SKILL-segmentador.md   ← como identificar questões no texto extraído
├── SKILL-adaptacao.md     ← regras de adaptação NEE/AEE em LaTeX
├── construtor.py          ← Passo 2: extrai texto dos arquivos
├── main.tex               ← wrapper Overleaf (template — não editar)
├── entrada/               ← coloque aqui PDFs, DOCXs e imagens de prova
└── saida/
    ├── manifest.json          (gerado pelo construtor.py)
    ├── *_extraido.txt         (gerado pelo construtor.py)
    ├── questoes.tex           (gerado pelo agente no Passo 3)
    ├── main.tex               (copiado do template no Passo 5)
    └── questoes.zip           (gerado pelo agente no Passo 5) ← entregável final
```

### Conteúdo do ZIP (`saida/questoes.zip`)

```
questoes.zip/
  questoes.tex   ← DSL QuestBank (parser Python lê este arquivo)
  main.tex       ← wrapper LaTeX padrão (Overleaf compila este arquivo)
  imagem1.png    ← imagens na raiz (mesma pasta dos .tex)
  imagem2.png
  ...
```
