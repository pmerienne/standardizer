import os

from haystack import Pipeline
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.connectors.langfuse import LangfuseConnector
from notion_haystack import NotionExporter


def get_notion_retriever(page_id: str) -> InMemoryBM25Retriever:
    if page_id.startswith("https://www.notion.so/"):
        page_id = page_id.split("?")[0]
        page_id = page_id.split("-")[-1]

    in_memory_store = InMemoryDocumentStore()
    exporter = NotionExporter(api_token=os.getenv("NOTION_API_TOKEN"))

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("tracer", LangfuseConnector("Notion indexer"))
    indexing_pipeline.add_component("exporter", exporter)
    indexing_pipeline.add_component("cleaner", DocumentCleaner())
    indexing_pipeline.add_component(
        "splitter", DocumentSplitter(split_by="sentence", split_length=5)
    )
    indexing_pipeline.add_component(
        "writer", DocumentWriter(document_store=in_memory_store)
    )
    indexing_pipeline.connect("exporter", "cleaner")
    indexing_pipeline.connect("cleaner", "splitter")
    indexing_pipeline.connect("splitter", "writer")

    indexing_pipeline.run({"exporter": {"page_ids": [page_id]}})

    retriever = InMemoryBM25Retriever(document_store=in_memory_store)
    return retriever
