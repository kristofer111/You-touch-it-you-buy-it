from dataclasses import dataclass


@dataclass
class DbConfig:
    user: str
    password: str
    database: str
    host: str