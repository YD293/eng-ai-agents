import gradio as gr

from ollama import chat
from feature_engineering.rag import generate_rag_prompt
from embedding_model import EmbeddingModel
from qdrant_db import QdrantDB


def query_rag_system(question):
    global embedding_model, qdrant_db

    prompt = generate_rag_prompt(question, embedding_model, qdrant_db)

    stream = chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    response_text = ""
    for chunk in stream:
        content = chunk["message"]["content"]
        response_text += content
        yield response_text


PREDEFINED_QUESTIONS = [
    "Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
    "Can you provide me with code for this task?",
]


if __name__ == "__main__":
    embedding_model = EmbeddingModel("cpu", "all-MiniLM-L6-v2")
    qdrant_db = QdrantDB(host="localhost", port=6333, collection_name="ros2_doc")

    with gr.Blocks() as rag_app:
        gr.Markdown("# RAG for ROS2")

        with gr.Row():
            question_dropdown = gr.Dropdown(
                choices=PREDEFINED_QUESTIONS,
                label="Select a Question",
                value=None,
            )
            question_input = gr.Textbox(
                label="Or enter your own question",
                value="",
            )

        def handle_question(dropdown_question, input_question):
            print('dropdown_question', dropdown_question)
            print('input_question', input_question)
            question = dropdown_question if dropdown_question else input_question
            yield from query_rag_system(question)

        gr.Markdown("### Answer")
        answer_box = gr.Markdown()
        submit_button = gr.Button("Submit")

        submit_button.click(
            fn=handle_question,
            inputs=[question_dropdown, question_input],
            outputs=answer_box,
            api_name="query",
        )

    rag_app.launch(server_name="localhost", server_port=7860)
