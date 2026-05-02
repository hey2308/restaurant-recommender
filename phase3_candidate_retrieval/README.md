# Phase 3: Candidate Retrieval and Filtering

Implements the architecture components for Phase 3:

- Filter Engine (hard filters: location, budget, cuisine, minimum rating)
- Scoring Helper (optional weighted score before LLM)
- Top-N Selector (shortlist candidates for prompt context)

## Input

- Structured restaurant data from `phase1_data_foundation/data/restaurants.db`
- Validated user profile from Phase 2 (`location`, `budget`, `cuisine`, `min_rating`, `optional_tags`)

## Output

- Prompt-ready candidate shortlist JSON (default: `phase3_candidate_retrieval/data/candidates.json`)

## Run

```powershell
Set-Location c:\Projects\Milestone1
& "$env:LocalAppData\Programs\Python\Python312\python.exe" -m phase3_candidate_retrieval.pipeline `
  --location Delhi `
  --budget medium `
  --cuisine Chinese `
  --min-rating 3.8 `
  --optional-tags "quick service,family-friendly" `
  --top-n 20
```
