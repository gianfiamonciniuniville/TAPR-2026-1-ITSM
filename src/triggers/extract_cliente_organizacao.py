import azure.functions as func

from etl.extraction import SqlExtraction

app = func.Blueprint()


class ClienteOrganizacaoExtraction(SqlExtraction):
    def select_sql(self) -> str:
        return """
        SELECT
            cd_cliente_organizacao,
            nm_cliente_organizacao,
            nr_cnpj,
            fl_ativo,
            dt_inclusao,
            dt_atualizacao,
            nm_sistema_origem,
            cd_registro_origem
        FROM itsm.cliente_organizacao
    """

    def upsert_sql(self) -> str:
        return """
        MERGE corptech.cliente_organizacao AS tgt
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?)) AS src (
            cd_cliente_organizacao, nm_cliente_organizacao, nr_cnpj, fl_ativo,
            dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
        )
        ON tgt.cd_cliente_organizacao = src.cd_cliente_organizacao
        WHEN MATCHED THEN
            UPDATE SET
                nm_cliente_organizacao = src.nm_cliente_organizacao,
                nr_cnpj                = src.nr_cnpj,
                fl_ativo               = src.fl_ativo,
                dt_atualizacao         = SYSUTCDATETIME(),
                nm_sistema_origem      = src.nm_sistema_origem,
                cd_registro_origem     = src.cd_registro_origem
        WHEN NOT MATCHED THEN
            INSERT (cd_cliente_organizacao, nm_cliente_organizacao, nr_cnpj, fl_ativo,
                    dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem)
            VALUES (src.cd_cliente_organizacao, src.nm_cliente_organizacao, src.nr_cnpj, src.fl_ativo,
                    src.dt_inclusao, src.dt_atualizacao, src.nm_sistema_origem, src.cd_registro_origem);
    """


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    ClienteOrganizacaoExtraction().run()
