import azure.functions as func

from etl.extraction import SqlExtraction

app = func.Blueprint()


class AnalistaExtraction(SqlExtraction):
    def select_sql(self) -> str:
        return """
        SELECT
            a.cd_analista,
            a.nm_analista,
            a.ds_email,
            a.ds_nivel,
            f.cd_fila   AS cd_fila_atual,
            a.fl_ativo,
            a.dt_inclusao,
            a.dt_atualizacao,
            a.nm_sistema_origem,
            a.cd_registro_origem
        FROM itsm.analista AS a
        LEFT JOIN itsm.fila AS f ON f.id_fila = a.id_fila_atual
    """

    def upsert_sql(self) -> str:
        return """
        MERGE corptech.analista AS tgt
        USING (
            SELECT
                src.cd_analista,
                src.nm_analista,
                src.ds_email,
                src.ds_nivel,
                f_dst.id_fila  AS id_fila_atual,
                src.fl_ativo,
                src.dt_inclusao,
                src.dt_atualizacao,
                src.nm_sistema_origem,
                src.cd_registro_origem
            FROM (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS src (
                cd_analista, nm_analista, ds_email, ds_nivel, cd_fila_atual,
                fl_ativo, dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
            )
            LEFT JOIN corptech.fila AS f_dst ON f_dst.cd_fila = src.cd_fila_atual
        ) AS resolved
        ON tgt.cd_analista = resolved.cd_analista
        WHEN MATCHED THEN
            UPDATE SET
                nm_analista        = resolved.nm_analista,
                ds_email           = resolved.ds_email,
                ds_nivel           = resolved.ds_nivel,
                id_fila_atual      = resolved.id_fila_atual,
                fl_ativo           = resolved.fl_ativo,
                dt_atualizacao     = SYSUTCDATETIME(),
                nm_sistema_origem  = resolved.nm_sistema_origem,
                cd_registro_origem = resolved.cd_registro_origem
        WHEN NOT MATCHED THEN
            INSERT (cd_analista, nm_analista, ds_email, ds_nivel, id_fila_atual,
                    fl_ativo, dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem)
            VALUES (resolved.cd_analista, resolved.nm_analista, resolved.ds_email, resolved.ds_nivel,
                    resolved.id_fila_atual, resolved.fl_ativo, resolved.dt_inclusao,
                    resolved.dt_atualizacao, resolved.nm_sistema_origem, resolved.cd_registro_origem);
    """


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_analista(myTimer: func.TimerRequest) -> None:
    AnalistaExtraction().run()
