from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    # admin_ids: list[int]|None


@dataclass
class Database:
    bd_login: str
    bd_password: str
    bd_host: str
    bd_name: str


@dataclass
class Config:
    tg_bot: TgBot
    db: Database


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        db=Database(
            bd_login=env("BD_LOGIN"),
            bd_password=env("BD_PASSWORD"),
            bd_host=env("BD_HOST"),
            bd_name=env("BD_NAME"),
        ),
    )
