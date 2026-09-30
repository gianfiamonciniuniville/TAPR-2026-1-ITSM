import os
from collections.abc import Callable, Mapping
from typing import TypeVar

from etl.extraction import ExtractionRunner
from etl.queries import DEFINITIONS
from etl.strategies import (
    BatchMergeWriteStrategy,
    FetchAllReadStrategy,
    FetchManyReadStrategy,
    ReadStrategy,
    RowMergeWriteStrategy,
    WriteStrategy,
)


def _fetch_many(config: Mapping[str, str]) -> ReadStrategy:
    try:
        return FetchManyReadStrategy(int(config.get("ETL_BATCH_SIZE", "1000")))
    except ValueError as error:
        raise ValueError("ETL_BATCH_SIZE deve ser um inteiro positivo.") from error


# Estender estes registros acrescenta algoritmos sem alterar ExtractionRunner.
# Fábricas recebem configuração e retornam instâncias novas, sem abrir conexões.
READ_STRATEGIES: dict[str, Callable[[Mapping[str, str]], ReadStrategy]] = {
    "fetch_all": lambda config: FetchAllReadStrategy(),
    "fetch_many": _fetch_many,
}
WRITE_STRATEGIES: dict[str, Callable[[Mapping[str, str]], WriteStrategy]] = {
    "batch": lambda config: BatchMergeWriteStrategy(),
    "row": lambda config: RowMergeWriteStrategy(),
}
_Strategy = TypeVar("_Strategy")


def _select(
    registry: Mapping[str, Callable[[Mapping[str, str]], _Strategy]],
    option: str,
    default: str,
    config: Mapping[str, str],
) -> _Strategy:
    name = config.get(option, default)
    if name not in registry:
        raise ValueError(f"{option} desconhecida: {name!r}. Opções: {', '.join(registry)}.")
    return registry[name](config)


def create_runner(
    entity: str, environ: Mapping[str, str] | None = None,
) -> ExtractionRunner:
    config = dict(os.environ if environ is None else environ)
    if entity not in DEFINITIONS:
        raise ValueError(f"Entidade desconhecida: {entity!r}. Opções: {', '.join(DEFINITIONS)}.")
    read = _select(READ_STRATEGIES, "ETL_READ_STRATEGY", "fetch_all", config)
    write = _select(WRITE_STRATEGIES, "ETL_WRITE_STRATEGY", "batch", config)
    return ExtractionRunner(DEFINITIONS[entity], read, write)


def run_extraction(entity: str) -> None:
    create_runner(entity).run()
