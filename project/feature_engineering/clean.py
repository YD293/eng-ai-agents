import re
from typing import List
from domain.document import Document
from clearml import Task, Logger

def clean_text(text: str) -> str:
    if text is None:
        return None
    text = re.sub(r"[^\w\s.,!?]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_documents(documents: List[dict]):
    task = Task.init(project_name="RAG Project", task_name="Clean documents")

    cleaned_docs = []
    for doc in documents:
        content = clean_text(doc["content"])
        title = clean_text(doc["title"])
        subtitle = clean_text(doc["subtitle"])
        metadata = {
            "title": title,
            "subtitle": subtitle,
            "url": doc["url"],
        }
        cleaned_docs.append(Document(content, metadata))
    logger = Logger.current_logger()
    logger.report_text(f"Clean documents success, documents count: {len(cleaned_docs)}")
    task.close()
    return cleaned_docs
