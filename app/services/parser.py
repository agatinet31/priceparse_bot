import asyncio
import re
from decimal import Decimal

import httpx

from app.exceptions import PriceParseNotFoundError, PriceParseRequestError
from lxml.etree import HTML
from pandas import DataFrame

REQUEST_HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

MONEY = re.compile(r"\d*(\d\.?|\.\d{1,2})")


async def parse_price(url: str, xpath: str) -> Decimal:
    """Парсит цену по товару с сайта."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=REQUEST_HEADERS,
            )
            response.raise_for_status()
            data = (
                HTML(response.text)
                .xpath(f"{xpath}/text()")[0]
                .translate(str.maketrans("", "", " \n\t\r"))
                .replace(",", ".")
            )
            return Decimal(MONEY.search(data).group(0))
    except httpx.HTTPError as exc:
        raise PriceParseRequestError(url, xpath) from exc
    except (AttributeError, IndexError) as exc:
        raise PriceParseNotFoundError(url, xpath) from exc


async def calc_avg_parse_price(data_frame: DataFrame) -> DataFrame:
    """Возвращает среднюю цену распарсиных данных по товарам из data_frame."""
    tasks = [
        parse_price(*parse_data)
        for parse_data in data_frame[["url", "xpath"]].values.tolist()
    ]
    data_frame["price"] = await asyncio.gather(*tasks)
    grouped = data_frame[["title", "url", "price"]].groupby(["title", "url"])
    return grouped.mean()
