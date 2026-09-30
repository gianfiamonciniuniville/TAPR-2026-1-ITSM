from etl.contracts import ExtractionDefinition

DEFINITION = ExtractionDefinition(
    name='chamado_sla',
    select_sql="""
        SELECT
            c.nr_chamado,
            s.cd_sla,
            cs.fl_breach,
            cs.qt_tempo_restante_minutos,
            cs.qt_tempo_decorrido_minutos,
            cs.qt_meta_minutos,
            cs.dt_referencia,
            cs.dt_inclusao,
            cs.dt_atualizacao,
            cs.nm_sistema_origem,
            cs.cd_registro_origem
        FROM itsm.chamado_sla AS cs
        INNER JOIN itsm.chamado AS c ON c.id_chamado = cs.id_chamado
        INNER JOIN itsm.sla     AS s ON s.id_sla     = cs.id_sla
    """,
    upsert_sql="""
        MERGE corptech.chamado_sla AS tgt
        USING (
            SELECT
                ch_dst.id_chamado,
                s_dst.id_sla,
                src.fl_breach,
                src.qt_tempo_restante_minutos,
                src.qt_tempo_decorrido_minutos,
                src.qt_meta_minutos,
                src.dt_referencia,
                src.dt_inclusao,
                src.dt_atualizacao,
                src.nm_sistema_origem,
                src.cd_registro_origem
            FROM (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS src (
                nr_chamado, cd_sla, fl_breach,
                qt_tempo_restante_minutos, qt_tempo_decorrido_minutos, qt_meta_minutos,
                dt_referencia, dt_inclusao, dt_atualizacao,
                nm_sistema_origem, cd_registro_origem
            )
            INNER JOIN corptech.chamado AS ch_dst ON ch_dst.nr_chamado = src.nr_chamado
            INNER JOIN corptech.sla     AS s_dst  ON s_dst.cd_sla      = src.cd_sla
        ) AS resolved
        ON tgt.cd_registro_origem = resolved.cd_registro_origem
        WHEN MATCHED THEN
            UPDATE SET
                id_chamado                 = resolved.id_chamado,
                id_sla                     = resolved.id_sla,
                fl_breach                  = resolved.fl_breach,
                qt_tempo_restante_minutos  = resolved.qt_tempo_restante_minutos,
                qt_tempo_decorrido_minutos = resolved.qt_tempo_decorrido_minutos,
                qt_meta_minutos            = resolved.qt_meta_minutos,
                dt_referencia              = resolved.dt_referencia,
                dt_atualizacao             = SYSUTCDATETIME(),
                nm_sistema_origem          = resolved.nm_sistema_origem
        WHEN NOT MATCHED THEN
            INSERT (
                id_chamado, id_sla, fl_breach,
                qt_tempo_restante_minutos, qt_tempo_decorrido_minutos, qt_meta_minutos,
                dt_referencia, dt_inclusao, dt_atualizacao,
                nm_sistema_origem, cd_registro_origem
            )
            VALUES (
                resolved.id_chamado, resolved.id_sla, resolved.fl_breach,
                resolved.qt_tempo_restante_minutos, resolved.qt_tempo_decorrido_minutos,
                resolved.qt_meta_minutos, resolved.dt_referencia, resolved.dt_inclusao,
                resolved.dt_atualizacao, resolved.nm_sistema_origem, resolved.cd_registro_origem
            );
    """,
)
