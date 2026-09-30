import azure.functions as func

from etl.bootstrap import run_extraction

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_csat(myTimer: func.TimerRequest) -> None:
    run_extraction('csat')


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_sla(myTimer: func.TimerRequest) -> None:
    run_extraction('sla')


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_categoria(myTimer: func.TimerRequest) -> None:
    run_extraction('categoria')


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    run_extraction('cliente_organizacao')


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_solicitante(myTimer: func.TimerRequest) -> None:
    run_extraction('solicitante')


@app.timer_trigger(schedule="0 30 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_fila(myTimer: func.TimerRequest) -> None:
    run_extraction('fila')


@app.timer_trigger(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_analista(myTimer: func.TimerRequest) -> None:
    run_extraction('analista')


@app.timer_trigger(schedule="0 10 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    run_extraction('chamado')


@app.timer_trigger(schedule="0 20 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_chamado_status_historico(myTimer: func.TimerRequest) -> None:
    run_extraction('chamado_status_historico')


@app.timer_trigger(schedule="0 20 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_csat_avaliacao(myTimer: func.TimerRequest) -> None:
    run_extraction('csat_avaliacao')


@app.timer_trigger(schedule="0 20 12 * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    run_extraction('chamado_sla')
