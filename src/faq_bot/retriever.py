"""BM25 retriever implemented with the standard library only."""
import math
import re
from collections import Counter

STOPWORDS = {
    "a", "an", "the", "is", "are", "i", "do", "does", "can", "how", "to", "my",
    "me", "of", "in", "on", "for", "and", "or", "it", "what", "you", "your",
    "we", "will", "be", "with", "this", "that", "there",
}


# Query-time synonyms: map informal phrasing to the vocabulary used in the FAQs.
SYNONYMS = {
    "2fa": ["two", "factor", "authentication"],
    "mfa": ["two", "factor", "authentication"],
    "money": ["refund"],
    "forgot": ["reset"],
    "stop": ["cancel"],
    "remove": ["delete"],
    "update": ["change"],
    "company": ["team"],
    "pricing": ["plan"],
}


def stem(token: str) -> str:
    """Very light suffix stripping so 'invoices' matches 'invoice'."""
    if token.endswith("ing") and len(token) > 6:
        return token[:-3]
    if token.endswith("s") and not token.endswith("ss") and len(token) > 4:
        return token[:-1]  # 'invoices' -> 'invoice' (never strip 'es': it breaks 'invoice')
    return token


def tokenize(text: str, expand: bool = False) -> list[str]:
    raw = re.findall(r"[a-z0-9]+", text.lower())
    out: list[str] = []
    for t in raw:
        if t in STOPWORDS:
            continue
        out.append(stem(t))
        if expand:
            out.extend(stem(x) for x in SYNONYMS.get(t, []))
    return out


class BM25Retriever:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = [tokenize(d) for d in documents]
        self.n = len(self.docs)
        self.avgdl = sum(len(d) for d in self.docs) / max(self.n, 1)
        df = Counter()
        for d in self.docs:
            df.update(set(d))
        self.idf = {
            t: math.log(1 + (self.n - f + 0.5) / (f + 0.5)) for t, f in df.items()
        }

    def score(self, query: str) -> list[float]:
        q = tokenize(query, expand=True)
        scores = []
        for d in self.docs:
            tf = Counter(d)
            s = 0.0
            for t in q:
                if t not in tf:
                    continue
                f = tf[t]
                denom = f + self.k1 * (1 - self.b + self.b * len(d) / self.avgdl)
                s += self.idf[t] * f * (self.k1 + 1) / denom
            scores.append(s)
        return scores

    def search(self, query: str, top_k: int = 3) -> list[tuple[int, float]]:
        scores = self.score(query)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
