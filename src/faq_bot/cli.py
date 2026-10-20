import sys
from pathlib import Path

from .bot import FAQBot

DEFAULT = Path(__file__).resolve().parents[2] / "data" / "faqs.json"


def main() -> None:
    bot = FAQBot(DEFAULT)
    print("FAQ assistant. Type a question (or 'quit').")
    while True:
        try:
            q = input("> ").strip()
        except EOFError:
            break
        if q == "quit":
            break
        if not q:
            continue
        r = bot.ask(q)
        print(f"[{r['id']} | score={r['score']:.2f}] {r['answer']}")


if __name__ == "__main__":
    main()
