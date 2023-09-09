from core.db import get_async_session
from core.decorators import validate_data_schema
from models.product import LinkProduct
from pandas import DataFrame
from schemas import LinkProductShema


@validate_data_schema(data_schema=LinkProductShema)
async def save_bot_data_to_db(data: DataFrame):
    """Импортирует в БД данные по ссылкам на продукцию."""
    async with get_async_session() as session:
        conn = await session.connection()
        await conn.run_sync(
            lambda sync_conn: data.to_sql(
                LinkProduct.__tablename__,
                con=sync_conn,
                if_exists="replace",
                index=False,
            ),
        )
        await session.commit()
