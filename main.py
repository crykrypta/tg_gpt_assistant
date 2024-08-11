import os
import sys
import openai

sys.path.append(os.path.join(os.getcwd(), 'GPT_assist'))

from config_data.config import load_config
from db.database import faiss_db
from llms.models import search_documents


config = load_config()
openai.api_key = config.openai.token

client = openai.OpenAI()
os.environ['OPENAI_API_KEY'] = config.openai.token


def answer_index(system, user, db, k=4, verbose=True):
    """Возвращает ответ на запрос пользователя"""
    docs = search_documents(user, db, k=k, verbose=verbose)

    user_query = f'Документы с информацией: \n{docs}'
    '\n\nВопрос пользователя: {user}'

    completions = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user_query}
        ]
    )
    return completions.choices[0].message.content