---
title: "Exa's blind spot → client‑side‑rendered docs & GitHub blob URLs"
context: ["docs‑crawling", "Exa", "Firecrawl", "github‑raw"]
author: glassBead
status: draft
---

> **insight‑blast**  
> exa fails whenever the page's real content is delivered after first paint—most visibly on github **blob** links and next‑js/docusaurus shells.

## What i saw
- byte‑size test disproved the previous "32 kB cutoff" guess: failing pages weigh **200 kB+** (git‑blob html) while their **raw markdown is tiny (≈1.7 kB)**.  
- exa grabs `github.com/.../blob/.../file.md` instead of `raw.githubusercontent.com/.../file.md`, so it screenshots a chrome‑rendered ui wrapper with zero markdown.  
- on formik (next.js) docs exa captures only the hydration shell (`<script defer src="/_next/static/...">` etc.) and times out before js finishes.  
- tanstack works because its ssr pushes enough html **before** hydration, so exa's snapshot is already rich.  
- verdict stats unchanged: firecrawl still wins **62 %**, exa **20 %**, but root cause now pinned to "post‑paint content".

## Why it matters
This issue affects crawling effectiveness on widely-used documentation platforms including GitHub, Next.js, and Docusaurus sites. These platforms represent a significant portion of modern open-source project documentation, making improved handling important for comprehensive web crawling coverage.

## Areas for improvement
- GitHub URL handling for markdown files
- Client-side rendering support and timing
- Framework-specific content detection
- Reproduction case documentation

---

### appendix
<details>
<summary>evidence snapshot</summary>

**File Size Analysis:**
- GitHub blob useDebounce.md: 207,392 bytes (empty capture)
- GitHub RAW useDebounce.md: 1,711 bytes (would succeed)
- Formik API (Next.js shell): 259,801 bytes (exa empty)
- TanStack table (SSR): 208,100 bytes (exa success)

**Root Cause:**
- Blob HTML contains `.js-blob-wrapper` + AJAX call to fetch raw markdown
- Exa snapshot taken before AJAX completes → no content
- Exa timeout triggers at default 2s after DOMContentLoaded
</details>