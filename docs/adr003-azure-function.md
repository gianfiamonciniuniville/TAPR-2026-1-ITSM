# ADR-003: Azure Functions

**Status:** Aceito | **Data:** 12-09-2025 | **Autor:** Gian

## Contexto

Precisamos executar pequenos scripts Python em horários definidos para
extrair e carregar dados.

## Decisão

Usar Azure Functions com triggers de timer. As 11 triggers ficam em
`src/function_app.py` e chamam `run_extraction()` para executar o ETL
usando [Strategy](adr006-strategy.md).

## Consequências

- Os scripts podem ser executados automaticamente nos horários configurados.
- A execução depende da configuração do Azure e do acesso ao SQL Server.
- Os horários não garantem a ordem de execução entre entidades dependentes.

Decisão de nuvem: [ADR-001](adr001-cloud.md).
