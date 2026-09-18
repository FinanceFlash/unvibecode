"""Synthetic RAG controls: Python 3.10+, standard library, no network calls.
Run: python rag_review_example.py
Export: python rag_review_example.py --ragchecker-json > ragchecker_inputs.json
Parser/OCR outputs are fixtures. SQLite queries and Python arithmetic really run.
RAGChecker input export only; no evaluator, model, PDF parser or OCR is executed.
Schema: https://github.com/amazon-science/RAGChecker
"""
import ast
import copy
import json
import hashlib
import sqlite3
import sys
import unittest
from datetime import date
from decimal import Decimal

POLICIES = [
    dict(id="policy-v3", tenant="demo", start="2025-01-01", end="2026-09-01", limit="1.00", unit="percent", page=2, score=0.99),
    dict(id="policy-v4", tenant="demo", start="2026-09-01", end=None, limit="1.50", unit="percent", page=1, score=0.85),
]
LIVE = dict(exposure="1.37", unit="percent", as_of="2026-09-18", tenant="demo")
MEMORY = dict(exposure="0.80", as_of="2026-08-15")
EDGES = [("e1", "strategy-a", "eligibility-rule"), ("e2", "eligibility-rule", "exchange-restriction")]


def parser_for(page_kind):
    """Page/region type is manually reviewed here, not automatically detected."""
    choices = {"digital": "PyMuPDF", "layout": "Docling",
               "scan": "PyMuPDF + DeepSeek OCR"}
    if page_kind not in choices:
        raise ValueError("Review unclassified page/region")
    return choices[page_kind]


def hybrid_fixture():
    """Simulated accepted parser outputs, one non-overlapping region per page.

    Real integration: extract digital text; use Docling for layout; render scans
    with PyMuPDF and invoke DeepSeek OCR separately. Validate before indexing.
    A whole-file hash and batch/checkpoint manifest belong at document level;
    the chunk hash below supports per-chunk change detection only.
    """
    pages = [("digital", "Strategy A exposure limit is 1.50%."),
             ("layout", "Strategy A depends on eligibility-rule."),
             ("scan", "Eligibility-rule is restricted by exchange-restriction.")]
    return [dict(document_id="policy", version_id="policy-v4",
                 chunk_id=f"policy-v4:p{i}", source_uri="fixture://policy-v4",
                 page_start=i, page_end=i, section_path=f"Rules/{i}",
                 parent_section_id="rules", tenant="demo", entity_ids=["strategy-a"],
                 effective_from="2026-09-01", effective_to=None,
                 parser=parser_for(kind), parser_version="fixture-only",
                 extraction_status="reviewed-fixture", language="en",
                 content_type="text", text=text,
                 chunk_hash=hashlib.sha256(text.encode()).hexdigest())
            for i, (kind, text) in enumerate(pages, 1)]


def exact_chunk(chunks, chunk_id, tenant, when):
    """Metadata-scoped exact retrieval; tenant must come from trusted auth."""
    day = date.fromisoformat(when)
    matches = [c for c in chunks if c["chunk_id"] == chunk_id
               and c["tenant"] == tenant
               and c["extraction_status"] == "reviewed-fixture"
               and date.fromisoformat(c["effective_from"]) <= day
               and (c["effective_to"] is None or day < date.fromisoformat(c["effective_to"]))]
    if len(matches) != 1:
        raise ValueError("Missing or conflicting authorized source span")
    return matches[0]


def db_snapshot(tenant, entity, when):
    """Real parameterized query against a synthetic in-memory SQLite database.

    Production must derive tenant from authenticated context and enforce its
    own authorization/freshness policies; this is not a live trading connector.
    """
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE exposure (tenant TEXT, entity TEXT, exposure TEXT, unit TEXT, as_of TEXT)")
        con.execute("INSERT INTO exposure VALUES (?, ?, ?, ?, ?)",
                    ("demo", "strategy-a", "1.37", "percent", "2026-09-18"))
        rows = con.execute("SELECT exposure, unit, as_of, tenant FROM exposure WHERE tenant=? AND entity=? AND as_of=?",
                           (tenant, entity, when)).fetchall()
        if len(rows) != 1:
            raise ValueError("Missing or conflicting DB snapshot")
        return dict(zip(("exposure", "unit", "as_of", "tenant"), rows[0]))
    finally:
        con.close()


def linked_evidence(chunks, edges=EDGES):
    """Tiny graph with explicit edge-to-source provenance, not graph extraction."""
    sources = {"e1": "policy-v4:p2", "e2": "policy-v4:p3"}
    return [dict(edge_id=eid, evidence=exact_chunk(chunks, sources[eid], "demo", "2026-09-18"))
            for eid in trace(edges, "strategy-a", "exchange-restriction")]


