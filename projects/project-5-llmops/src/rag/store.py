"""Chroma-backed document store + retriever."""
from __future__ import annotations

from dataclasses import dataclass

import chromadb
from sentence_transformers import SentenceTransformer


@dataclass(frozen=True)
class Doc:
    id: str
    text: str
    metadata: dict


class DocStore:
    def __init__(self, url: str, collection: str = "docs"):
        self.client = chromadb.HttpClient(host=url.replace("http://", "").split(":")[0],
                                            port=int(url.split(":")[-1]))
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(collection)

    def add(self, docs: list[Doc]):
        if not docs:
            return
        ids = [d.id for d in docs]
        texts = [d.text for d in docs]
        metas = [d.metadata for d in docs]
        embeddings = self.encoder.encode(texts).tolist()
        self.collection.add(ids=ids, documents=texts, metadatas=metas, embeddings=embeddings)

    def search(self, query: str, k: int = 4) -> list[Doc]:
        emb = self.encoder.encode(query).tolist()
        r = self.collection.query(query_embeddings=[emb], n_results=k)
        out: list[Doc] = []
        for id_, text, meta in zip(r["ids"][0], r["documents"][0], r["metadatas"][0]):
            out.append(Doc(id=id_, text=text, metadata=meta or {}))
        return out
