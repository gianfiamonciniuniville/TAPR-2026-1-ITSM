from collections.abc import Mapping
from types import MappingProxyType

from etl.contracts import ExtractionDefinition
from etl.queries.analista import DEFINITION as analista
from etl.queries.categoria import DEFINITION as categoria
from etl.queries.chamado import DEFINITION as chamado
from etl.queries.chamado_sla import DEFINITION as chamado_sla
from etl.queries.chamado_status_historico import DEFINITION as chamado_status_historico
from etl.queries.cliente_organizacao import DEFINITION as cliente_organizacao
from etl.queries.csat import DEFINITION as csat
from etl.queries.csat_avaliacao import DEFINITION as csat_avaliacao
from etl.queries.fila import DEFINITION as fila
from etl.queries.sla import DEFINITION as sla
from etl.queries.solicitante import DEFINITION as solicitante

DEFINITIONS: Mapping[str, ExtractionDefinition] = MappingProxyType({
    'analista': analista,
    'categoria': categoria,
    'chamado': chamado,
    'chamado_sla': chamado_sla,
    'chamado_status_historico': chamado_status_historico,
    'cliente_organizacao': cliente_organizacao,
    'csat': csat,
    'csat_avaliacao': csat_avaliacao,
    'fila': fila,
    'sla': sla,
    'solicitante': solicitante,
})
