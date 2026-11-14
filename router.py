"""Select the cheapest suitable answer path for a small evidence catalog."""
from dataclasses import asdict, dataclass
from datetime import date, timedelta
import re

from corpus import CACHE, DOCUMENTS, STOP_WORDS

MAX_AGE = timedelta(days=7)
COMPARISON = re.compile(r"\b(compare|versus|vs|trade-offs?)\b", re.I)
LIVE = re.compile(r"\b(today|current|latest|right now)\b", re.I)


@dataclass(frozen=True)
class Answer:
    route: str
    answer: str
    sources: list[str]
    generation_units: int

    def payload(self):
        return asdict(self)


def normalize(query):
    return " ".join(re.findall(r"[a-z0-9]+", query.lower()))


def retrieve(query, as_of):
    terms = set(normalize(query).split()) - STOP_WORDS
    ranked = []
    for doc in DOCUMENTS:
        if doc.observed > as_of or (LIVE.search(query) and as_of - doc.observed > MAX_AGE):
            continue
        matched = terms & doc.keywords
        if matched:
            ranked.append((len(matched), doc))
    return [doc for _, doc in sorted(ranked, key=lambda pair: -pair[0])[:2]]


def synthesize(query, documents):
    """Offline stand-in: compose evidence without an external model call."""
    if not documents:
        return Answer("synthesis", "No matching evidence in this catalog.", [], 1)
    return Answer(
        "synthesis",
        " ".join(doc.fact for doc in documents),
        [doc.id for doc in documents],
        1,
    )


def answer(query, *, adaptive=True, as_of=None):
    as_of = as_of or date.today()
    if not adaptive:
        return synthesize(query, retrieve(query, as_of))
    if not LIVE.search(query) and not COMPARISON.search(query):
        cached = CACHE.get(normalize(query))
        if cached and cached.observed <= as_of:
            return Answer("cache", cached.fact, [cached.id], 0)
    documents = retrieve(query, as_of)
    if not documents:
        return Answer("abstain", "No matching evidence in this catalog.", [], 0)
    if COMPARISON.search(query):
        if len(documents) < 2:
            return Answer("abstain", "Not enough evidence to compare the options.", [], 0)
        return synthesize(query, documents)
    top = documents[0]
    return Answer("retrieval", top.fact, [top.id], 0)
