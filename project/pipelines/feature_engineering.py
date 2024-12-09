from typing import List

from domain.document import ChunkedDocument
from qdrant_db import QdrantDB
from nosql_db import NoSqlDB
from feature_engineering.query_data_warehouse import query_data_warehouse
from feature_engineering.clean import clean_documents
from embedding_model import EmbeddingModel
from feature_engineering.chunk import chunk_and_embed_documents
from qdrant_client import models
from clearml import Task, Logger

def feature_engineering(db: NoSqlDB, embedding_model: EmbeddingModel, qdrant_db: QdrantDB):
    documents = query_data_warehouse(db, with_clearml=False)
    documents = clean_documents(documents)
    chunked_documents = chunk_and_embed_documents(documents, embedding_model)

    save_chunked_documents_to_qdrant(chunked_documents, qdrant_db)
    return chunked_documents


def save_chunked_documents_to_qdrant(
    chunked_documents: List[ChunkedDocument], qdrant_db: QdrantDB
):
    task = Task.init(project_name="RAG Project", task_name="Save chunked documents to qdrant")
    for chunked_document in chunked_documents:
        for chunk in chunked_document.chunks:
            qdrant_db.client.upload_points(
                collection_name="ros2_doc",
                    points=[
                        models.PointStruct(
                            id=chunk.chunk_id, vector=chunk.embedding, payload=chunk.to_dict()
                        )
                    ]
                )
    logger = Logger.current_logger()
    logger.report_text(f"Save chunked documents to qdrant success, chunks count: {len(chunked_documents)}")
    task.close()

if __name__ == "__main__":
    embedding_model = EmbeddingModel("cpu", "all-MiniLM-L6-v2")
    
    db_config = {
        "mongo_uri": "mongodb://127.0.0.1:27017/",
        "db_name": "nosql_db",
        "collection_name": "ros2_doc",
    }
    db = NoSqlDB(db_config)
    qdrant_db = QdrantDB(host="127.0.0.1", port=6333, collection_name="ros2_doc")
    qdrant_db.create_collection(embedding_model.embedding_dimension)
    feature_engineering(db, embedding_model, qdrant_db)
