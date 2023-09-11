import asyncio
from decimal import Decimal
from typing import Awaitable, Dict, Tuple

from aiogram.enums import ParseMode
from aiogram.types import Message
from pandas import DataFrame

from bot.core.config import settings


async def gather_dict(
    tasks: Dict[int, Awaitable[Decimal]]
) -> Dict[int, Decimal]:
    """Выполнения списка корутин."""

    async def mark(
        key: int, coroutine: Awaitable[Decimal]
    ) -> Tuple[int, Decimal]:
        return key, await coroutine

    return {
        key: result
        for key, result in await asyncio.gather(
            *(mark(key, coroutine) for key, coroutine in tasks.items())
        )
    }


def write_bytesio_to_file(filename, bytesio):
    """Запись контента из BytesIO в файл."""
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())


async def send_answer_with_grid(message: Message, data_frame: DataFrame):
    grid = data_frame.to_markdown(tablefmt="grid")
    if len(grid) > settings.max_len_telegram_message:
        for idx in range(0, len(grid), settings.max_len_telegram_message):
            await message.answer(
                f"```{grid[idx: idx + settings.max_len_telegram_message]}```",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
    else:
        await message.answer(f"```{grid}```", parse_mode=ParseMode.MARKDOWN_V2)
