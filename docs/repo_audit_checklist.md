# Repo audit checklist
- [x] Code in named directories: `src/faq_bot/`, `data/`, `eval/`, `docs/`
- [x] `.gitignore` added (caches, venvs, `.env`, editor folders)
- [x] No API keys or secrets in the code (none are needed; stdlib only, no network calls)
- [ ] Before pushing, run: `grep -rniE "api[_-]?key|secret|token|password\s*=" .` and confirm nothing real shows up (the word "password" appears only in FAQ text)
- [ ] Export diagram to `docs/architecture.png` (excalidraw.com -> open the .excalidraw file -> Export image)
- [ ] Replace `<your-username>` in README
- [ ] Push, then open the repo page on GitHub and confirm the README renders: table, code blocks, and the image
