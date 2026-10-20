Most "AI support bots" fail in a boring way: they always answer.

I built a small FAQ assistant to study exactly that. Version 1 returned the closest match every time. On questions it should have refused, it scored 0 out of 7. "Tell me a joke" got the password-reset instructions.

What I did about it:
- Wrote an evaluation suite first (accuracy on in-scope questions, refusal rate on out-of-scope ones)
- Debugged by printing tokens and scores, which found a stemmer bug ("invoices" became "invoic" and never matched "invoice")
- Chose a rejection threshold from the measured score distribution, not a guess
- Added harder test cases on purpose. Refusal fell from 100% to 70%, and I kept those failures visible instead of hiding them

The hardest challenge: keyword search cannot tell that "cancel my pizza order" is not "cancel my subscription". Fixing that properly needs semantic matching, and I have documented it as the next step.

Repo (README, architecture diagram, 5 design decisions, case study): <GITHUB LINK>
5-minute demo: <LOOM LINK>

#Python #AI #SoftwareEngineering #Portfolio
(Attach docs/architecture.png to the post)
