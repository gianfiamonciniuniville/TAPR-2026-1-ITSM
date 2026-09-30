import logging
from collections.abc import Iterator
from contextlib import contextmanager
from itertools import chain
from typing import Protocol, TypeVar

from etl.connections import get_source_connection, get_target_connection
from etl.contracts import ConnectionFactory, ExtractionDefinition
from etl.strategies import ReadStrategy, WriteStrategy

logger = logging.getLogger(__name__)


class _Closeable(Protocol):
    def close(self) -> None: ...


_Resource = TypeVar("_Resource", bound=_Closeable)


@contextmanager
def _closing(resource: _Resource) -> Iterator[_Resource]:
    """Fecha o recurso sem substituir uma exceção que já está em propagação."""
    try:
        yield resource
    except BaseException:
        try:
            resource.close()
        except Exception:
            logger.exception("Falha adicional ao fechar recurso do ETL.")
        raise
    else:
        resource.close()


class ExtractionRunner:
    """Executa qualquer par de estratégias com uma transação por extração.

    Fábricas devem devolver conexões novas; o destino deve ter autocommit=False
    (padrão de pyodbc.connect). As estratégias não controlam a transação.
    """

    def __init__(
        self,
        definition: ExtractionDefinition,
        read_strategy: ReadStrategy,
        write_strategy: WriteStrategy,
        source_connection: ConnectionFactory | None = None,
        target_connection: ConnectionFactory | None = None,
    ) -> None:
        self.definition = definition
        self.read_strategy = read_strategy
        self.write_strategy = write_strategy
        self._source_connection = (
            get_source_connection if source_connection is None else source_connection
        )
        self._target_connection = (
            get_target_connection if target_connection is None else target_connection
        )

    def run(self) -> None:
        name = self.definition.name
        logger.info("%s: iniciando leitura=%s carga=%s.", name,
                    type(self.read_strategy).__name__, type(self.write_strategy).__name__)
        try:
            self._run()
        except Exception:
            logger.exception("%s: erro na extração/carga.", name)
            raise

    def _run(self) -> None:
        count = 0
        with _closing(self._source_connection()) as source:
            with _closing(source.cursor()) as source_cursor:
                batches = (
                    batch for batch in self.read_strategy.read(
                        source_cursor, self.definition.select_sql
                    ) if batch
                )
                first = next(batches, None)
                if first is None:
                    logger.info("%s: origem sem linhas.", self.definition.name)
                    return
                with _closing(self._target_connection()) as target:
                    try:
                        with _closing(target.cursor()) as target_cursor:
                            for batch in chain((first,), batches):
                                self.write_strategy.write(
                                    target_cursor, self.definition.upsert_sql, batch
                                )
                                count += len(batch)
                        target.commit()
                    except Exception:
                        try:
                            target.rollback()
                        except Exception:
                            logger.exception("%s: falha adicional no rollback.", self.definition.name)
                        raise
        logger.info("%s: carga confirmada; %s linha(s) processada(s).",
                    self.definition.name, count)
