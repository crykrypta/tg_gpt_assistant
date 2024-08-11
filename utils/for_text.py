from langchain.text_splitter import (RecursiveCharacterTextSplitter,
                                     MarkdownHeaderTextSplitter)
from langchain.docstore.document import Document

import requests
import re
from tiktoken import get_encoding
import matplotlib.pyplot as plt

doc_url = 'https://docs.google.com/document/d/1YhUEX9fZDNTeE3eJ-yXskxZG46LsTRYvXjZ9Ij-t3Gw/edit'


# Загружает текст документа из Google Docs.
def _load_doc(url: str) -> str:
    """Возвращает текст документа из Google Docs."""
    doc_id = re.findall(r'/document/d/(.+)/', url)
    if doc_id is None:
        raise ValueError('Invalid Google Doc URL')

    response = requests.get(f'https://docs.google.com/document/d/{doc_id[0]}/export?format=txt')

    if response.status_code == 200:
        return response.text
    else:
        raise ValueError('Failed to load document')


# Приводит текст документа к формату Markdown
def _txt_to_mkd(text: str) -> str:
    """Приводит текст документа к формату Markdown
    # Римские цифры.
    # Арабские цифры."""
    # Заголовки первого уровня
    def _replace_header_1(match):
        return f'# {match.group(2)}\n{match.group(2)}'
    text = re.sub(
        r'(I{1,3}|IV|V|VI{1,3}|IX|X{0,3}|XI{1,3}|XIV|XVI{1,3}\.)\s*(.+)',
        _replace_header_1, text, flags=re.M
    )
    return text


# Преобразует текст документа из Google Docs в формат Markdown.
def url_to_mkd(url: str) -> str:
    """Приводит текст документа из Google Docs к формату Markdown."""
    return _txt_to_mkd(_load_doc(url))


# Считает количество токенов в тексте.
def _number_of_tokens(text: str, encoding_name: str = 'cl100k_base') -> int:
    """Возвращает количество токенов в тексте."""
    encoding = get_encoding(encoding_name)
    return len(encoding.encode(text))


def _plot_by_tokens(source_chunks: list[Document], encoding_name) -> None:
    token_counts = [_number_of_tokens(chunk.page_content, encoding_name)
                    for chunk in source_chunks]

    plt.hist(token_counts, bins=20, alpha=0.5, label='Source Chunks')
    plt.title('Distribution of Source Chunk Token Counts')
    plt.xlabel('Token Count')
    plt.ylabel('Frequency')
    plt.show()


# Разбивает текст на части по заголовкам.
def split_text_to_chunks(text: str, max_count) -> list[str]:
    # Разбиваем текст на части по заголовкам
    headers_to_split_on = [('#', 'Header 1')]
    mkd_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    fragments = mkd_splitter.split_text(text)

    # Дорезаем до max_count с помощью рекурсивного разбиения текста
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_count,
        chunk_overlap=0,
        length_function=lambda x: _number_of_tokens(x, 'cl100k_base')
    )
    # Собираем все части в список документов
    source_chunks = [
        Document(page_content=chunk, metadata=fragment.metadata)
        for fragment in fragments
        for chunk in r_splitter.split_text(fragment.page_content)
    ]
    return source_chunks


# Выводим длины
chunks = split_text_to_chunks(url_to_mkd(doc_url), 2000)


_plot_by_tokens(chunks, 'cl100k_base')
