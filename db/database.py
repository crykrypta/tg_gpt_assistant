# sys.path.append(os.path.join(os.getcwd(), 'GPT_assist')) # type: ignore
# import os
# import sys
import openai

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from utils.for_text import url_to_mkd, split_text_to_chunks
from config_data.config import load_config


config = load_config()

openai.api_key = config.openai.token

# Получаем хранилище с чанками
doc_url = 'https://docs.google.com/document/d/1YhUEX9fZDNTeE3eJ-yXskxZG46LsTRYvXjZ9Ij-t3Gw/edit'
chunks = split_text_to_chunks(url_to_mkd(doc_url), 200)

# Создаем векторное хранилище
embeddings = OpenAIEmbeddings()
faiss_db = FAISS.from_documents(chunks, embeddings)
