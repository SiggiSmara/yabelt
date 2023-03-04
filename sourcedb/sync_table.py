from loguru import logger
from sqlalchemy import engine, MetaData, Table
from sqlalchemy.engine import Row
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime

class SyncTable:
    def __init__(
        self,
        table_name: str,
        source_engine: engine,
        destination_engine: engine,
        table_metadata: MetaData,
        metadata_from_source: bool = False,
    ):
        self.table_name = table_name
        self.source_engine = source_engine
        self.destination_engine = destination_engine
        self.metadata = table_metadata
        self.metadata_from_source = metadata_from_source
        self.table = self.reflect_table()

    def reflect_table(self, metadata_from_source: bool = None):
        metadata_from_source = next(
            sub for sub in (metadata_from_source, self.metadata_from_source) if sub is not None
        )
        if metadata_from_source:
            return Table(
                self.table_name, self.metadata, autoload_with=self.source_engine
            )
        else:
            return Table(
                self.table_name, self.metadata, autoload_with=self.destination_engine
            )

    def read_from_source(self, from_date:datetime=None, to_date:datetime=None):
        my_sel = select(self.table)
        if from_date is not None:
            my_sel = my_sel.where(self.table.c.moddt > from_date)
        if to_date is not None:
            my_sel = my_sel.where(self.table.c.moddt <= to_date)
        with self.source_engine.connect() as conn:
            result_list = []
            for row in conn.execute(my_sel):
                result_list.append(row)
                if len(result_list) == 1000:
                    self.write_to_destination(result_list=result_list)
                    result_list = []
            if len(result_list) > 0:
                self.write_to_destination(result_list=result_list)

    def write_to_destination(self, result_list:List(Row)):
        my_insert = insert(self.table)
        my_rows = [arow._asdict()for arow in result_list]
        with self.destination_engine.connect() as conn:
            try:
                result = conn.execute(my_insert, my_rows)
                conn.commit()
            except IntegrityError as e:
                logger.warning(e)
                logger.warning("Rolling back.")
                conn.rollback()
                if len(result_list) == 1:
                    # try update
                    logger.warning(f"Trying to recover from inegrity error in {self.table_name} by updating single record.")
                    my_row = result_list[0]
                    my_update = update(self.table)
                    prim_names = []
                    for one_p in self.table.primary_key:
                        my_update = my_update.where(one_p == my_row[one_p.name])
                        prim_names.append(one_p.name)
                    my_vals = {
                        one_c.name: my_row[one_c.name] for one_c in self.table.c if one_c.name not in prim_names
                    }
                    my_update = my_update.values(**my_vals)
                    result = conn.execute(my_update)
                    # error here means foreign key error, should not happen
                    # unless table sync orchestration fails
                    conn.commit()
                else:
                    # split in two and try again
                    logger.warning(f"Trying to recover from inegrity error in {self.table_name} by splitting list in two.")
                    mid = len(result_list)//2
                    self.write_to_destination(result_list=result[:mid])
                    self.write_to_destination(result_list=result_list[mid:])

           