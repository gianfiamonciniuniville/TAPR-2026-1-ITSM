from etl.contracts import ExtractionDefinition

DEFINITION = ExtractionDefinition(
    name='sla',
    select_sql="""
        SELECT
            cd_sla,
            nm_sla,
            qt_meta_minutos,
            ds_descricao,
            fl_ativo,
            dt_inclusao,
            dt_atualizacao,
            nm_sistema_origem,
            cd_registro_origem
        FROM itsm.sla
    """,
    upsert_sql="""
        MERGE corptech.sla AS tgt
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)) AS src (
            cd_sla, nm_sla, qt_meta_minutos, ds_descricao, fl_ativo,
            dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
        )
        ON tgt.cd_sla = src.cd_sla
        WHEN MATCHED THEN
            UPDATE SET
                nm_sla             = src.nm_sla,
                qt_meta_minutos    = src.qt_meta_minutos,
                ds_descricao       = src.ds_descricao,
                fl_ativo           = src.fl_ativo,
                dt_atualizacao     = SYSUTCDATETIME(),
                nm_sistema_origem  = src.nm_sistema_origem,
                cd_registro_origem = src.cd_registro_origem
        WHEN NOT MATCHED THEN
            INSERT (cd_sla, nm_sla, qt_meta_minutos, ds_descricao, fl_ativo,
                    dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem)
            VALUES (src.cd_sla, src.nm_sla, src.qt_meta_minutos, src.ds_descricao, src.fl_ativo,
                    src.dt_inclusao, src.dt_atualizacao, src.nm_sistema_origem, src.cd_registro_origem);
    """,
)
