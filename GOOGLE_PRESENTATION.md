# When should AI Search generate an answer?

Independent engineering prototype by Hirdyansh Pandey

## 1. Why this matters to Google

Alphabet reported Q3 2026 Search and related advertising revenue of $63.3B, up 12% year over year. It reported $51.4B in company-wide capital expenditure, with most going to technical infrastructure supporting AI investment. These disclosures motivate a testable design question. When is generation useful enough to justify invoking it? The disclosures do not establish Google's internal query cost or routing architecture.

[Alphabet Q3 earnings transcript](https://abc.xyz/investor/events/event-details/2026/2026-Q3-Earnings-Call-2026-Ujou16CTw9/default.aspx) · [SEC earnings exhibit](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm)

## 2. What I built

A FastAPI prototype selects among exact cache, evidence retrieval, synthesis and abstention. It accepts a freshness-sensitive query only when recent evidence matches. Outcome and route are visible in each API response.

## 3. Live walkthrough

Show an exact fact hit, a fresh-source query, a two-source comparison, and an abstention on stale evidence. Use the four examples in the README. Then run `python benchmark.py` and open its per-query results.

## 4. Offline results

| Metric | Always-generate baseline | Adaptive routing |
| --- | ---: | ---: |
| Fixture expectations matched | 12/14 | 14/14 |
| Simulated generation calls | 14 | 2 |
| Scenario cost per 1,000 queries | $2.00 | $0.29 |
| Local routing p95, microseconds | 11.17 | 13.25 |

The router avoided 12 of 14 simulated calls, about 86%, on this fixture mix. The baseline assembles up to two documents and always records one simulated generation call. The comparison measures routing behavior under that baseline. It gives no estimate of a real model's quality, total cost, latency or Google's savings.

## 5. Proposal to validate with a search team

Run both paths in shadow mode on a held-out, privacy-reviewed query set stratified by fact lookup, comparison, freshness and ambiguity. Use the same retriever and actual model across variants. Compare correctness, citation support, abstention and time-to-first-answer by query class. Measure actual tokens and infrastructure cost. Define quality gates before the test and examine misses before deciding which routes can ship.

## 60-second pitch

I wanted to test whether every query needs generation. A lookup, a comparison and a request for today's information have different evidence requirements. My FastAPI prototype routes each differently and exposes that choice in the response. On fourteen synthetic queries it invoked the simulated generation stage twice versus fourteen times for an always-generate baseline. I'd like to validate that decision policy against real models and held-out queries, with citation support, quality and tail latency measured per query class.
