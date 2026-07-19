import json
import shutil
import subprocess
from pathlib import Path

APP = Path("/app")
OUT = APP / "output" / "ledger_compaction_report.json"
LABELS = ["clean", "restart", "rollback", "idempotent"]
ARTIFACT_PATHS = [
    "/app/environment/f6/r1.json",
    "/app/environment/f6/r2.json",
    "/app/environment/g8/r1.json",
    "/app/environment/g8/r2.json",
]
EXPECTED = {
    "A100": {"generation": 1, "value": 10, "source": "anchor"},
    "B200": {"generation": 2, "value": 20, "source": "anchor"},
    "C300": {"generation": 3, "value": 30, "source": "anchor"},
}
FORBIDDEN = {"D400"}


def _run_report():
    shutil.rmtree(APP / "output", ignore_errors=True)
    result = subprocess.run(
        ["go", "run", "/app/environment/e5", "--write-report", "/app/output/ledger_compaction_report.json"],
        cwd=APP / "environment",
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert OUT.exists(), "command did not regenerate the report"
    return json.loads(OUT.read_text())


def _by_label(report):
    return {run["label"]: run for run in report["runs"]}


def _records(run):
    return {row["id"]: row for row in run["records"]}


def _input_row_count(path: str) -> int:
    data = json.loads(Path(path).read_text())
    return len(data.get("rows", []))


def _digest_for(records):
    parts = []
    for key in sorted(records):
        row = records[key]
        parts.append(f"{key}:{row['generation']}:{row['value']}:{row['source']}")
    return "|".join(parts)


def _assert_expected_records(run):
    records = _records(run)
    assert set(records) == set(EXPECTED)
    for key, want in EXPECTED.items():
        got = records[key]
        assert got["generation"] == want["generation"]
        assert got["value"] == want["value"]
        assert got["source"] == want["source"]
    assert len(set(records) & FORBIDDEN) == 0
    return records


def _assert_provenance(run):
    records = _records(run)
    provenance = {row["id"]: row for row in run["provenance"]}
    assert set(provenance) == set(records)
    for key, record in records.items():
        row = provenance[key]
        assert row["generation"] == record["generation"]
        assert row["value"] == record["value"]
        assert row["source"] == record["source"]


def _assert_artifact_row_counts(report):
    by_path = {item["path"]: item for item in report["artifacts"]}
    assert set(by_path) == set(ARTIFACT_PATHS)
    for path in ARTIFACT_PATHS:
        assert by_path[path]["row_count"] == _input_row_count(path)


def test_a1():
    """The normal command regenerates a complete evidence report."""
    report = _run_report()
    assert report["schema_version"] == 1
    assert report["command"] == "go run /app/environment/e5 --write-report /app/output/ledger_compaction_report.json"
    assert isinstance(report["runs"], list)
    assert all(isinstance(run, dict) and "label" in run for run in report["runs"])
    assert sorted(_by_label(report)) == sorted(LABELS)
    assert [item["path"] for item in report["artifacts"]] == ARTIFACT_PATHS
    _assert_artifact_row_counts(report)


def test_a2():
    """Conflicting local surfaces converge to the same active rows."""
    report = _run_report()
    for run in report["runs"]:
        records = _assert_expected_records(run)
        _assert_provenance(run)
        assert run["state_digest"] == _digest_for(records)


def test_a3():
    """The restart workflow keeps the clean state observations stable."""
    runs = _by_label(_run_report())
    clean_records = _assert_expected_records(runs["clean"])
    restart_records = _assert_expected_records(runs["restart"])
    assert restart_records["B200"]["generation"] == EXPECTED["B200"]["generation"]
    assert runs["restart"]["state_digest"] == _digest_for(clean_records)
    transition = runs["restart"]["transitions"][0]
    assert transition["label"] == "restart"
    assert transition["record_count"] == len(EXPECTED)
    assert transition["max_generation"] == max(row["generation"] for row in EXPECTED.values())


def test_a4():
    """Rollback preserves active rows without carrying retired input rows."""
    runs = _by_label(_run_report())
    rollback_records = _assert_expected_records(runs["rollback"])
    assert "D400" not in rollback_records
    assert runs["rollback"]["state_digest"] == _digest_for(rollback_records)
    assert runs["rollback"]["transitions"][0]["max_generation"] == max(row["generation"] for row in EXPECTED.values())


def test_a5():
    """Repeated invocations produce stable records and digests."""
    first = _run_report()
    second = _run_report()
    first_runs = _by_label(first)
    second_runs = _by_label(second)
    for label in LABELS:
        first_records = _assert_expected_records(first_runs[label])
        second_records = _assert_expected_records(second_runs[label])
        assert first_records == second_records
        _assert_provenance(first_runs[label])
        _assert_provenance(second_runs[label])
        assert first_runs[label]["provenance"] == second_runs[label]["provenance"]
        assert first_runs[label]["state_digest"] == second_runs[label]["state_digest"]
    assert first_runs["idempotent"]["state_digest"] == second_runs["idempotent"]["state_digest"]
    assert first_runs["clean"]["state_digest"] == first_runs["idempotent"]["state_digest"]


def test_a6():
    """The report contains derived observations rather than answer-key flags."""
    report = _run_report()
    text = json.dumps(report, sort_keys=True)
    for token in ["_ok", "_green", "_valid", "_passes", "stays_green"]:
        assert token not in text
    assert len(report["state_transitions"]) == len(LABELS)
    for run in report["runs"]:
        assert len(run["provenance"]) == len(EXPECTED)
        assert {p["id"] for p in run["provenance"]} == set(EXPECTED)
        assert run["transitions"][0]["record_count"] == len(run["records"])


def test_a7():
    """The pipeline derives observations from bundled inputs rather than a static template."""
    path = APP / "environment" / "f6" / "r1.json"
    original_text = path.read_text()
    data = json.loads(original_text)
    row = data["rows"][0]
    original_value = row["value"]
    bumped = original_value + 1
    try:
        row["value"] = bumped
        path.write_text(json.dumps(data))
        report = _run_report()
        clean = _by_label(report)["clean"]
        records = _records(clean)
        assert records["A100"]["value"] == bumped
        provenance = {item["id"]: item for item in clean["provenance"]}
        assert provenance["A100"]["value"] == bumped
        assert clean["state_digest"] == _digest_for(records)
    finally:
        path.write_text(original_text)


def test_a8():
    """Changing the secondary history surface updates merged active rows."""
    path = APP / "environment" / "f6" / "r2.json"
    original_text = path.read_text()
    data = json.loads(original_text)
    try:
        for row in data["rows"]:
            if row["id"] == "B200":
                row["generation"] = 3
                row["value"] = 44
        path.write_text(json.dumps(data))
        report = _run_report()
        clean = _by_label(report)["clean"]
        records = _records(clean)
        assert records["B200"]["generation"] == 3
        assert records["B200"]["value"] == 44
        assert records["B200"]["source"] == "cache"
        assert clean["state_digest"] == _digest_for(records)
        assert records["B200"]["value"] != EXPECTED["B200"]["value"]
    finally:
        path.write_text(original_text)


def test_a9():
    """Changing the bundled rank table resolves same-generation ties differently."""
    path = APP / "environment" / "f6" / "r3.json"
    original_text = path.read_text()
    data = json.loads(original_text)
    try:
        data["rank"] = {"anchor": 1, "cache": 3, "audit": 2}
        path.write_text(json.dumps(data))
        report = _run_report()
        clean = _by_label(report)["clean"]
        records = _records(clean)
        assert records["A100"]["source"] == "cache"
        assert records["C300"]["source"] == "cache"
        assert clean["state_digest"] == _digest_for(records)
        assert records["A100"]["source"] != EXPECTED["A100"]["source"]
    finally:
        path.write_text(original_text)


def test_a10():
    """Restart workflow inputs change restart observations without altering the clean baseline."""
    path = APP / "environment" / "g8" / "r1.json"
    original_text = path.read_text()
    data = json.loads(original_text)
    try:
        data["rows"][0]["generation"] = 3
        data["rows"][0]["value"] = 25
        path.write_text(json.dumps(data))
        report = _run_report()
        runs = _by_label(report)
        clean_b200 = _records(runs["clean"])["B200"]
        restart_b200 = _records(runs["restart"])["B200"]
        assert clean_b200["generation"] == 2
        assert clean_b200["value"] == 20
        assert restart_b200["generation"] == 3
        assert restart_b200["value"] == 25
        assert runs["restart"]["state_digest"] == _digest_for(_records(runs["restart"]))
    finally:
        path.write_text(original_text)


def test_a11():
    """Rollback workflow inputs surface only on rollback and idempotent runs."""
    path = APP / "environment" / "g8" / "r2.json"
    original_text = path.read_text()
    data = json.loads(original_text)
    extra = {
        "id": "E500",
        "generation": 2,
        "value": 50,
        "source": "audit",
        "active": True,
    }
    extra_id = extra["id"]
    try:
        data["rows"].append(extra)
        path.write_text(json.dumps(data))
        report = _run_report()
        runs = _by_label(report)
        for run in (runs["clean"], runs["restart"]):
            assert extra_id not in _records(run)
        for run in (runs["rollback"], runs["idempotent"]):
            row = _records(run)[extra_id]
            assert row["generation"] == 2
            assert row["value"] == 50
            assert row["source"] == "audit"
            assert run["state_digest"] == _digest_for(_records(run))
    finally:
        path.write_text(original_text)
