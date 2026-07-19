import hashlib
import json
import subprocess
from pathlib import Path

APP = Path('/app/environment/app')
OUT = Path('/app/output/migration_observations.json')
RUNNER = ['/app/environment/mig_exec', '--write', '/app/output/migration_observations.json']

EVIDENCE_KEYS = frozenset({'active', 'bundle', 'summary', 'source'})
CROSSED_DECEPTIVE = frozenset({'echo', 'fox'})


def _anchor() -> int:
    return int(json.loads((APP / 'fixtures/ledger_seed.json').read_text(encoding='utf-8'))['anchor'])


def _load_fixture_rows() -> list[dict]:
    rows = []
    for line in (APP / 'fixtures/packs.tsv').read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        parts = line.split('|')
        rows.append(
            {
                'run': parts[0],
                'mode': parts[1],
                'name': parts[2],
                'generation': int(parts[3]),
                'active': parts[4],
                'pack': parts[5],
                'summary': parts[6],
                'chain': parts[7],
                'file': parts[8],
                'span': parts[9],
                'removed': parts[9] == 'removed',
            }
        )
    return rows


def _apply_wal(rows: list[dict]) -> list[dict]:
    payload = json.loads((APP / 'fixtures/wal.json').read_text(encoding='utf-8'))
    out = [dict(row) for row in rows]
    for entry in sorted(payload['entries'], key=lambda item: item['seq']):
        for row in out:
            if row['run'] != entry['run'] or row['name'] != entry['name']:
                continue
            if entry['op'] == 'bump':
                if 'generation' in entry:
                    row['generation'] = entry['generation']
                if entry.get('active'):
                    row['active'] = entry['active']
                row['source'] = 'log'
            elif entry['op'] == 'tombstone':
                row['removed'] = True
                row['span'] = 'removed'
    return out


def _apply_tombstones(rows: list[dict]) -> list[dict]:
    payload = json.loads((APP / 'fixtures/tombstones.json').read_text(encoding='utf-8'))
    out = [dict(row) for row in rows]
    for mark in payload['marks']:
        for row in out:
            if row['run'] == mark['run'] and row['name'] == mark['name']:
                row['removed'] = True
                row['span'] = 'removed'
    return out


def _owner_for(row: dict) -> str:
    if row['span'] == 'crossed' and row['active']:
        return row['active']
    if row.get('source') == 'log' and row['active']:
        return row['active']
    if row['pack']:
        return row['pack']
    if row['summary']:
        return row['summary']
    return row['active'] or 'unknown'


def _lineage_for(row: dict, owner: str) -> str:
    return f"{row['chain']}:{owner}"


def _canonical_records() -> list[dict]:
    rows = _apply_tombstones(_apply_wal(_load_fixture_rows()))
    kept: dict[tuple[str, str], dict] = {}
    for row in rows:
        if row['removed'] or row['span'] == 'removed':
            continue
        key = (row['run'], row['name'])
        prior = kept.get(key)
        if prior is None or row['generation'] > prior['generation']:
            kept[key] = row
    records = []
    anchor = _anchor()
    for row in sorted(kept.values(), key=lambda r: (r['run'], r['name'])):
        owner = _owner_for(row)
        lineage = _lineage_for(row, owner)
        records.append(
            {
                'run_id': row['run'],
                'name': row['name'],
                'generation': row['generation'],
                'owner': owner,
                'lineage': lineage,
                'boundary': row['span'],
                'anchor': anchor,
            }
        )
    return records


def _expected_stable_digest() -> str:
    segments = [
        f"{r['run_id']}|{r['name']}|{r['generation']}|{r['owner']}|{r['lineage']}|{r['boundary']}|anchor:{r['anchor']}"
        for r in _canonical_records()
    ]
    return hashlib.sha256('\n'.join(segments).encode('utf-8')).hexdigest()


def _stable_hex_from_report(data: dict) -> str:
    anchor = _anchor()
    segments = []
    for run in sorted(data['runs'], key=lambda item: item['run_id']):
        for record in sorted(run['records'], key=lambda item: item['name']):
            segments.append(
                f"{run['run_id']}|{record['name']}|{record['generation']}|{record['owner']}|{record['lineage']}|{record['boundary']}|anchor:{anchor}"
            )
    return hashlib.sha256('\n'.join(segments).encode('utf-8')).hexdigest()


def build_report() -> dict:
    OUT.unlink(missing_ok=True)
    subprocess.run(RUNNER, check=True, cwd='/app')
    assert OUT.exists(), 'runner should create the observation report at the documented path'
    return json.loads(OUT.read_text(encoding='utf-8'))


def all_records(data: dict) -> list[dict]:
    return [record for run in data['runs'] for record in run['records']]


def by_run(data: dict) -> dict[str, dict]:
    return {run['run_id']: run for run in data['runs']}


def artifact_map(data: dict) -> dict[tuple[str, str], dict]:
    return {(item['run_id'], item['name']): item for item in data['artifacts']}


def assert_evidence_complete(record: dict) -> None:
    evidence = record['evidence']
    assert isinstance(evidence, dict)
    assert set(evidence.keys()) >= EVIDENCE_KEYS
    for key in EVIDENCE_KEYS:
        assert isinstance(evidence[key], str)


def test_h01_driver_emits_full_observation_trace() -> None:
    """Public runner produces runs, artifacts, fingerprints, and populated records."""
    data = build_report()
    assert set(data) == {'runs', 'artifacts', 'fingerprints'}
    assert data['fingerprints']['stable_digest']
    assert data['fingerprints']['session_span_id']
    assert data['fingerprints']['stable_digest'] != 'deadbeef'
    assert data['fingerprints']['session_span_id'] != '00000000'
    assert {run['mode'] for run in data['runs']} >= {'clean', 'replay', 'cleanup', 'rerun'}
    assert len(all_records(data)) >= 10
    for record in all_records(data):
        assert_evidence_complete(record)


