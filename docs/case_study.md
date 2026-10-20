# Building a FAQ bot that knows when to say "I don't know"

I wanted to build a support-style question-answering bot, but I decided early that the interesting part would not be the matching. It would be measuring how and when the bot is wrong. So I wrote the evaluation suite before I trusted anything.

## What I built

A retrieval bot over 15 FAQ entries, using a BM25 ranker I wrote from scratch with only Python's standard library. A user's question is tokenized, scored against every FAQ, and the best entry is returned. An evaluation script runs 25 labelled queries and reports two numbers: accuracy on questions the bot should answer, and refusal rate on questions it should not.

## What failed

My first version simply returned the highest-scoring FAQ. It scored 12 of 15 on in-scope questions, which looked fine, and 0 of 7 on out-of-scope ones. Asking "tell me a joke" returned the password-reset instructions with a score of exactly zero. The bot had no concept of "no good match". It always answered, because sorting a list of zeros still produces a first element.

The in-scope misses taught me something too. "download invoice pdf" returned the certificate FAQ instead of the invoice one. My first guess was a ranking problem, but printing the tokens showed the real cause: my stemmer stripped "es" before "s", so "invoices" in the FAQ became "invoic" while "invoice" in the query stayed "invoice". They never matched, and the word "pdf" alone pulled in the wrong entry. A two-line suffix rule had silently damaged retrieval.

## What I changed

First, I added a score threshold with a fallback message. My initial value of 2.5 was a guess, and it immediately rejected a valid query scoring 2.33, so I swept the actual score distribution instead. Out-of-scope queries all scored 0.0, giving a wide gap, and I set the cutoff at 1.5. Second, I fixed the stemmer to strip only a trailing "s". Third, I added a small synonym map so "2FA", "money back" and "stop my subscription" reach the right entries.

Results moved to 15 of 15 in-scope and 7 of 7 out-of-scope. Then I made the test fairer by adding three harder negatives that share vocabulary with real FAQs, such as "how do I cancel my pizza order". Refusal dropped to 7 of 10. I kept those failures in the suite, tagged as known limitations, rather than deleting them.

## What I learned

Accuracy on a friendly test set is a weak signal; the useful tests are the ones designed to break your system. Debugging by printing intermediate values (tokens, scores) found the stemmer bug in minutes, where guessing at ranking parameters would not have. And a threshold chosen from measured data beats one chosen by intuition, though I tuned mine on the same set I evaluate on, so it is probably optimistic. The next step is a semantic reranker, since keyword overlap alone cannot tell that a pizza order is not a subscription.
