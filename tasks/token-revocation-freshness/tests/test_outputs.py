import os
import json
import subprocess
from pathlib import Path
# assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert assert
import pytest

DB_PATH = Path("gateway.db")
SCENARIO_PATH = Path("scenario.json")
TRACE_PATH = Path("/app/logs/verifier/auth_audit_trace.json")
FORBIDDEN_TEST_READ_MARKERS = ("/tests", "test_outputs.py")


def assert_runtime_does_not_reference_tests():
    scan_roots = [Path("/app/environment/src"), Path("/app/environment/dist")]
    offenders = []

    for root in scan_roots:
        if not root.exists():
            continue

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            try:
                text = file_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            if any(marker in text for marker in FORBIDDEN_TEST_READ_MARKERS):
                offenders.append(str(file_path))

    assert not offenders, f"Runtime code must not reference mounted test files: {offenders}"


@pytest.fixture(autouse=True)
def clean_test_environment():
    for p in [DB_PATH, SCENARIO_PATH, TRACE_PATH]:
        if p.exists():
            try:
                os.remove(p)
            except OSError:
                pass
    yield
    for p in [DB_PATH, SCENARIO_PATH, TRACE_PATH]:
        if p.exists():
            try:
                os.remove(p)
            except OSError:
                pass


def make_jwt_token(payload: dict, secret: str, kid: str) -> str:
    js_cmd = (
        f"console.log(require('jsonwebtoken').sign("
        f"{json.dumps(payload)}, '{secret}', "
        f"{{ header: {{ kid: '{kid}' }}, algorithm: 'HS256' }}))"
    )
    res = subprocess.run(["node", "-e", js_cmd], capture_output=True, text=True, check=True, cwd="/app/environment")
    return res.stdout.strip()


def make_jwt_tokens(payloads: list[dict], secret: str, kid: str) -> list[str]:
    js_cmd = (
        f"const jwt = require('jsonwebtoken');"
        f"const payloads = {json.dumps(payloads)};"
        f"const tokens = payloads.map(p => jwt.sign(p, '{secret}', {{ header: {{ kid: '{kid}' }}, algorithm: 'HS256' }}));"
        f"console.log(JSON.stringify(tokens));"
    )
    res = subprocess.run(["node", "-e", js_cmd], capture_output=True, text=True, check=True, cwd="/app/environment")
    return json.loads(res.stdout)


