# ADR-003: [Azure Function]

**Status:** [Aceito] | **Data:** [12-09-2025] | **Autores:** [Gian
(Desenvolvedor)]

## Contexto

Precisamos de um SAAS que tinha fácil configuração e na execução de scripts
pequenos, porém separados.

## Decisão

Foi decidido Azure Functions por causa da facilidade;

## Consequências

(+) Roda

(+) Suporte com a linguagem requirida.

(-) Rodar em produção

(-) A integração com Azure e SQL Server requer ambiente configurado.

O fluxo de extração possui testes unitários locais após a aplicação de
[Template Method (ADR-005)](./adr005-template-method.md). Os timers delegam
a execução às subclasses de `SqlExtraction`.

## Alternativas rejeitadas

## Links

- Relacionado: [adrr001-cloud](./adr001-cloud.md)
