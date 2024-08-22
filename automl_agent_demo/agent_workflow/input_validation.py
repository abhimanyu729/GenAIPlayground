from pydantic import BaseModel, validator, HttpUrl, constr, ValidationError
from pathlib import Path
from typing import Union

class DatasetLocationModel(BaseModel):
    location: Union[HttpUrl, constr(strip_whitespace=True)]

    @validator('location', pre=True)
    def check_location(cls, v):
        if cls.is_valid_local_path(v):
            if cls.has_valid_extension(v):
                return v
            raise ValueError('The local path does not point to a CSV or Parquet file')

        if cls.is_valid_url(v):
            if cls.has_valid_extension(v):
                return v
            raise ValueError('The URL does not point to a CSV or Parquet file')

        raise ValueError('The provided location is not a valid URL or local path')

    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            HttpUrl(url=url)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_valid_local_path(path: str) -> bool:
        return Path(path).exists()

    @staticmethod
    def has_valid_extension(path: str) -> bool:
        valid_extensions = ('.csv', '.parquet')
        return path.lower().endswith(valid_extensions)

    @classmethod
    def validate_location(cls, location: str) -> bool:
        try:
            cls(location=location)
            return True
        except ValidationError:
            return False