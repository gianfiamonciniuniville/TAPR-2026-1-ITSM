from etl.contracts import ExtractionDefinition

DEFINITION = ExtractionDefinition(
    name='csat',
    select_sql="SELECT Id, Column1, Column2 FROM itsm.csat",
    upsert_sql="""
        MERGE corptech.csat AS tgt
        USING (VALUES (?, ?, ?)) AS src (Id, Column1, Column2)
        ON tgt.Id = src.Id
        WHEN MATCHED THEN
            UPDATE SET Column1 = src.Column1, Column2 = src.Column2
        WHEN NOT MATCHED THEN
            INSERT (Id, Column1, Column2) VALUES (src.Id, src.Column1, src.Column2);
    """,
)
