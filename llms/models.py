import re


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