def test_h02_wal_bump_advances_yankee_on_repeat() -> None:
    """Write-log bump applied in seq order upgrades yankee on the repeat run."""
    data = build_report()
    repeat = by_run(data)['repeat']
    yankee = next(r for r in repeat['records'] if r['name'] == 'yankee')
    assert yankee['generation'] == 2
    assert yankee['owner'] == 'owner-y2'
    assert yankee['boundary'] == 'local'
    assert yankee['evidence']['active'] == 'owner-y2'


def test_h03_tombstoned_delta_never_resurrected() -> None:
    """Tombstone marks and log tombstones keep delta out of records and artifacts."""
    data = build_report()
    names = {record['name'] for record in all_records(data)}
    artifact_names = {item['name'] for item in data['artifacts']}
    assert 'delta' not in names
    assert 'delta' not in artifact_names
    assert all(record['boundary'] != 'removed' for record in all_records(data))


def test_h04_crossed_deceptive_rows_follow_active_authority() -> None:
    """Crossed rows whose summary text lags still bind owner to active authority."""
    data = build_report()
    for name in sorted(CROSSED_DECEPTIVE):
        crossed = [
            r
            for r in all_records(data)
            if r['name'] == name and r['boundary'] == 'crossed'
        ]
        assert crossed, f'expected crossed rows for {name}'
        for record in crossed:
            assert record['evidence']['active'] == record['owner']
            assert record['owner'].startswith(record['evidence']['active'][:6])
            assert record['owner'] != record['evidence']['summary']
            assert record['lineage'].endswith(':' + record['owner'])


def test_h05_artifacts_track_record_owner_across_runs() -> None:
    """Artifact sidecars mirror record owner, lineage, and generation for every pair."""
    data = build_report()
    artifacts = artifact_map(data)
    for run in data['runs']:
        for record in run['records']:
            item = artifacts[(run['run_id'], record['name'])]
            assert item['generation'] == record['generation']
            assert item['owner'] == record['owner']
            assert item['lineage'] == record['lineage']
            assert item['path'] == f"local/{record['artifact']}"


def test_h06_stable_digest_matches_canonical_projection() -> None:
    """Stable digest matches the documented SHA-256 projection over canonical rows."""
    data = build_report()
    expected = _expected_stable_digest()
    assert data['fingerprints']['stable_digest'] == expected
    assert data['fingerprints']['stable_digest'] == _stable_hex_from_report(data)


def test_h07_triple_regeneration_preserves_stable_digest() -> None:
    """Three consecutive regenerations keep an identical stable digest."""
    first = build_report()
    second = build_report()
    third = build_report()
    digest = first['fingerprints']['stable_digest']
    assert second['fingerprints']['stable_digest'] == digest
    assert third['fingerprints']['stable_digest'] == digest
    assert digest == _expected_stable_digest()


def test_h08_session_span_advances_while_digest_stable() -> None:
    """Session span id changes across writes while stable digest stays fixed."""
    first = build_report()
    second = build_report()
    assert first['fingerprints']['stable_digest'] == second['fingerprints']['stable_digest']
    assert first['fingerprints']['session_span_id'] != second['fingerprints']['session_span_id']
    assert len(first['fingerprints']['session_span_id']) == 8
    assert len(second['fingerprints']['session_span_id']) == 8


def test_h09_control_rows_stable_between_clean_and_repeat() -> None:
    """Control rows listed in control_sets stay identical between clean and repeat."""
    controls = json.loads((APP / 'fixtures/control_sets.json').read_text(encoding='utf-8'))['controls']
    data = build_report()
    runs = by_run(data)
    for ctrl in controls:
        clean = next(r for r in runs['clean']['records'] if r['name'] == ctrl['name'])
        repeat = next(r for r in runs['repeat']['records'] if r['name'] == ctrl['name'])
        assert clean['owner'] == repeat['owner']
        assert clean['lineage'] == repeat['lineage']
        assert clean['boundary'] == 'local'


def test_h10_per_run_generation_keeps_latest_fixture_row() -> None:
    """Each run/name pair reflects the highest generation after log and tombstone replay."""
    data = build_report()
    expected = {(r['run_id'], r['name']): r['generation'] for r in _canonical_records()}
    for run in data['runs']:
        for record in run['records']:
            key = (run['run_id'], record['name'])
            assert record['generation'] == expected[key]


def test_h11_crossed_evidence_source_names_active_pick() -> None:
    """Deceptive crossed rows whose owner came from active authority report source active."""
    data = build_report()
    for name in sorted(CROSSED_DECEPTIVE):
        for record in all_records(data):
            if record['name'] != name or record['boundary'] != 'crossed':
                continue
            if record['owner'] == record['evidence']['active']:
                assert record['evidence']['source'] == 'active'


def test_h12_static_placeholder_report_is_replaced() -> None:
    """Driver replaces a seeded empty placeholder with a populated regenerated report."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('{"runs": [], "artifacts": [], "fingerprints": {"stable_digest": "00", "session_span_id": "00"}}')
    subprocess.run(RUNNER, check=True, cwd='/app')
    data = json.loads(OUT.read_text(encoding='utf-8'))
    assert all_records(data)
    assert data['fingerprints']['stable_digest'] == _expected_stable_digest()
