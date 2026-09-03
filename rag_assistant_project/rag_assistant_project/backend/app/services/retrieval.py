from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import get_settings


class Retriever:
    def __init__(self):
        s = get_settings()

        self.model = SentenceTransformer(
        s.embedding_model,
        token=False )
                   
        self.top_k = s.top_k

        vector_path = Path(s.vector_store_path)

        index_path = vector_path / "mars_faiss.index"
        metadata_path = vector_path / "chunks.json"

        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Chunk metadata not found: {metadata_path}"
            )

        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print(f"Loaded FAISS index with {self.index.ntotal} vectors")

    def search(self, question: str):
        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        k = min(self.top_k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            item = self.metadata[int(idx)]

            results.append({
                "text": item["text"],
                "source": item.get("filename", "unknown"),
                "chunk": item.get("chunk_id", "unknown"),
                "url": item.get("source_url", ""),
                "score": float(score)
            })

        return results