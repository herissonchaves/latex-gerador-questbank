# Backup do banco QuestBank

Coloque aqui o **último** arquivo de backup exportado pelo app QuestBank.

O nome segue o padrão:

```
questbank-backup-AAAA-MM-DD_HH-MM-SS.questbank.json
```

## Como o workflow usa esta pasta

A cada execução, o agente:

1. Procura nesta pasta o `*.questbank.json` mais recente (ordenação por nome).
2. Constrói automaticamente o índice em `saida/questbank_index.json`.
3. Verifica cada questão segmentada contra o índice **antes** de escrever o `.tex`.
4. Exclui silenciosamente questões já cadastradas e gera o relatório final.

## Boas práticas

- **Mantenha apenas o backup mais recente** — apague os antigos para evitar
  confusão. O agente sempre escolhe o de nome mais alto (cronológico), mas
  manter a pasta limpa simplifica auditoria.
- **Não versione o backup no git** se ele contiver dados sensíveis — use
  `.gitignore` se necessário.
- **Sem backup nesta pasta?** O agente avisa e segue sem deduplicação,
  alertando que pode haver questões duplicadas no `.tex`.
