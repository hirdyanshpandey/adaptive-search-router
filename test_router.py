from datetime import date
import unittest

from fastapi.testclient import TestClient

from app import app
from benchmark import CASES, correct
from router import answer

AS_OF = date(2026, 11, 15)


class SearchTests(unittest.TestCase):
    def test_all_adaptive_fixtures(self):
        for query, terms, sources in CASES:
            with self.subTest(query=query):
                self.assertTrue(correct(answer(query, as_of=AS_OF), terms, sources))

    def test_generation_baseline_is_charged_even_on_a_miss(self):
        result = answer("untracked destination", adaptive=False, as_of=AS_OF)
        self.assertEqual(result.generation_units, 1)
        self.assertEqual(result.sources, [])

    def test_exact_cache_and_live_bypass(self):
        self.assertEqual(answer("Sampletown PIN code", as_of=AS_OF).route, "cache")
        self.assertEqual(answer("Sampletown PIN code today", as_of=AS_OF).route, "retrieval")

    def test_stale_live_evidence_is_rejected(self):
        self.assertEqual(answer("current Harbor bus fare", as_of=date(2026, 12, 1)).route, "abstain")

    def test_api_contract(self):
        client = TestClient(app)
        response = client.post("/search", json={"query": "Compare Atlas vs Nova"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["route"], "synthesis")
        self.assertEqual(client.post("/search", json={"query": "  "}).status_code, 422)
