# Adaptive Search Router

A FastAPI reference prototype that decides when to spend a generation call. It returns an exact cache hit for known queries, retrieves a dated source for a simple fact, synthesizes a comparison from multiple sources, or abstains when evidence is missing.

## Run in five minutes

Use Python 3.10+.

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app:app
```

Open http://127.0.0.1:8000/docs and try POST /search with one of these inputs.

| Query | Expected route |
| --- | --- |
| Sampletown PIN code | Cache |
| What cloud region runs Ledger? | Retrieval |
| Compare Atlas vs Nova on battery | Synthesis |
| Current Riverside Museum ticket price | Abstain |

The response exposes the selected route, answer, synthetic source IDs, and the number of simulated generation calls. Set `"adaptive": false` to run the same request through the always-generate baseline. The service evaluates freshness against today's date. The benchmark deliberately pins the date so every run uses the same evidence.

```sh
python -m unittest -v
python benchmark.py
```

The benchmark writes `benchmark-results.json` including per-query decisions. Quality uses expected evidence IDs and text assertions on 14 hand-authored synthetic fixtures. The generation step is a deterministic stub. Its local timing excludes model calls, real indexing, network and API overhead. The scenario cost assumes USD 0.002 per simulated generation call and excludes retrieval, caching, and hosting costs.

The 7-day freshness rule and English keyword matching are demo policies. Real deployments need source-specific freshness, semantic relevance, calibrated abstention and a production-quality synthesis stage. The fixture suite is a smoke test without a held-out set.
