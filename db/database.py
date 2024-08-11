from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from utils.for_text import url_to_mkd, split_text_to_chunks


# Получаем хранилище с чанками
doc_url = 'https://docs.google.com/document/d/1YhUEX9fZDNTeE3eJ-yXskxZG46LsTRYvXjZ9Ij-t3Gw/edit'
chunks = split_text_to_chunks(url_to_mkd(doc_url), 200)

# Создаем векторное хранилище
embeddings = OpenAIEmbeddings()
faiss_db = FAISS.from_documents(chunks, embeddings)
