---
name: empacotador-zip
description: >
  Empacota saida/questoes.tex + main.tex + imagens em saida/questoes.zip
  dual-compatível com o app QuestBank e o Overleaf. Use esta skill no Passo 5
  do workflow, imediatamente após validar o questoes.tex pela skill
  formatador-latex. Roda o script montador.py, que localiza imagens
  referenciadas via \imagem{}, copia o wrapper main.tex e produz o ZIP final.
  Ative também quando o usuário disser "gerar o ZIP", "empacotar as questões"
  ou "montar o entregável".
---

# Empacotador do ZIP QuestBank (`questoes.zip`)

## Objetivo

Produzir o entregável final `saida/questoes.zip` contendo `questoes.tex`,
`main.tex` (wrapper Overleaf) e todas as imagens referenciadas pelas questões,
sempre na **raiz do ZIP** (sem subpastas).

## Entradas esperadas

- `saida/questoes.tex` — gerado pela skill `formatador-latex` no Passo 3/4
- `main.tex` — wrapper Overleaf na raiz do projeto (não editar)
- Imagens referenciadas via `\imagem{ImagemN.png}` — buscadas em `.`, `saida/`,
  `entrada/` e `imagens/`

## Saída esperada

```
saida/
├── main.tex          ← cópia do wrapper (gerada aqui)
└── questoes.zip      ← entregável final
```

Estrutura interna do ZIP:

```
questoes.zip/
├── questoes.tex      ← lido pelo servidor questbank-server (app QuestBank)
├── main.tex          ← compilado pelo Overleaf
├── Imagem1.png       ← imagens sempre na RAIZ do ZIP
├── Imagem2.png
└── ...
```

## Como executar

Execute sempre a partir da raiz do projeto:

```bash
python .agents/skills/empacotador-zip/scripts/montador.py
```

O script imprime quantas imagens foram empacotadas e quais não foram
encontradas (se houver).

## Passo a passo

1. Confirme que `saida/questoes.tex` existe e foi validado.
2. Confirme que `main.tex` está na raiz do projeto.
3. Execute `python .agents/skills/empacotador-zip/scripts/montador.py`.
4. Leia o output: anote imagens não localizadas e avise o usuário se houver.
5. Entregue o caminho `saida/questoes.zip` ao usuário.

## Regras e restrições

- **Nunca** coloque imagens em subpastas dentro do ZIP — sempre na raiz.
- **Não modifique** o `main.tex` da raiz; o script apenas o copia para `saida/`.
- Se `saida/questoes.tex` não existir: pare e oriente o usuário a rodar o
  Passo 3 (skill `formatador-latex`) antes.
- Se `main.tex` não existir na raiz: pare e oriente o usuário a restaurá-lo
  do repositório/backup — sem ele o Overleaf não compila.
- Imagens não encontradas **não** abortam o ZIP — são apenas reportadas no log.
  Cabe ao usuário adicioná-las manualmente ao ZIP antes de importar.

## Checklist pré-entrega

- [ ] `saida/questoes.tex` existe e foi validado pelo `formatador-latex`?
- [ ] `main.tex` está na raiz do projeto?
- [ ] Script executado sem erros Python?
- [ ] `saida/questoes.zip` gerado?
- [ ] Imagens faltantes (se houver) reportadas ao usuário?
- [ ] Caminho do ZIP entregue ao usuário?
