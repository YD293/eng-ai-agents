from qdrant_client import QdrantClient, models

class QdrantDB:
    def __init__(self, host: str, port: int, collection_name: str):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)
    
    def create_collection(self, embedding_dimension):
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(collection_name=self.collection_name)
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=embedding_dimension,
                distance=models.Distance.COSINE,
            )
    )