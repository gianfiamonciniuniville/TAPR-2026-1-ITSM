import azure.functions as func

from etl.extraction import SqlExtraction

app = func.Blueprint()


class FilaExtraction(SqlExtraction):
    def select_sql(self) -> str:
        return """
        SELECT
            cd_fila,
            nm_fila,
            ds_descricao,
            fl_ativo,
            dt_inclusao,
            dt_atualizacao,
            nm_sistema_origem,
            cd_registro_origem
        FROM itsm.fila
    """

    def upsert_sql(self) -> str:
        return """
        MERGE corptech.fila AS tgt
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?)) AS src (
            cd_fila, nm_fila, ds_descricao, fl_ativo,
            dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
        )
        ON tgt.cd_fila = src.cd_fila
        WHEN MATCHED THEN
            UPDATE SET
                nm_fila            = src.nm_fila,
                ds_descricao       = src.ds_descricao,
                fl_ativo           = src.fl_ativo,
                dt_atualizacao     = SYSUTCDATETIME(),
                nm_sistema_origem  = src.nm_sistema_origem,
                cd_registro_origem = src.cd_registro_origem
        WHEN NOT MATCHED THEN
            INSERT (cd_fila, nm_fila, ds_descricao, fl_ativo,
                    dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem)
            VALUES (src.cd_fila, src.nm_fila, src.ds_descricao, src.fl_ativo,
                    src.dt_inclusao, src.dt_atualizacao, src.nm_sistema_origem, src.cd_registro_origem);
    """


@app.timer_trigger(schedule="0 30 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_fila(myTimer: func.TimerRequest) -> None:
    FilaExtraction().run()
