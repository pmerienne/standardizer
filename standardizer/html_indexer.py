import glob

from haystack import Pipeline
from haystack.components.converters import HTMLToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from loguru import logger

from standardizer.chroma import delete_all, get_store


def index(store_name: str, path: str):
    file_names = glob.glob(path)

    document_store = get_store(store_name)

    pipeline = Pipeline()
    pipeline.add_component(
        "converter", HTMLToDocument(extraction_kwargs={"with_metadata": True})
    )
    pipeline.add_component("cleaner", DocumentCleaner())
    pipeline.add_component(
        "splitter", DocumentSplitter(split_by="sentence", split_length=5)
    )
    pipeline.add_component("writer", DocumentWriter(document_store=document_store))
    pipeline.connect("converter", "cleaner")
    pipeline.connect("cleaner", "splitter")
    pipeline.connect("splitter", "writer")

    logger.info("Indexing :\n- " + "\n- ".join(file_names))
    pipeline.run({"converter": {"sources": file_names}})
    logger.info("Indexed !")


if __name__ == "__main__":
    delete_all("Pédagogie")
    index("Pédagogie", "./data/oc/*.html")