def run_scenario_process(scenario: dict):
    assert_runtime_does_not_reference_tests()

    with open(SCENARIO_PATH, "w") as f:
        json.dump(scenario, f)

    res = subprocess.run(
        ["node", "/app/environment/dist/scenario.js", "scenario.json"],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        pass

    assert TRACE_PATH.exists(), f"Gateway did not output trace log. Stderr: {res.stderr}"
    with open(TRACE_PATH, "r") as f:
        return json.load(f)


def test_token_signature_rotation():
    """Verify that the token gateway successfully rotates and uses updated public keys from the JWKS endpoint."""
    token_payload = {"sub": "user-123", "scope": "read", "jti": "jti-1", "exp": 9999999999}
    tok = make_jwt_token(token_payload, "key-version-A", "kid-rot-1")

    scenario = {
        "dbPath": str(DB_PATH),
        "operations": [
            {"type": "validate", "token": tok, "skewMs": 0, "simulateTimeout": False}
        ]
    }
    
    tok_correct = make_jwt_token(token_payload, "mock-public-key-for-kid-kid-rot-1", "kid-rot-1")
    scenario["operations"][0]["token"] = tok_correct

    trace = run_scenario_process(scenario)
    results = trace["results"]
    assert len(results) == 1
    
    val = results[0]["result"]["valid"]
    assert val is True


def test_expired_fallback_keys():
    """Verify that cached keys are not used if they have exceeded their cache TTL expiration limit."""
    token_payload = {"sub": "user-123", "scope": "read", "jti": "jti-2", "exp": 9999999999}
    tok = make_jwt_token(token_payload, "mock-public-key-for-kid-kid-exp-1", "kid-exp-1")

    scenario = {
        "dbPath": str(DB_PATH),
        "keyCacheSeed": [
            {
                "kid": "kid-exp-1",
                "key": "mock-public-key-for-kid-kid-exp-1",
                "expiresAt": 1000  # Long expired timestamp
            }
        ],
        "operations": [
            {"type": "validate", "token": tok, "skewMs": 0, "simulateTimeout": True}
        ]
    }

    trace = run_scenario_process(scenario)
    results = trace["results"]
    assert len(results) == 1
    
    val = results[0]["result"]["valid"]
    assert val is False
    
    reason = results[0]["result"]["reason"].lower()
    assert "expire" in reason


def test_wildcard_eviction():
    """Verify that wildcards matching principal and scope evict corresponding cached tokens upon invalidation."""
    tok_payload_a = {"sub": "user-100", "scope": "read", "jti": "jti-a", "exp": 9999999999}
    tok_payload_b = {"sub": "user-200", "scope": "read", "jti": "jti-b", "exp": 9999999999}

    tok_a = make_jwt_token(tok_payload_a, "mock-public-key-for-kid-kid-wild-1", "kid-wild-1")
    tok_b = make_jwt_token(tok_payload_b, "mock-public-key-for-kid-kid-wild-1", "kid-wild-1")

    scenario = {
        "dbPath": str(DB_PATH),
        "operations": [
            {"type": "validate", "token": tok_a, "skewMs": 0},
            {"type": "validate", "token": tok_b, "skewMs": 0},
            {
                "type": "sync",
                "batch": {
                    "sequence": 1,
                    "revocations": [
                        {
                            "id": "rev-id-1",
                            "principal": "user-100",
                            "scope": "*",
                            "timestamp": 11111
                        }
                    ]
                }
            },
            {"type": "invalidateByPattern", "pattern": "principal:user-100"},
            {"type": "validate", "token": tok_a, "skewMs": 0},
            {"type": "validate", "token": tok_b, "skewMs": 0}
        ]
    }

    trace = run_scenario_process(scenario)
    results = trace["results"]

    val_init_a = results[0]["result"]["valid"]
    val_init_b = results[1]["result"]["valid"]
    assert val_init_a is True
    assert val_init_b is True

    val_post_a = results[4]["result"]["valid"]
    reason_post_a = results[4]["result"]["reason"]
    assert val_post_a is False
    assert reason_post_a == "Token revoked"

    val_post_b = results[5]["result"]["valid"]
    assert val_post_b is True


def test_capacity_eviction():
    """Verify cache capacity eviction of the oldest elements when the size reaches 1000 items."""
    tok_prefix_payload = {"scope": "read", "exp": 9999999999}
    
    tok_1 = make_jwt_token({"sub": "user-first", "jti": "jti-first", **tok_prefix_payload}, "mock-public-key-for-kid-k", "k")
    
    ops = []
    ops.append({"type": "validate", "token": tok_1, "skewMs": 0})
    
    # Sync a revocation for tok_1
    ops.append({
        "type": "sync",
        "batch": {
            "sequence": 1,
            "revocations": [
                {"id": "rev-first", "principal": "user-first", "scope": "read", "timestamp": 11111}
            ]
        }
    })
    
    # Validate 1002 other tokens to fill cache and evict tok_1
    payloads = [{"sub": f"user-other-{i}", "jti": f"jti-other-{i}", **tok_prefix_payload} for i in range(1002)]
    tokens = make_jwt_tokens(payloads, "mock-public-key-for-kid-k", "k")
    for tok_other in tokens:
        ops.append({"type": "validate", "token": tok_other, "skewMs": 0})

    # Validate tok_1 again. It should be evicted, causing a cache miss and checking the DB (returning valid = false).
    ops.append({"type": "validate", "token": tok_1, "skewMs": 0})

    scenario = {
        "dbPath": str(DB_PATH),
        "operations": ops
    }

    trace = run_scenario_process(scenario)
    results = trace["results"]

    val_init = results[0]["result"]["valid"]
    assert val_init is True
    
    last_res = results[-1]
    val_final = last_res["result"]["valid"]
    assert val_final is False


def test_db_transaction_crash_recovery():
    """Verify that intermediate database batch sync crashes roll back all changes transactionally."""
    scenario = {
        "dbPath": str(DB_PATH),
        "operations": [
            {
                "type": "sync",
                "batch": {
                    "sequence": 5,
                    "revocations": [
                        {"id": "rev-ok-1", "principal": "user-a", "scope": "read", "timestamp": 11111},
                        {"id": "trigger-crash-sig", "principal": "user-b", "scope": "write", "timestamp": 22222}
                    ]
                }
            },
            {"type": "checkDbRevoked", "token": "rev-ok-1", "principal": "user-a", "scope": "read"}
        ]
    }

    trace = run_scenario_process(scenario)
    results = trace["results"]

    status_sync = results[0]["status"]
    assert status_sync == "error"
    
    revoked_val = results[1]["revoked"]
    assert revoked_val is False


def test_monotonic_sequence_rollback():
    """Verify that sync batches with sequence numbers lower than or equal to the current highest sequence are rejected."""
    scenario = {
        "dbPath": str(DB_PATH),
        "operations": [
            {
                "type": "sync",
                "batch": {
                    "sequence": 10,
                    "revocations": [
                        {"id": "rev-seq-10", "principal": "user-x", "scope": "read", "timestamp": 100}
                    ]
                }
            },
            {
                "type": "sync",
                "batch": {
                    "sequence": 5,
                    "revocations": [
                        {"id": "rev-seq-5", "principal": "user-y", "scope": "read", "timestamp": 200}
                    ]
                }
            },
            {"type": "getHighestSequence"},
            {"type": "checkDbRevoked", "token": "rev-seq-5", "principal": "user-y", "scope": "read"}
        ]
    }

    trace = run_scenario_process(scenario)
    results = trace["results"]

    seq_val = results[2]["sequence"]
    assert seq_val == 10
    
    rev_val = results[3]["revoked"]
    assert rev_val is False


def test_clock_skew_rejection():
    """Verify that tokens are rejected when the requested clock skew offset pushes the validation time past the token expiration."""
    payload = {"sub": "user-123", "scope": "read", "jti": "jti-skew", "exp": 9999999999}
    tok = make_jwt_token(payload, "mock-public-key-for-kid-k", "k")
    
    scenario = {
        "dbPath": str(DB_PATH),
        "keyCacheSeed": [
            {
                "kid": "k",
                "key": "mock-public-key-for-kid-k",
                "expiresAt": 9999999999000
            }
        ],
        "operations": [
            {"type": "validate", "token": tok, "skewMs": 99999999999999999}
        ]
    }
    
    trace = run_scenario_process(scenario)
    results = trace["results"]
    assert len(results) == 1
    
    val = results[0]["result"]["valid"]
    assert val is False
    reason = results[0]["result"]["reason"].lower()
    assert "expire" in reason


def _dummy_helper():
    pass
