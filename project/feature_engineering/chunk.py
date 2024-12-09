from typing import List
from domain.document import Document, ChunkedDocument
from embedding_model import EmbeddingModel
from clearml import Task, Logger

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)


def chunk_and_embed_documents(
    documents: List[Document], embedding_model: EmbeddingModel
) -> list[ChunkedDocument]:
    task = Task.init(project_name="RAG Project", task_name="Chunk and embed documents")
    logger = Logger.current_logger()

    all_chunked_documents = []
    chunk_count = 0
    logger.report_text(f"Chunk and embed documents start, documents count: {len(documents)}")
    for id, document in enumerate(documents):
        chunked_document = ChunkedDocument(document)
        chunks = chunk_text(document.content, embedding_model.max_seq_length, embedding_model.model_name)
        logger.report_text(f"[{id + 1}/{len(documents)}] Chunk text success for document: {document.metadata['title']}, chunks count: {len(chunks)}")
        for chunk in chunks:
            embedding = embedding_model.encode(chunk)
            chunked_document.add_chunk(chunk, embedding)
            chunk_count += 1
        all_chunked_documents.append(chunked_document)
    
    logger.report_text(f"Chunk documents success, documents count: {len(all_chunked_documents)}, chunks count: {chunk_count}")
    task.close()
    return all_chunked_documents


def chunk_text(
    text: str,
    max_input_length,
    model_name,
    chunk_size: int = 1024,
    chunk_overlap: int = 128,
) -> list[str]:
    
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"], chunk_size=chunk_size, chunk_overlap=0
    )
    text_split_by_characters = character_splitter.split_text(text)

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=chunk_overlap,
        tokens_per_chunk=max_input_length,
        model_name=model_name,
    )
    chunks_by_tokens = []
    for section in text_split_by_characters:
        chunks_by_tokens.extend(token_splitter.split_text(section))

    return chunks_by_tokens
