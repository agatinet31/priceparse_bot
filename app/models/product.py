from sqlalchemy import Column, Text

from app.core.db import Base


class LinkProduct(Base):
    """Модель ссылок на продукцию."""

    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    xpath = Column(Text, nullable=False)

    def __repr__(self):
        """Возвращает информацию по ссылке на товар."""
        return f"<{self.title}> " f"{self.url} => " f"{self.xpath}"
