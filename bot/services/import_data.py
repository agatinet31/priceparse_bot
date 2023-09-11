import contextlib
import os
from typing import BinaryIO

from pandas import DataFrame, read_excel
from pydantic import ValidationError

from bot.core.config import settings
from bot.core.db import get_async_session
from bot.core.decorators import validate_data_schema
from bot.core.exceptions import ImportExcelFileError
from bot.core.utils import write_bytesio_to_file
from bot.models.product import LinkProduct
from bot.schemas import LinkProductShema


@validate_data_schema(data_schema=LinkProductShema)
async def save_bot_data_to_db(data: DataFrame):
    """Валидация и импорт данных в БД по ссылкам на продукцию."""
    get_async_session_context = contextlib.asynccontextmanager(
        get_async_session
    )
    async with get_async_session_context() as session:
        conn = await session.connection()
        await conn.run_sync(
            lambda sync_conn: data.to_sql(
                LinkProduct.__tablename__,
                con=sync_conn,
                if_exists="append",
                index=False,
            ),
        )
        await session.commit()


async def import_bot_data(bytes_io: BinaryIO, file_name: str) -> DataFrame:
    """Импорт файла для парсинга в сервис."""
    try:
        data_frame = read_excel(bytes_io)
        await save_bot_data_to_db(data_frame)
        file_path = os.path.join(settings.import_files_root, file_name)
        write_bytesio_to_file(file_path, bytes_io)
        return data_frame
    except (ValueError, ValidationError):
        raise ImportExcelFileError
