# Phase 4: LLM Recommendation Intelligence

Implements the architecture components for Phase 4:

- Prompt Builder (system + user + candidate context template)
- LLM Client (Groq API integration)
- Response Parser (extract ranking, reasons, summary)
- Guardrails (prompt size/candidate limits + safe fallback)

## Input

- Candidate list JSON from Phase 3 (`phase3_candidate_retrieval/data/candidates.json`)

## Output

- Ranked recommendations JSON (default: `phase4_llm_recommendation/data/recommendations.json`)

## Setup

```powershell
Set-Location c:\Projects\Milestone1
& "$env:LocalAppData\Programs\Python\Python312\python.exe" -m pip install -r phase4_llm_recommendation\requirements.txt
setx GROQ_API_KEY "your-groq-api-key"
```

Restart terminal after `setx` so env var is available.

## Run

```powershell
Set-Location c:\Projects\Milestone1
& "$env:LocalAppData\Programs\Python\Python312\python.exe" -m phase4_llm_recommendation.pipeline `
  --in phase3_candidate_retrieval\data\candidates.json `
  --out phase4_llm_recommendation\data\recommendations.json `
  --model llama-3.3-70b-versatile `
  --top-n 5
```

If Groq fails or `GROQ_API_KEY` is missing, pipeline returns deterministic fallback recommendations.

