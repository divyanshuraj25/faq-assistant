import json
from pathlib import Path

from .retriever import BM25Retriever

FALLBACK = "Sorry, I couldn't find an answer to that. Please contact support@example.com."


class FAQBot:
    def __init__(self, faq_path: str | Path, min_score: float = 1.5):
        self.min_score = min_score
        self.faqs = json.loads(Path(faq_path).read_text(encoding="utf-8"))
        corpus = [f["question"] + " " + f["answer"] for f in self.faqs]
        self.retriever = BM25Retriever(corpus)

    def ask(self, query: str) -> dict:
        hits = self.retriever.search(query, top_k=1)
        idx, score = hits[0]
        if score < self.min_score:
            return {"id": None, "answer": FALLBACK, "score": score}
        return {"id": self.faqs[idx]["id"], "answer": self.faqs[idx]["answer"], "score": score}
