from qdrant_db import QdrantDB
from embedding_model import EmbeddingModel
from clearml import Task, Logger


def generate_rag_prompt(
    query: str, embedding_model: EmbeddingModel, qdrant_db: QdrantDB
):
    task = Task.init(project_name="RAG Project", task_name="RAG")
    logger = Logger.current_logger()

    query_embedding = embedding_model.encode(query)
    similar_chunks = qdrant_db.client.search(
        collection_name=qdrant_db.collection_name, query_vector=query_embedding
    )

    logger.report_text("Similar chunks:")
    for id, chunk in enumerate(similar_chunks):
        logger.report_text(f"{id}: {chunk.payload}")
    logger.report_text("-" * 100)

    chunk_str = ""
    for chunk in similar_chunks:
        chunk_str += f"Document title: {chunk.payload['doc_metadata']['title']}\n"
        subtitle = chunk.payload["doc_metadata"]["subtitle"]
        if subtitle:
            chunk_str += f"Document subtitle: {subtitle}\n"
        chunk_str += f"Document url: {chunk.payload['doc_metadata']['url']}\n"
        chunk_str += f"Chunk Content: {chunk.payload['chunk_content']}\n"
        chunk_str += "-" * 100 + "\n"

    prompt = f"""
    You are a helpful assistant for ROS2.
    You are given the following chunks:
    {chunk_str}
    Please answer the user's question based on the chunks(with document metadata).
    User's question: {query}
    Please refer to the document metadata after your answer.
    """
    task.close()
    return prompt


if __name__ == "__main__":
    query = 'Tell me how can I navigate to a specific pose - include replanning aspects in your answer.'
    embedding_model = EmbeddingModel("cpu", "all-MiniLM-L6-v2")
    qdrant_db = QdrantDB(host="localhost", port=6333, collection_name="ros2_doc")
    print(generate_rag_prompt(query, embedding_model, qdrant_db))