def demonstration():
    chunks = hybrid_fixture()
    span = exact_chunk(chunks, "policy-v4:p1", "demo", "2026-09-18")
    snapshot = db_snapshot("demo", "strategy-a", "2026-09-18")
    answer = headroom(POLICIES, snapshot, "demo", "2026-09-18")
    response = (f'Strategy A exposure is {answer["exposure_percent"]}%, its limit is '
                f'{answer["limit_percent"]}%, and headroom is '
                f'{answer["headroom_percentage_points"]} percentage points.')
    return dict(synthetic_demo=True, parser_routes=[c["parser"] for c in chunks],
                exact_quote=span, linked_evidence=linked_evidence(chunks),
                db_snapshot=snapshot, naive=naive_headroom(), guarded=answer,
                response=response)


def ragchecker_input():
    """Documented input shape; fixed fixture reference, no invented scores.

    This case diagnoses response grounding in selected evidence. The DB record
    is serialized as tool evidence. Arithmetic correctness is tested separately.
    """
    demo = demonstration()
    return {"results": [{"query_id": "synthetic-headroom-1",
            "query": "What is Strategy A exposure, limit and headroom on 2026-09-18?",
            "gt_answer": "Exposure is 1.37%, limit is 1.50%, and headroom is 0.13 percentage points.",
            "response": demo["response"],
            "retrieved_context": [
                {"doc_id": demo["exact_quote"]["chunk_id"], "text": demo["exact_quote"]["text"]},
                {"doc_id": "db:demo:strategy-a:2026-09-18", "text": "Strategy A exposure is 1.37% as of 2026-09-18."}]}]}


def policy_at(policies, tenant, when):
    day = date.fromisoformat(when)
    matches = [p for p in policies if p["tenant"] == tenant
               and date.fromisoformat(p["start"]) <= day
               and (p["end"] is None or day < date.fromisoformat(p["end"]))]
    if len(matches) != 1:
        raise ValueError("Missing or conflicting applicable policy")
    return matches[0]


def headroom(policies, live, tenant, when):
    policy = policy_at(policies, tenant, when)
    if not live or live.get("exposure") is None:
        raise ValueError("Missing live exposure")
    if live.get("tenant") != tenant:
        raise ValueError("Unauthorized snapshot")
    # Same-day freshness is a DEMO assumption, not adequate for live trading.
    if live.get("as_of") != when:
        raise ValueError("Stale snapshot under demo freshness rule")
    if live.get("unit") != "percent" or policy.get("unit") != "percent":
        raise ValueError("Incompatible units")
    limit, exposure = Decimal(policy["limit"]), Decimal(live["exposure"])
    if not limit.is_finite() or not exposure.is_finite() or min(limit, exposure) < 0:
        raise ValueError("Invalid finite nonnegative inputs")
    return dict(policy=policy["id"], citation=f'{policy["id"]}:page-{policy["page"]}',
                exposure_percent=str(exposure), limit_percent=str(limit),
                headroom_percentage_points=str(limit-exposure), snapshot=when)


def naive_headroom():
    policy = max(POLICIES, key=lambda p: p["score"])
    return dict(policy=policy["id"], exposure_source="old memory",
                headroom_percentage_points=str(Decimal(policy["limit"])-Decimal(MEMORY["exposure"])))


def extraction_issue(table):
    """Compare synthetic parser output with a reviewed fixture; no OCR runs."""
    if table.get("headers") != ["Segment", "FY25", "FY24"]:
        return "Missing/mismatched headers: cannot attribute values"
    if table.get("rows") != [["A", "420", "380"]]:
        return "Cell association differs from reviewed source"
    return None


def trace(edges, start, target, max_hops=3):
    """Bounded BFS on trusted synthetic edges. Edge IDs are evidence references."""
    queue, seen = [(start, [])], {start}
    while queue:
        node, path = queue.pop(0)
        if node == target:
            return path
        if len(path) >= max_hops:
            continue
        for eid, source, dest in edges:
            if source == node and dest not in seen:
                seen.add(dest)
                queue.append((dest, path + [eid]))
    raise ValueError("Incomplete linked evidence")


def symbol_ids(source, module):
    """Top-level syntax only: no call graph/import resolution."""
    return [f"{module}.{n.name}" for n in ast.parse(source).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]


def route(intent):
    """Validated intent enum: not a natural-language router."""
    plans = {
        "current_headroom": ["current_db_snapshot", "effective_policy", "decimal_calculation"],
        "policy_quote": ["effective_policy", "exact_source_span"],
        "dependency_reason": ["provenance_link_traversal"],
        "code_location": ["qualified_symbol_search"],
        "previous_discussion": ["conversation_memory"],
    }
    if intent not in plans:
        raise ValueError("Clarify ambiguous or unsupported intent")
    return plans[intent]


