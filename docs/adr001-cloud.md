# ADR-001: [Cloud]

**Status:** [Aceito]  |  **Data:** [12-09-2025]  |  **Autores:** [Gian (Desenvolvedor)]

## Contexto

Precisamos de uma plataforma de nuvem robusta e popular que suportasse alta segurança e flexibilidade na execução e deploy do projeto. 

Como precisamos de algumas azure functions para executar scripts pequenos, porém separados. Integração com GitHub Actions para CI\CD.

## Decisão

Foi decidido Azure por causa da melhor usabilidade e preço. 

## Consequências

(+) Fácil de configurar;

(+) Suporte com a linguagem requirida (para as azure funtions).

(-) Execução somente na produção

## Alternativas rejeitadas

## Links

- Relacionado: [adrr003-azure-function](./adr003-azure-function.md)