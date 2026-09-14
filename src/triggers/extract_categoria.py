import azure.functions as func

from etl.extraction import SqlExtraction

app = func.Blueprint()


class CategoriaExtraction(SqlExtraction):
    def select_sql(self) -> str:
        return """
        SELECT
            cd_categoria,
            nm_categoria,
            ds_descricao,
            fl_ativo,
            dt_inclusao,
            dt_atualizacao,
            nm_sistema_origem,
            cd_registro_origem
        FROM itsm.categoria
    """

    def upsert_sql(self) -> str:
        return """
        MERGE corptech.categoria AS tgt
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?)) AS src (
            cd_categoria, nm_categoria, ds_descricao, fl_ativo,
            dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
        )
        ON tgt.cd_categoria = src.cd_categoria
        WHEN MATCHED THEN
            UPDATE SET
                nm_categoria       = src.nm_categoria,
                ds_descricao       = src.ds_descricao,
                fl_ativo           = src.fl_ativo,
                dt_atualizacao     = SYSUTCDATETIME(),
                nm_sistema_origem  = src.nm_sistema_origem,
                cd_registro_origem = src.cd_registro_origem
        WHEN NOT MATCHED THEN
            INSERT (cd_categoria, nm_categoria, ds_descricao, fl_ativo,
                    dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem)
            VALUES (src.cd_categoria, src.nm_categoria, src.ds_descricao, src.fl_ativo,
                    src.dt_inclusao, src.dt_atualizacao, src.nm_sistema_origem, src.cd_registro_origem);
    """


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_categoria(myTimer: func.TimerRequest) -> None:
    CategoriaExtraction().run()
