import azure.functions as func

from etl.extraction import SqlExtraction

app = func.Blueprint()


class CsatExtraction(SqlExtraction):
    def select_sql(self) -> str:
        return "SELECT Id, Column1, Column2 FROM itsm.csat"

    def upsert_sql(self) -> str:
        return """
        MERGE corptech.csat AS tgt
        USING (VALUES (?, ?, ?)) AS src (Id, Column1, Column2)
        ON tgt.Id = src.Id
        WHEN MATCHED THEN
            UPDATE SET Column1 = src.Column1, Column2 = src.Column2
        WHEN NOT MATCHED THEN
            INSERT (Id, Column1, Column2) VALUES (src.Id, src.Column1, src.Column2);
    """


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_csat(myTimer: func.TimerRequest) -> None:
    CsatExtraction().run()
