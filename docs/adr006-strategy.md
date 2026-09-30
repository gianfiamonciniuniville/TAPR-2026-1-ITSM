# ADR-006: Strategy nas Azure Functions

**Status:** Aceito | **Data:** 30-09-2026

Substitui o [ADR-005: Template Method](adr005-template-method.md).

## Contexto

As 11 Azure Functions extraem dados de `itsm` e gravam em `corptech`.
Precisávamos poder trocar a forma de ler e gravar sem alterar o fluxo principal.

## Decisão

Usar **Strategy**: cada forma de ler ou gravar fica em uma classe separada.
O `ExtractionRunner` recebe essas classes e coordena a execução.

| Contrato | Implementações |
| --- | --- |
| `ReadStrategy`: como ler | `FetchAllReadStrategy` lê tudo; `FetchManyReadStrategy` lê em lotes |
| `WriteStrategy`: como gravar | `BatchMergeWriteStrategy` grava em lote; `RowMergeWriteStrategy` grava por linha |

Os contratos definem os métodos que cada estratégia precisa oferecer.
O `bootstrap.py` escolhe as estratégias pelas variáveis de ambiente.
As triggers ficam em `src/function_app.py` e os SQLs em `src/etl/queries/`.
As consultas e os agendamentos foram preservados.

Antes, cada entidade herdava do executor. Agora, o executor recebe as
estratégias como objetos: essa troca de herança por composição permite
combinar leitura e gravação de maneiras diferentes.

## Consequências

- Podemos adicionar estratégias sem modificar o executor.
- Conexões, commit, rollback e fechamento ficam centralizados no executor.
- Ler em lotes reduz memória, mas mantém uma única transação para toda a carga.
- A execução não garante ordem entre timers nem implementa carga incremental.

## Validação

Os testes executados durante a implementação passaram e depois foram removidos
a pedido. A integração com SQL Server e o host Azure ainda precisa ser validada.

Configuração e organização dos arquivos: [README](../README.md).