class RegressionFixtures(unittest.TestCase):
    def test_hybrid_routes_and_metadata(self):
        chunks = hybrid_fixture()
        self.assertEqual([c["parser"] for c in chunks], ["PyMuPDF", "Docling", "PyMuPDF + DeepSeek OCR"])
        self.assertEqual(len({c["chunk_id"] for c in chunks}), 3)
        with self.assertRaises(ValueError):
            parser_for("unknown")

    def test_exact_quote_and_filters(self):
        chunks = hybrid_fixture()
        self.assertEqual(exact_chunk(chunks, "policy-v4:p1", "demo", "2026-09-18")["text"],
                         "Strategy A exposure limit is 1.50%.")
        for tenant, when in [("other", "2026-09-18"), ("demo", "2026-08-31")]:
            with self.assertRaises(ValueError):
                exact_chunk(chunks, "policy-v4:p1", tenant, when)
        with self.assertRaises(ValueError):
            exact_chunk(chunks + [chunks[0]], "policy-v4:p1", "demo", "2026-09-18")

    def test_db_lookup_and_parameterization(self):
        self.assertEqual(db_snapshot("demo", "strategy-a", "2026-09-18"), LIVE)
        for tenant in ["other", "demo' OR 1=1 --"]:
            with self.assertRaises(ValueError):
                db_snapshot(tenant, "strategy-a", "2026-09-18")
        with self.assertRaises(ValueError):
            db_snapshot("demo", "missing", "2026-09-18")

    def test_graph_requires_source_evidence(self):
        self.assertEqual(len(linked_evidence(hybrid_fixture())), 2)
        with self.assertRaises(ValueError):
            linked_evidence(hybrid_fixture()[:2])

    def test_ragchecker_export(self):
        record = ragchecker_input()["results"][0]
        self.assertIn("0.13 percentage points", record["response"])
        self.assertEqual(len(record["retrieved_context"]), 2)
        self.assertNotIn("metrics", record)

    def test_current_answer(self):
        a = headroom(POLICIES, LIVE, "demo", "2026-09-18")
        self.assertEqual(a["policy"], "policy-v4")
        self.assertEqual(a["headroom_percentage_points"], "0.13")
        self.assertEqual(a["citation"], "policy-v4:page-1")

    def test_naive_failure(self):
        self.assertEqual(naive_headroom()["headroom_percentage_points"], "0.20")
        self.assertNotEqual(naive_headroom()["policy"], "policy-v4")

    def test_version_boundary(self):
        self.assertEqual(policy_at(POLICIES, "demo", "2026-08-31")["id"], "policy-v3")
        self.assertEqual(policy_at(POLICIES, "demo", "2026-09-01")["id"], "policy-v4")

    def test_version_conflict(self):
        p = copy.deepcopy(POLICIES)
        p[0]["end"] = None
        with self.assertRaisesRegex(ValueError, "conflicting"):
            policy_at(p, "demo", "2026-09-18")

    def test_no_policy(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            policy_at(POLICIES, "other", "2026-09-18")

    def test_missing(self):
        with self.assertRaisesRegex(ValueError, "Missing live"):
            headroom(POLICIES, {}, "demo", "2026-09-18")

    def test_stale(self):
        with self.assertRaisesRegex(ValueError, "Stale"):
            headroom(POLICIES, dict(LIVE, as_of="2026-09-17"), "demo", "2026-09-18")

    def test_tenant(self):
        with self.assertRaisesRegex(ValueError, "Unauthorized"):
            headroom(POLICIES, dict(LIVE, tenant="other"), "demo", "2026-09-18")

    def test_units(self):
        with self.assertRaisesRegex(ValueError, "units"):
            headroom(POLICIES, dict(LIVE, unit="fraction"), "demo", "2026-09-18")

    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError, "Invalid"):
            headroom(POLICIES, dict(LIVE, exposure="NaN"), "demo", "2026-09-18")

    def test_over_limit(self):
        a = headroom(POLICIES, dict(LIVE, exposure="1.60"), "demo", "2026-09-18")
        self.assertEqual(a["headroom_percentage_points"], "-0.10")

    def test_table_fixture(self):
        self.assertIsNone(extraction_issue(dict(headers=["Segment", "FY25", "FY24"], rows=[["A", "420", "380"]])))
        self.assertIsNotNone(extraction_issue(dict(headers=[], rows=[["420", "380"]])))
        self.assertIsNotNone(extraction_issue(dict(headers=["Segment", "FY25", "FY24"], rows=[["A", "380", "420"]])))

    def test_links(self):
        self.assertEqual(trace(EDGES, "strategy-a", "exchange-restriction"), ["e1", "e2"])
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            trace(EDGES[:1], "strategy-a", "exchange-restriction")

    def test_traversal_limit(self):
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            trace(EDGES, "strategy-a", "exchange-restriction", max_hops=1)

    def test_symbols(self):
        code = "def stop_loss():\n    return True\n"
        self.assertEqual(symbol_ids(code, "strategy_a"), ["strategy_a.stop_loss"])
        self.assertNotEqual(symbol_ids(code, "strategy_a"), symbol_ids(code, "strategy_b"))

    def test_route(self):
        self.assertNotIn("conversation_memory", route("current_headroom"))
        with self.assertRaisesRegex(ValueError, "Clarify"):
            route("guess")


if __name__ == "__main__":
    if sys.argv[1:] == ["--ragchecker-json"]:
        print(json.dumps(ragchecker_input(), indent=2))
        sys.exit(0)
    print(json.dumps(demonstration(), indent=2), flush=True)
    unittest.main(verbosity=2)
