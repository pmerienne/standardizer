import os

from haystack_integrations.components.connectors.langfuse import LangfuseConnector

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-9e6042e3-3c53-4030-b3d2-dadc851a1f52"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-caeac624-5814-4de4-a0a7-7730301a5f59"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"
os.environ["HAYSTACK_CONTENT_TRACING_ENABLED"] = "True"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def create_tracer(name: str):
    return LangfuseConnector(name)
