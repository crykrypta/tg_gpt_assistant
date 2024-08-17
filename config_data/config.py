from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class OpenAI:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    openai: OpenAI


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    print("BOT_TOKEN:", env('BOT_TOKEN', 'Не найден'))
    print("OPENAI_API_KEY:", env('OPENAI_API_KEY', 'Не найден'))
    
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        openai=OpenAI(token=env('OPENAI_API_KEY'))
    )
