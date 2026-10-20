"""Evaluation suite: accuracy on in-scope questions, refusal rate on out-of-scope ones."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from faq_bot import FAQBot  # noqa: E402
from faq_bot.bot import FALLBACK  # noqa: E402


def main() -> int:
    bot = FAQBot(ROOT / "data" / "faqs.json")
    cases = json.loads((ROOT / "eval" / "eval_set.json").read_text())
    in_ok = in_n = out_ok = out_n = 0
    failures = []
    for c in cases:
        r = bot.ask(c["query"])
        got = "NONE" if r["answer"] == FALLBACK else r["id"]
        ok = got == c["expected"]
        if c["expected"] == "NONE":
            out_n += 1; out_ok += ok
        else:
            in_n += 1; in_ok += ok
        if not ok:
            failures.append((c["query"], c["expected"], got, round(r["score"], 2), c.get("known_limitation", False)))
    print(f"In-scope accuracy   : {in_ok}/{in_n} ({100*in_ok/in_n:.0f}%)")
    print(f"Out-of-scope refusal: {out_ok}/{out_n} ({100*out_ok/out_n:.0f}%)")
    for q, e, g, s, known in failures:
        tag = "KNOWN" if known else "FAIL "
        print(f"  {tag} {q!r}: expected={e} got={g} score={s}")
    return 0 if all(f[4] for f in failures) else 1


if __name__ == "__main__":
    sys.exit(main())
