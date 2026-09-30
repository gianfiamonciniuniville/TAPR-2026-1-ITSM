# ADR-005: Template Method para extração SQL

**Status:** Substituído pelo [ADR-006: Strategy](adr006-strategy.md) em 30-09-2026
**Data original:** 11-09-2026

## Contexto

As 11 extrações repetiam o código de conexão, leitura, gravação e tratamento
de erros.

## Decisão original

Usar **Template Method**: a classe `SqlExtraction` definia o fluxo completo.
Cada entidade herdava dessa classe e fornecia seus SQLs pelos métodos
`select_sql()` e `upsert_sql()`.

## Resultado e substituição

A solução centralizou o código comum, mas mantinha as entidades ligadas ao
executor por herança. Foi substituída por Strategy para permitir a troca das
formas de leitura e gravação por composição.

Este documento registra a solução anterior. A implementação atual está
explicada no [ADR-006](adr006-strategy.md).
