import yaml

from typing import (
    Dict, 
    Optional
)

from pydantic import BaseModel

from .types import Alias


class Account(BaseModel):
    api_key: str
    secret: str
    password: Optional[str]
    proxy: Optional[str]


class Config(BaseModel):
    okx: Optional[Dict[Alias, Account]] | Account
    huobi: Optional[Dict[Alias, Account]] | Account
    bybit: Optional[Dict[Alias, Account]] | Account

    @classmethod
    def from_yaml_file(cls, file_path: str):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return cls(**data)
