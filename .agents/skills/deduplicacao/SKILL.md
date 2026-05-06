---
name: deduplicacao
description: >
  Verifica se questões dos arquivos de entrada já existem no banco QuestBank
  antes de incluí-las no questoes.tex. Use esta skill no Passo 2.5 do workflow,
  SEMPRE — é obrigatória. O agente procura automaticamente o .questbank.json
  mais recente na pasta backup/ e constrói o índice. Se a pasta estiver vazia,
  avisa o usuário e segue sem deduplicação. Executa deduplicador.py para
  verificar as questões segmentadas (modo batch para lotes >5, single-shot
  para casos pontuais), excluindo duplicatas do .tex e gerando relatório final.
---

# Deduplicação contra o Banco QuestBank

## Objetivo

Evitar que questões já cadastradas no app QuestBank sejam exportadas novamente.
Questões identificadas como duplicatas são silenciosamente excluídas do
`questoes.tex` (regular + adaptada) e listadas no relatório final ao usuário.

## Entradas esperadas

- `*.questbank.json` mais recente em **`backup/`** (backup exportado pelo app QuestBank)
- Lista de questões segmentadas (Passo 2) — enunciado em texto puro, banca e ano de cada questão

> **Localização canônica do backup:** `backup/`. Não procure em outros lugares.
> O usuário foi orientado a depositar sempre o backup mais recente nessa pasta.

## Saída esperada

- `saida/questbank_index.json` — índice temporário das questões do banco
- Lista de questões filtradas: `NOVA` (incluir no `.tex`) vs `DUPLICATA:<id>` (excluir)
- Relatório final com contagem de inclusões e duplicatas

---

## Passo a passo

### Passo 1 — Localizar o backup em `backup/`

O caminho canônico é a pasta `backup/` na raiz do projeto. O script faz a
descoberta automaticamente — basta rodar `build` sem argumento (próximo passo).

Para auditar manualmente antes:

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py discover
```

Saídas possíveis:

| Resultado | Ação |
|---|---|
| Imprime o caminho do backup mais recente | Continue para o Passo 2 |
| Sai com erro "nenhum *.questbank.json em backup/" | **Avise o usuário** que a deduplicação será pulada e siga direto para o Passo 3 do workflow principal (formatador-latex), incluindo todas as questões |

### Passo 2 — Construir o índice

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py build
```

Sem argumento, o script usa o backup mais recente em `backup/`.
(Para casos especiais, é possível passar um caminho explícito.)

Gera `saida/questbank_index.json`. Verifique se o número de questões indexadas
bate com o campo `stats.questions` do JSON de backup.

### Passo 3 — Verificar todas as questões em uma única chamada (preferido)

Para qualquer lote com **mais de 5 questões**, use o modo batch — uma única
chamada Python classifica todas de uma vez, evitando N cold starts.

**Monte um JSON com todas as questões segmentadas:**

```json
[
  {"ref": "q1", "banca": "ENEM",   "ano": "2020", "trecho": "Um dos animais..."},
  {"ref": "q2", "banca": "FUVEST", "ano": "2019", "trecho": "Considere o sistema..."},
  {"ref": "q3", "banca": "UECE",   "ano": "0",    "trecho": "Em uma corda..."}
]
```

`ref` é um identificador interno seu (ex: índice da questão). `trecho` deve
ter os primeiros 100–150 caracteres do enunciado em texto puro, sem LaTeX
nem HTML, sem incluir a banca/ano.

**Execute:**

```bash
echo '<JSON acima>' | python .agents/skills/deduplicacao/scripts/deduplicador.py check-batch
```

Ou salve em arquivo e use redirect:

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py check-batch < /tmp/lote.json
```

**Saída (JSON no stdout):**

```json
[
  {"ref": "q1", "status": "DUPLICATA", "id_banco": "00042"},
  {"ref": "q2", "status": "NOVA"},
  {"ref": "q3", "status": "DUPLICATA", "id_banco": "00117"}
]
```

### Passo 3 (alternativo) — Modo single-shot

Para uma única questão (ou debug pontual), use o modo individual:

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py check "<banca>" "<ano>" "<trecho>"
```

| Saída no stdout | Ação |
|---|---|
| `NOVA` | Incluir normalmente no `.tex` |
| `DUPLICATA:00042` | **Não incluir** — registrar na lista de ignoradas |

### Passo 4 — Registrar duplicatas

Mantenha uma lista durante o processamento:
- Não gere o bloco regular nem o bloco adaptado de questões duplicadas.
- Continue processando as demais normalmente.

### Passo 5 — Relatório final

Apresente após o ZIP:

```
📦 questoes.zip gerado com sucesso.

✅ X questões incluídas.

⚠️ Y questões ignoradas (já existem no banco):
  • Questão 1 (ENEM 2020) → já cadastrada como id 00042
  • Questão 5 (FUVEST 2019) → já cadastrada como id 00117
```

Se não houver duplicatas: `✅ X questões incluídas. Nenhuma duplicata encontrada.`

---

## Regras e restrições

- Se o script falhar (erro Python, arquivo corrompido): avise o usuário e
  continue **sem** deduplicação — não interrompa o processamento.
- `saida/questbank_index.json` é descartável — não versionado.
- A comparação usa: `banca normalizada | ano | primeiros 120 chars do texto`.

### Como a chave de comparação é gerada (ordem obrigatória)

> ⚠️ Alterar essa ordem reintroduz bugs conhecidos — não modifique sem entender o motivo.

1. **`strip_html()` primeiro** — remove tags HTML do enunciado bruto *antes* de qualquer regex.
   O banco armazena enunciados com HTML (`<p>`, `<b>`, etc.). Se o HTML não for removido primeiro,
   o regex de prefixo `(BANCA - ANO)` falha porque encontra `<p>(FAMEMA - 2020)</p>` em vez de
   `(FAMEMA - 2020)` no início da string.

2. **Regex de prefixo depois** — remove `(BANCA - ANO)` e `(BANCA)` do início do texto já limpo.

3. **`normalizar()` por último** — lowercase e remoção de pontuação sobre o texto já sem prefixo.

### Tolerância de ano desconhecido

Quando o PDF não traz o ano da questão, o agente registra `ano = "0"`. O script trata `"0"` e
`""` como **"ano desconhecido"** em ambos os lados da comparação: se qualquer um dos dois for
`"0"` ou vazio, o critério de ano é ignorado e a detecção cai apenas sobre banca + texto.

Isso evita falsos negativos do tipo: questão com `ano=0` na entrada vs `ano=2020` no banco.

## Checklist

- [ ] `discover` executado para confirmar a presença de backup em `backup/`?
- [ ] Se backup ausente: usuário avisado e workflow seguiu sem deduplicação?
- [ ] Se backup presente: `deduplicador.py build` executado com sucesso?
- [ ] Contagem do índice confere com `stats.questions` do backup?
- [ ] Cada questão verificada antes de ser incluída no `.tex`?
- [ ] Duplicatas excluídas (regular + adaptada)?
- [ ] Relatório final apresentado ao usuário?