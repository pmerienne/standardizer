import os

from haystack import Document
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.document_stores.chroma import ChromaDocumentStore

CHROMA_ROOT_PATH = os.getenv("CHROMA_ROOT_PATH")


def get_retriever(store_name: str) -> ChromaQueryTextRetriever:
    document_store = get_store(store_name)
    retriever = ChromaQueryTextRetriever(document_store=document_store)
    return retriever


def get_store(store_name: str) -> ChromaDocumentStore:
    document_store = ChromaDocumentStore(persist_path=f"{CHROMA_ROOT_PATH}/{store_name}.chroma")
    return document_store


def delete_all(store_name: str):
    document_store = get_store(store_name)
    documents = document_store.filter_documents()
    document_ids = [document.id for document in documents]
    if document_ids:
        document_store.delete_documents(document_ids)


def find_all(store_name: str) -> list[Document]:
    document_store = get_store(store_name)
    return document_store.filter_documents()


def count(store_name: str):
    document_store = get_store(store_name)
    return document_store.count_documents()
