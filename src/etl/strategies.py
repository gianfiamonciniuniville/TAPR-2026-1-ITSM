from collections.abc import Iterator
from dataclasses import dataclass
from typing import Protocol

from etl.contracts import Batch, Cursor


class ReadStrategy(Protocol):
    def read(self, cursor: Cursor, sql: str) -> Iterator[Batch]: ...


class WriteStrategy(Protocol):
    def write(self, cursor: Cursor, sql: str, rows: Batch) -> None: ...


class FetchAllReadStrategy:
    """Materializa a consulta inteira, preservando o comportamento original."""

    def read(self, cursor: Cursor, sql: str) -> Iterator[Batch]:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            yield rows


@dataclass(frozen=True)
class FetchManyReadStrategy:
    """Consome o cursor em lotes; não executa paginação SQL nem checkpoints."""

    batch_size: int = 1000

    def __post_init__(self) -> None:
        if type(self.batch_size) is not int or self.batch_size <= 0:
            raise ValueError("batch_size deve ser um inteiro positivo.")

    def read(self, cursor: Cursor, sql: str) -> Iterator[Batch]:
        cursor.execute(sql)
        while rows := cursor.fetchmany(self.batch_size):
            yield rows


class BatchMergeWriteStrategy:
    """Envia cada lote ao driver usando fast_executemany."""

    def write(self, cursor: Cursor, sql: str, rows: Batch) -> None:
        if rows:
            cursor.fast_executemany = True
            cursor.executemany(sql, rows)


class RowMergeWriteStrategy:
    """Executa um MERGE por linha, na mesma transação controlada pelo executor."""

    def write(self, cursor: Cursor, sql: str, rows: Batch) -> None:
        for row in rows:
            cursor.execute(sql, row)
