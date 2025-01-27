from database.chroma_db import get_global_collection
from server import create_server

# Creates backend server and initialises vector database
app = create_server()
collection = get_global_collection()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
