# Phase 5: Presentation and Delivery

Implements the architecture components for Phase 5:

- `Response Formatter` (card/table/json structure)
- `UI Renderer` (HTML page and CLI text output)
- `Explanation View` (why this was recommended)

## Input

- Parsed LLM recommendations from Phase 4  
  (`phase4_llm_recommendation/data/recommendations.json`)

## Output

- User-facing presentation payload JSON  
  (`phase5_presentation_delivery/data/presentation.json`)
- Rendered web page  
  (`phase5_presentation_delivery/data/recommendations.html`)
- CLI-style text report  
  (`phase5_presentation_delivery/data/recommendations.txt`)

## Run

```powershell
Set-Location c:\Projects\Milestone1
& "$env:LocalAppData\Programs\Python\Python312\python.exe" -m phase5_presentation_delivery.pipeline `
  --in phase4_llm_recommendation\data\recommendations.json `
  --out-json phase5_presentation_delivery\data\presentation.json `
  --out-html phase5_presentation_delivery\data\recommendations.html `
  --out-text phase5_presentation_delivery\data\recommendations.txt
```

