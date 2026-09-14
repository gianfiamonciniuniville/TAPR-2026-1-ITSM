# ADR-005: Template Method para extração e carga SQL

**Status:** Aceito | **Data:** 11-09-2026

## Contexto

O projeto possui 11 Azure Functions com timer que consultam o schema `itsm`
e executam `MERGE` no schema `corptech`, utilizado na análise do Power BI.
As rotinas repetiam conexões, leitura, carga em lote, commit e tratamento de
erros. A variação efetiva está no SQL de cada entidade, incluindo a resolução
de chaves naturais no destino. O CSAT também tinha uma variante de gerenciamento
de recursos que operava diretamente sobre cursores.

## Decisão

Aplicar o padrão comportamental GoF **Template Method** a todas as 11 rotinas.
`SqlExtraction.run()` define o fluxo; subclasses implementam `select_sql()` e
`upsert_sql()`. Os timers continuam como pontos de entrada e instanciam a
subclasse correspondente. As conexões ficam em `etl/connections.py`.

O fluxo fecha explicitamente conexões e cursores, evita carga de lote vazio,
confirma a transação após a carga e tenta rollback quando a carga ou o commit
falha. Exceções são registradas e propagadas ao runtime.

## Alternativas avaliadas

| Alternativa | Adequação ao código atual | Decisão |
| --- | --- | --- |
| Template Method | Um fluxo estável com consultas específicas por entidade | Escolhido |
| Strategy | Útil para alternar algoritmos completos por composição; não há essa seleção dinâmica hoje | Não necessário neste momento |
| Factory Method | Trata criação polimórfica; não elimina por si só o fluxo repetido | Não escolhido |
| Observer | Útil para notificar consumidores de eventos; as entradas atuais são timers | Não escolhido |
| Função parametrizada por SQL | Seria uma solução mais curta para a duplicação atual | Viável, mas optou-se pelo Template Method para atender ao estudo GoF e explicitar os pontos de extensão |

## Consequências

- Correções no fluxo passam a ser feitas em um único local.
- As consultas e seus parâmetros permanecem específicos e preservados por entidade.
- Testes usam conexões simuladas, sem depender de Azure ou SQL Server.
- Há uma classe por entidade e acoplamento por herança à classe base.
- Alterações na classe base afetam todas as extrações e exigem validação.
- `fetchall()` continua carregando tudo em memória; paginação não faz parte desta decisão.
- A transação é por extração no destino, sem atomicidade entre origem e destino
  ou entre timers. Agendamentos existentes não garantem ordem de dependências.

## Validação e referências

Testes: `python -m unittest discover -s tests -v`, na raiz do repositório.
Os testes cobrem sucesso, lote vazio, falhas de leitura, conexão, carga e commit,
rollback, liberação de recursos e contrato abstrato. Não substituem integração
com SQL Server e execução no Azure Functions.

Pesquisa, referências e diagrama: [Padrões GoF](padroes-gof.md).
Decisão de plataforma: [ADR-003](adr003-azure-function.md).
