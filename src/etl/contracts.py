from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

Row = Sequence[Any]
Batch = Sequence[Row]


class Cursor(Protocol):
    fast_executemany: bool

    def execute(self, sql: str, *parameters: Any) -> "Cursor": ...
    def executemany(self, sql: str, rows: Batch) -> None: ...
    def fetchall(self) -> Batch: ...
    def fetchmany(self, size: int) -> Batch: ...
    def close(self) -> None: ...


class Connection(Protocol):
    def cursor(self) -> Cursor: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...


ConnectionFactory = Callable[[], Connection]


@dataclass(frozen=True)
class ExtractionDefinition:
    name: str
    select_sql: str
    upsert_sql: str
