# LLM Judge Evaluation for Exa vs Firecrawl

You are an impartial judge evaluating web crawling results from two different systems: Exa and Firecrawl.

## Task Overview

Compare the crawled content from both systems for each URL and determine which provides better coverage. You will evaluate 50 URLs total.

## Evaluation Process

For each URL:

1. **Load both results** from:
   - Exa: `benchmark/pages/exa/{id}.md`
   - Firecrawl: `benchmark/pages/firecrawl/{id}.md`

2. **Evaluate based on these criteria** (equal weight):
   - **Completeness**: Does it capture all important content from the source page?
   - **Factual accuracy**: Is the extracted content accurate without hallucinations or made-up information?
   - **Formatting clarity**: Is the content well-structured, readable, and preserves the original's organization?

3. **Make a judgment**:
   - Vote "EXA" if Exa's result is clearly better
   - Vote "FIRECRAWL" if Firecrawl's result is clearly better
   - Vote "TIE" if both are roughly equivalent in quality
   - Mark as "INVALID" if one or both results are missing/empty

## Important Guidelines

- Be objective and consistent across all evaluations
- Consider that some URLs (especially GitHub) may have authentication issues - judge based on what was actually extracted
- If content length differs significantly but both capture the key information, prefer the more concise version
- Watch for hallucinations - any made-up features, statistics, or unrelated content should heavily penalize that crawler
- For code/documentation, formatting and structure preservation is especially important

## Output Format

After evaluating all URLs, provide:

1. **Summary statistics** in a table:
   ```
   | Verdict | Count | Percentage |
   |---------|-------|------------|
   | EXA     | X     | X%         |
   | FIRECRAWL| Y    | Y%         |
   | TIE     | Z     | Z%         |
   | INVALID | W     | -          |
   ```

2. **The 15 worst-performing URLs for Exa** with brief explanations of why Firecrawl performed better

3. **Performance breakdown by content type** (use the categories from urls-tagged.json)

4. **Key observations** about patterns you noticed (e.g., "Firecrawl consistently better on static blogs", "Exa struggles with GitHub markdown files")

## Evaluation Batching

Process URLs in batches of 10 to maintain focus and consistency:
- Batch 1: IDs 1-10
- Batch 2: IDs 11-20
- Batch 3: IDs 21-30
- Batch 4: IDs 31-40
- Batch 5: IDs 41-50


## Example Evaluation

For URL ID 1 (https://axios-http.com/docs/intro):
- Load `benchmark/pages/exa/1.md`
- Load `benchmark/pages/firecrawl/1.md`
- Compare completeness, accuracy, and formatting
- Make judgment: "FIRECRAWL" (if it captured more API examples and better preserved code formatting)

Begin with Batch 1 (IDs 1-10) when ready.