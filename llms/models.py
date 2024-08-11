import re
import os
import openai
import logging

from config_data.config import load_config

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='#%(levelname)-8s [%(name)s]: '
                    '%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка конфигурации
config = load_config()

# Настройка Openai API
openai.api_key = config.openai.token
client = openai.OpenAI()
os.environ['OPENAI_API_KEY'] = config.openai.token


# Поиск документов по FAISS
def search_documents(query, db, k=4, verbose=False):
    """Возвращает наиболее релевантные документы для заданного запроса"""
    separator = '\n=================================================='
    docs = db.similarity_search(query, db, k=k, verbose=verbose)
    if verbose:
        print(separator)
    message_content = re.sub(
        r'\n{2}', ' ', '\n'.join([f'\nDocument №{i+1}: {doc.page_content}\n'
                                  for i, doc in enumerate(docs)]))
    if verbose:
        print(separator)
    return message_content


# Model I
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
