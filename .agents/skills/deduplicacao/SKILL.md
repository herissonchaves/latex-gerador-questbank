---
name: deduplicacao
description: >
  Verifica se questões dos arquivos de entrada já existem no banco QuestBank
  antes de incluí-las no questoes.tex. Use esta skill no Passo 2.5 do workflow,
  sempre que houver um arquivo *.questbank.json na raiz do projeto ou em entrada/.
  Executa deduplicador.py para construir o índice do banco e verificar cada
  questão segmentada, excluindo duplicatas do .tex e gerando relatório final.
---

# Deduplicação contra o Banco QuestBank

## Objetivo

Evitar que questões já cadastradas no app QuestBank sejam exportadas novamente.
Questões identificadas como duplicatas são silenciosamente excluídas do
`questoes.tex` (regular + adaptada) e listadas no relatório final ao usuário.

## Entradas esperadas

- `*.questbank.json` na raiz do projeto ou em `entrada/` (backup exportado pelo app)
- Lista de questões segmentadas (Passo 2) — enunciado em texto puro, banca e ano de cada questão

## Saída esperada

- `saida/questbank_index.json` — índice temporário das questões do banco
- Lista de questões filtradas: `NOVA` (incluir no `.tex`) vs `DUPLICATA:<id>` (excluir)
- Relatório final com contagem de inclusões e duplicatas

---

## Passo a passo

### Passo 1 — Localizar o backup

```bash
find . -name "*.questbank.json" | head -5
```

- Se **não encontrar**: pule esta skill inteiramente e continue para o Passo 3.
- Se encontrar **mais de um**: use o de data mais recente (pelo nome do arquivo).

### Passo 2 — Construir o índice

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py build <backup.questbank.json>
```

Gera `saida/questbank_index.json`. Verifique se o número de questões indexadas
bate com o campo `stats.questions` do JSON de backup.

### Passo 3 — Verificar cada questão antes de incluir no `.tex`

Para cada questão segmentada, execute **antes** de escrever o bloco LaTeX:

```bash
python .agents/skills/deduplicacao/scripts/deduplicador.py check "<banca>" "<ano>" "<trecho>"
```

**Como fornecer o trecho:** primeiros 100–150 caracteres do enunciado em texto
puro, sem LaTeX nem HTML, sem incluir a banca/ano.

| Saída | Ação |
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
  HTML e LaTeX são normalizados para texto puro antes de comparar.

## Checklist

- [ ] Arquivo `.questbank.json` localizado? Se não, skip.
- [ ] `deduplicador.py build` executado com sucesso?
- [ ] Contagem do índice confere com `stats.questions` do backup?
- [ ] Cada questão verificada antes de ser incluída no `.tex`?
- [ ] Duplicatas excluídas (regular + adaptada)?
- [ ] Relatório final apresentado ao usuário?