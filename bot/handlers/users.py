import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from fluent.runtime import FluentLocalization

from bot.core.exceptions import ImportExcelFileError, PriceParseError
from bot.core.utils import send_answer_with_grid
from bot.services.import_data import import_bot_data
from bot.services.parser import calc_avg_parse_price

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, l10n: FluentLocalization):
    """Стартовое сообщение от бота."""
    await message.answer(l10n.format_value("intro"))


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, l10n: FluentLocalization):
    """Справка по сервису."""
    await message.answer(l10n.format_value("help"))


@router.message(F.document)
async def download_document(
    message: Message, bot: Bot, l10n: FluentLocalization
):
    try:
        if message.caption and len(message.caption) > 1000:
            return await message.reply(
                l10n.format_value("too-long-caption-error")
            )
        await message.answer(l10n.format_value("file-import"))
        bytes_io = await bot.download(message.document)
        file_name = (
            f"{message.document.file_unique_id}_{message.document.file_name}"
        )
        data_frame = await import_bot_data(bytes_io, file_name)
        await message.answer(l10n.format_value("file-load"))
        await send_answer_with_grid(message, data_frame)
        await message.answer(l10n.format_value("file-parse"))
        avg_price = await calc_avg_parse_price(data_frame)
        await send_answer_with_grid(message, avg_price)
        await message.answer(
            text="Спасибо, что воспользовались ботом!", show_alert=True
        )
    except ImportExcelFileError:
        error_message = l10n.format_value("error-excel-file")
        logger.exception(error_message)
        await message.answer(error_message)
    except PriceParseError:
        error_message = l10n.format_value("error-parse-file")
        logger.exception(error_message)
        await message.answer(error_message)


@router.message()
async def unsupported_types(message: Message, l10n: FluentLocalization):
    """Хэндлер на неподдерживаемые типы сообщений."""
    if message.content_type not in (
        ContentType.NEW_CHAT_MEMBERS,
        ContentType.LEFT_CHAT_MEMBER,
        ContentType.VIDEO_CHAT_STARTED,
        ContentType.VIDEO_CHAT_ENDED,
        ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED,
        ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED,
        ContentType.NEW_CHAT_PHOTO,
        ContentType.DELETE_CHAT_PHOTO,
        ContentType.SUCCESSFUL_PAYMENT,
        ContentType.NEW_CHAT_TITLE,
        ContentType.PINNED_MESSAGE,
    ):
        await message.reply(
            l10n.format_value("unsupported-message-type-error")
        )
