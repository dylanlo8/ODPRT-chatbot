from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"


loader = PyPDFLoader("")  # path to documents
documents = loader.load()
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
# change to dylans embedding model

semantic_chunker = SemanticChunker(embed_model,
                                   breakpoint_threshold_type="percentile")

semantic_chunks = (semantic_chunker
                   .create_documents([d.page_content for d in documents]))

# for semantic_chunk in semantic_chunks:
#     if "Effect of Pre-training Tasks" in semantic_chunk.page_content:
#         print(semantic_chunk.page_content)
#         print(len(semantic_chunk.page_content))
