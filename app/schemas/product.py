from lxml.etree import XPath, XPathSyntaxError
from pydantic import AnyHttpUrl, BaseModel, Field, validator


class LinkProductShema(BaseModel):
    """Класс схемы ссылки на продукцию."""

    title: str = Field(..., min_length=1)
    url: AnyHttpUrl
    xpath: str

    @validator("xpath")
    def validate_syntax_xpath(cls, data):
        try:
            XPath(data)
        except XPathSyntaxError:
            raise ValueError("XPath invalid expression!")
        return data
