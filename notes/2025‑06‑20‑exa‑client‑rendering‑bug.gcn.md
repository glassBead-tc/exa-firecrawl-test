---
title: "Exa’s blind spot → client‑side‑rendered docs & GitHub blob URLs"
context: ["docs‑crawling", "Exa", "Firecrawl", "github‑raw"]
author: glassBead
status: draft
---

> **insight‑blast**  
> exa fails whenever the page’s real content is delivered after first paint—most visibly on github **blob** links and next‑js/docusaurus shells.

## What i saw
- byte‑size test disproved the previous “32 kB cutoff” guess: failing pages weigh **200 kB+** (git‑blob html) while their **raw markdown is tiny (≈1.7 kB)**.  
- exa grabs `github.com/.../blob/.../file.md` instead of `raw.githubusercontent.com/.../file.md`, so it screenshots a chrome‑rendered ui wrapper with zero markdown.  
- on formik (next.js) docs exa captures only the hydration shell (`<script defer src="/_next/static/...">` etc.) and times out before js finishes.  
- tanstack works because its ssr pushes enough html **before** hydration, so exa’s snapshot is already rich.  
- verdict stats unchanged: firecrawl still wins **62 %**, exa **20 %**, but root cause now pinned to “post‑paint content”.

## Why it matters
until exa rewrites blob urls and/or waits for client hydration, it will under‑index the exact docs ecosystems (github, next.js, docusaurus) that power > 70 % of modern open‑source projects. that blocks dev teams from relying on exa as a one‑stop crawler and keeps firecrawl as the default choice.

## Next up
- [ ] **exa core** – auto‑rewrite `github.com/.../blob/*.md` → `raw.githubusercontent.com/.../*.md` (due 07/05)  
- [ ] **exa core** – add `--wait-for-selector "#readme,.markdown-body"` cli flag (due 07/05)  
- [ ] **i** – assemble repro zip (blob vs raw, formik with/without js, csv of pass/fail urls) and open issue “client‑render bug” (due 06/22)  
- [ ] **alex** – draft playbook for framework‑specific waits (docusaurus, gatsby, next.js) (due 07/02)

---

### appendix
<details>
<summary>evidence snapshot</summary>

```plaintext
FILE‑SIZE TEST
──────────────
github blob useDebounce.md        207 392 bytes   (empty capture)
github RAW  useDebounce.md          1 711 bytes   (would succeed)

formik api (next.js shell)        259 801 bytes   exa empty
tanstack table (ssr)              208 100 bytes   exa ok

ROOT‑CAUSE TRACE
- blob html contains `.js‑blob‑wrapper` + ajax call to fetch raw markdown
- exa snapshot taken before ajax completes → no content
- exa timeout triggers at default 2 s after DOMContentLoaded
</details>
