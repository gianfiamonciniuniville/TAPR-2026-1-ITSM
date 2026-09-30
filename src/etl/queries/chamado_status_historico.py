from etl.contracts import ExtractionDefinition

DEFINITION = ExtractionDefinition(
    name='chamado_status_historico',
    select_sql="""
        SELECT
            c.nr_chamado,
            csh.ds_status_chamado,
            csh.dt_inicio_status,
            csh.dt_fim_status,
            csh.qt_tempo_status_minutos,
            a.cd_analista   AS cd_analista_responsavel,
            f.cd_fila,
            csh.dt_inclusao,
            csh.dt_atualizacao,
            csh.nm_sistema_origem,
            csh.cd_registro_origem
        FROM itsm.chamado_status_historico AS csh
        INNER JOIN itsm.chamado  AS c ON c.id_chamado  = csh.id_chamado
        LEFT JOIN  itsm.analista AS a ON a.id_analista = csh.id_analista_responsavel
        LEFT JOIN  itsm.fila     AS f ON f.id_fila     = csh.id_fila
    """,
    upsert_sql="""
        MERGE corptech.chamado_status_historico AS tgt
        USING (
            SELECT
                ch_dst.id_chamado,
                src.ds_status_chamado,
                src.dt_inicio_status,
                src.dt_fim_status,
                src.qt_tempo_status_minutos,
                a_dst.id_analista AS id_analista_responsavel,
                f_dst.id_fila,
                src.dt_inclusao,
                src.dt_atualizacao,
                src.nm_sistema_origem,
                src.cd_registro_origem
            FROM (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS src (
                nr_chamado, ds_status_chamado, dt_inicio_status, dt_fim_status,
                qt_tempo_status_minutos, cd_analista_responsavel, cd_fila,
                dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
            )
            INNER JOIN corptech.chamado  AS ch_dst ON ch_dst.nr_chamado = src.nr_chamado
            LEFT JOIN  corptech.analista AS a_dst  ON a_dst.cd_analista = src.cd_analista_responsavel
            LEFT JOIN  corptech.fila     AS f_dst  ON f_dst.cd_fila     = src.cd_fila
        ) AS resolved
        ON tgt.cd_registro_origem = resolved.cd_registro_origem
        WHEN MATCHED THEN
            UPDATE SET
                id_chamado              = resolved.id_chamado,
                ds_status_chamado       = resolved.ds_status_chamado,
                dt_inicio_status        = resolved.dt_inicio_status,
                dt_fim_status           = resolved.dt_fim_status,
                qt_tempo_status_minutos = resolved.qt_tempo_status_minutos,
                id_analista_responsavel = resolved.id_analista_responsavel,
                id_fila                 = resolved.id_fila,
                dt_atualizacao          = SYSUTCDATETIME(),
                nm_sistema_origem       = resolved.nm_sistema_origem
        WHEN NOT MATCHED THEN
            INSERT (
                id_chamado, ds_status_chamado, dt_inicio_status, dt_fim_status,
                qt_tempo_status_minutos, id_analista_responsavel, id_fila,
                dt_inclusao, dt_atualizacao, nm_sistema_origem, cd_registro_origem
            )
            VALUES (
                resolved.id_chamado, resolved.ds_status_chamado, resolved.dt_inicio_status,
                resolved.dt_fim_status, resolved.qt_tempo_status_minutos,
                resolved.id_analista_responsavel, resolved.id_fila,
                resolved.dt_inclusao, resolved.dt_atualizacao,
                resolved.nm_sistema_origem, resolved.cd_registro_origem
            );
    """,
)
