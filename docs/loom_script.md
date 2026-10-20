# 5-minute Loom script

Have these open before recording: terminal in the repo folder, the GitHub README, `architecture.png`, and `eval/eval_set.json`.

## 0:00 - 1:00 | Problem and motivation
- "Support bots that always answer are dangerous: they give confident wrong answers."
- Show the "cancel my pizza order" example in the README intro.
- "I built a FAQ bot whose real goal is to know when to say 'I don't know', and to measure that."

## 1:00 - 3:00 | Live demo (type these live)
1. `python3 eval/run_eval.py` and point at 15/15 in-scope and 7/10 refusal.
2. `PYTHONPATH=src python3 -m faq_bot.cli`
3. Happy path: `how can i get my money back` -> refund answer (synonym expansion at work).
4. Plural case: `download invoice pdf` -> invoice answer (the stemmer fix).
5. **Edge case handled gracefully:** `tell me a joke`, then press Enter on empty input, then `???` -> fallback message, no crash, no wrong answer.
6. **Honest failure:** `how do I cancel my pizza order` -> wrongly answered. Say: "This is a known limitation, BM25 only sees word overlap."

## 3:00 - 4:00 | Architecture walkthrough (show the diagram)
- Follow the arrows: CLI -> FAQBot -> tokenizer (stopwords, stemmer, synonyms) -> BM25 -> threshold gate -> answer or fallback.
- Storage is two JSON files. No external APIs, fully offline.
- Dashed lines = setup and evaluation paths.

## 4:00 - 5:00 | What I would build differently
- Add an embedding model and a reranker so semantic out-of-scope queries get rejected.
- Build a bigger eval set written by other people, and split it into tune/test so the threshold is not tuned on the test set.
- Replace the hand-written synonym map with learned query expansion.
- Close with the repo link.
