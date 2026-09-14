import logging
from abc import ABC, abstractmethod
from contextlib import closing

from etl.connections import get_source_connection, get_target_connection


class SqlExtraction(ABC):
    def __init__(self, source_connection=None, target_connection=None):
        self._source_connection = source_connection or get_source_connection
        self._target_connection = target_connection or get_target_connection

    @abstractmethod
    def select_sql(self) -> str:    
        pass
        
    @abstractmethod
    def upsert_sql(self) -> str:
        pass
    
    def run(self) -> None:
        name = type(self).__name__
        logging.info("%s: iniciando.", name)
        try:
            with closing(self._source_connection()) as source:
                with closing(source.cursor()) as cursor:
                    rows = cursor.execute(self.select_sql()).fetchall()
            logging.info("%s: %s linha(s) lida(s) da origem.", name, len(rows))
            if not rows:
                return
            with closing(self._target_connection()) as target:
                try:
                    with closing(target.cursor()) as cursor:
                        cursor.fast_executemany = True
                        cursor.executemany(self.upsert_sql(), rows)
                    target.commit()
                except Exception:
                    target.rollback()
                    raise
            logging.info("%s: upsert concluído.", name)
        except Exception:
            logging.exception("%s: erro na extração/carga.", name)
            raise
