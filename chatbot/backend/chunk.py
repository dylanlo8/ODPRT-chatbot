from chatbot.backend.services.embedding_model import embedding_model
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader
import os


def chunk(embed_model, path):

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    loader = PyPDFLoader(path)
    documents = loader.load()
    semantic_chunker = SemanticChunker(embed_model,
                                       breakpoint_threshold_type="percentile")
    semantic_chunks = (semantic_chunker
                       .create_documents([d.page_content for d in documents]))
    return semantic_chunks


print(chunk(embedding_model, "notebooks/1810.04805v2.pdf"))
