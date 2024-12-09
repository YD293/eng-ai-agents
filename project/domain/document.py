from typing import List
import hashlib

class Document:
    def __init__(self, content: str, metadata: dict = None):
        self.content = content
        self.metadata = metadata

class Chunk:
    def __init__(self, chunk_content: str, doc_id: str, doc_metadata: dict, embedding: List[float]):
        self.chunk_content = chunk_content
        self.doc_id = doc_id
        self.embedding = embedding
        self.chunk_id = hashlib.md5((doc_id + ":" + chunk_content).encode()).hexdigest()
        self.doc_metadata = doc_metadata
    
    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "chunk_content": self.chunk_content,
            "doc_id": self.doc_id,
            "doc_metadata": self.doc_metadata,
        }

class ChunkedDocument:
    def __init__(self, document: Document):
        self.doc_id = hashlib.md5(document.content.encode()).hexdigest()
        self.document = document
        self.chunks = []
    
    def add_chunk(self, chunk_content: str, embedding: List[float]):
        chunk = Chunk(chunk_content, self.doc_id, self.document.metadata, embedding)
        self.chunks.append(chunk)
        
        
