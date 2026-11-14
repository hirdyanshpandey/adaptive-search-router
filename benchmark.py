"""Compare route cost and fixture quality. No external model is invoked."""
from datetime import date
import json
from math import ceil
from pathlib import Path
from time import perf_counter_ns

from router import answer

AS_OF = date(2026, 11, 15)
CASES = (
    ("Sampletown PIN code", ("123456",), {"pin"}),
    ("Northbridge library hours", ("9 am",), {"hours"}),
    ("When does Northbridge Library open?", ("9 am",), {"hours"}),
    ("Postal code of Sampletown please", ("123456",), {"pin"}),
    ("Compare Atlas vs Nova on battery", ("10 hours", "7 hours"), {"atlas", "nova"}),
    ("Compare Nova and Atlas RAM", ("32 GB", "16 GB"), {"atlas", "nova"}),
    ("Harbor bus fare", ("40 credits",), {"bus"}),
    ("Harbor bus fare today", ("40 credits",), {"bus"}),
    ("What cloud region runs Ledger?", ("Metro",), {"cloud"}),
    ("Riverside Museum ticket price", ("18 credits",), {"museum"}),
    ("Current Riverside Museum ticket price", (), set()),
    ("Today's space launch weather", (), set()),
    ("Compare Atlas versus an unknown model", (), set()),
    ("What battery life does Nova have?", ("7 hours",), {"nova"}),
)
UNIT_COST_USD = 0.002  # Arbitrary scenario input, not a vendor price.


def correct(result, substrings, sources):
    return set(result.sources) == sources and all(s in result.answer for s in substrings)


def run(cases=CASES, repeats=300):
    report = {"scenario_generation_cost_usd": UNIT_COST_USD, "repeats": repeats, "modes": {}}
    for adaptive in (False, True):
        results = [answer(q, adaptive=adaptive, as_of=AS_OF) for q, *_ in cases]
        durations = []
        for _ in range(repeats):
            for q, *_ in cases:
                start = perf_counter_ns()
                answer(q, adaptive=adaptive, as_of=AS_OF)
                durations.append((perf_counter_ns() - start) / 1000)
        durations.sort()
        checks = [correct(result, words, refs) for result, (_, words, refs) in zip(results, cases)]
        units = sum(result.generation_units for result in results)
        report["modes"]["adaptive" if adaptive else "always_generate"] = {
            "correct": sum(checks), "total": len(cases), "generation_units": units,
            "scenario_cost_per_1000_usd": round(1000 * UNIT_COST_USD * units / len(cases), 4),
            "local_p95_microseconds": round(durations[ceil(len(durations) * 0.95) - 1], 2),
            "cases": [{"query": case[0], "route": result.route, "correct": passed}
                      for case, result, passed in zip(cases, results, checks)],
        }
    return report


if __name__ == "__main__":
    report = json.dumps(run(), indent=2) + "\n"
    Path("benchmark-results.json").write_text(report)
    print(report, end="")
