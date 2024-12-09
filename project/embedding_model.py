from sentence_transformers.SentenceTransformer import SentenceTransformer


class EmbeddingModel:
    def __init__(self, device, model_name) -> None:
        self.device = device
        self.model_name = model_name
        self.model = SentenceTransformer(
            self.model_name, device=self.device
        )
        self.max_seq_length = self.model.max_seq_length
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, text):
        return self.model.encode(text)
