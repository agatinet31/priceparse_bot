import functools

from pandas import DataFrame
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


def validate_data_schema(data_schema: ModelMetaclass):
    """Декоратор валидации DataFrame."""

    class ValidationWrap(BaseModel):
        data_frame_dict: list[data_schema]

    def decorator_validate_data_frame(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for data_frame in args:
                if not isinstance(data_frame, DataFrame):
                    raise TypeError("Args function is not type DataFrame!")
                ValidationWrap(
                    data_frame_dict=data_frame.to_dict(orient="records")
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator_validate_data_frame
