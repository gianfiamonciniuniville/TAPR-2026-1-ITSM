# TAPR-2026-1-ITSM

IT Service Management

# Integrantes

> Gian Carlo Fiamoncini, Edson Luis Rosa Junior, Gustavo Pereira e Carlos
> Alberto Junior

---

# Padrão de projeto GoF

Foi aplicado **Template Method** às 11 extrações SQL. A classe `SqlExtraction`
centraliza leitura, carga, transação e fechamento dos recursos; cada subclasse
fornece as consultas da sua entidade.

---

# Atividade de Documentação Arquitetural

### ADR's

- [adrr001-cloud](./docs/adr001-cloud.md)
- [adrr002-database](./docs/adr002-database.md)
- [adr003-azure-function](./docs/adr003-azure-function.md)
- [adr004-power-bi](./docs/adr004-power-bi.md)
- [adr005-template-method](./docs/adr005-template-method.md)

### C4 Diagram

- [Diagram DRAWIO](./docs/c4-contexto.drawio)

#### C4 Imagem

- ![Diagram](./docs/c4-contexto.png)

---

# Escopo

![Desenho EXCALIDRAW](docs/antique/desenho.png)

# Print AZURE

![Print Azure](docs/antique/Captura%20de%20tela%202026-04-04%20192359.png)

# Justificativa Documento

[Link Documento](docs/antique/Justificativa_ITSM_Azure.docx)

# Dashboard Power BI

Para documentar o dashboard Power BI, seguem três prints:

## Geral

![Dashboard Power BI - Print 1](docs/antique/dashboard-geral.png)

## Abertos

![Dashboard Power BI - Print 2](docs/antique/dashboard-aberto.png)

## Encerrados

![Dashboard Power BI - Print 3](docs/antique/dashboard-encerrados.png)
