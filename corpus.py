"""Synthetic, dated evidence fixtures. Names and prices are illustrative."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Document:
    id: str
    keywords: frozenset[str]
    fact: str
    observed: date


def doc(id, keywords, fact, observed=date(2026, 11, 12)):
    return Document(id, frozenset(keywords.split()), fact, observed)


DOCUMENTS = (
    doc("pin", "pin postcode postal sampletown code", "Sampletown's demo postal code is 123456."),
    doc("hours", "library hours opening opens northbridge", "Northbridge Library opens at 9 am."),
    doc("atlas", "atlas laptop battery ram budget", "Atlas has 16 GB RAM and 10 hours of rated battery life."),
    doc("nova", "nova laptop battery ram budget", "Nova has 32 GB RAM and 7 hours of rated battery life."),
    doc("bus", "bus fare route harbor", "The Harbor bus fare is 40 credits."),
    doc("museum", "museum ticket price riverside", "The Riverside Museum lists tickets at 18 credits.", date(2026, 10, 1)),
    doc("cloud", "cloud region ledger latency service", "Ledger runs in the Metro cloud region."),
)

CACHE = {"sampletown pin code": DOCUMENTS[0], "northbridge library hours": DOCUMENTS[1]}

STOP_WORDS = frozenset(
    "a an the is are what of to for in how much does tell me please compare versus vs "
    "trade offs today current latest right now and with at which".split()
)
