
from chatbot.backend.services.vector_db.db import vector_db

vector_db.delete_data(
    field="doc_source",
    match_results= ['Dylan Resume.pdf']
)