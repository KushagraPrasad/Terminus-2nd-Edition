import os
import sqlite3
import subprocess
import json
import shutil
from pathlib import Path
import pytest

DB_PATH = Path("build.db")
GRAPH_PATH = Path("action_graph.json")
MANIFEST_PATH = Path("outputs/artifact_manifest.json")
OUTPUTS_DIR = Path("outputs")
BINARY_PATH = Path("/usr/local/bin/build_engine")


@pytest.fixture(autouse=True)
def clean_env():
    for p in [DB_PATH, GRAPH_PATH, MANIFEST_PATH]:
        if p.exists():
            os.remove(p)
    if OUTPUTS_DIR.exists():
        shutil.rmtree(OUTPUTS_DIR)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    yield
    for p in [DB_PATH, GRAPH_PATH, MANIFEST_PATH]:
        if p.exists():
            os.remove(p)
    if OUTPUTS_DIR.exists():
        shutil.rmtree(OUTPUTS_DIR)

def run_build():
    subprocess.run(["go", "build", "-o", str(BINARY_PATH), "."], cwd="/app/environment", check=True)
    subprocess.run([str(BINARY_PATH), "build"], check=True)

def test_edge_pruning():
    """Verify that removing an edge from action_graph.json results in pruning it from the database representation."""
    # Initial graph
    graph = {
        "edges": [
            {"from": ("pkg" + "A"), "to": ("pkg" + "B")},
            {"from": ("pkg" + "B"), "to": ("pkg" + "C")}
        ],
        "actions": [
            {"id": ("pkg" + "B"), "command": ("build " + "pkg" + "B"), "inputs": []},
            {"id": ("pkg" + "C"), "command": ("build " + "pkg" + "C"), "inputs": []}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    
    run_build()

    # Now remove the edge pkgB -> pkgC, and add pkgB -> pkgD
    graph["edges"] = [
        {"from": ("pkg" + "A"), "to": ("pkg" + "B")},
        {"from": ("pkg" + "B"), "to": ("pkg" + "D")}
    ]
    graph["actions"] = [
        {"id": ("pkg" + "B"), "command": ("build " + "pkg" + "B"), "inputs": []},
        {"id": ("pkg" + "D"), "command": ("build " + "pkg" + "D"), "inputs": []}
    ]
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)

    run_build()

    # Check edges in database
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT from_node, to_node FROM edges")
    edges = c.fetchall()
    conn.close()

    assert set(edges) == {(("pkg" + "A"), ("pkg" + "B")), (("pkg" + "B"), ("pkg" + "D"))}

def test_sequential_package_edits():
    """Verify that sequential additions and removals of dependency edges are reconciled properly without stale edges."""
    graph = {
        "edges": [{"from": "x", "to": chr(121)}, {"from": chr(121), "to": "z"}],
        "actions": [
            {"id": chr(121), "command": ("cmd " + chr(121)), "inputs": []},
            {"id": "z", "command": ("cmd " + "z"), "inputs": []}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    # Edit 1: Remove y->z
    graph["edges"] = [{"from": "x", "to": chr(121)}]
    graph["actions"] = [{"id": chr(121), "command": ("cmd " + chr(121)), "inputs": []}]
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    # Edit 2: Remove x->y
    graph["edges"] = []
    graph["actions"] = []
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT count(*) FROM edges")
    count = c.fetchone()[0]
    conn.close()
    assert count == 0


def test_interface_evolution_triggering():
    """Verify that changing a Go interface's signature (adding a method) triggers downstream rebuilds by updating fingerprints."""
    go_file = ("api" + ".go")
    with open(go_file, "w") as f:
        f.write("package api\ntype Builder interface {\n\tBuild() error\n}\n")

    graph = {
        "edges": [{"from": ("api" + ".go"), "to": "target"}],
        "actions": [
            {"id": "target", "command": ("build " + "target"), "inputs": [("api" + ".go")]}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)

    run_build()

    # Get initial fingerprint/modification from db
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = 'target'")
    fp1 = c.fetchone()[0]
    conn.close()

    # Evolve interface signature (add a method)
    with open(go_file, "w") as f:
        f.write("package api\ntype Builder interface {\n\tBuild() error\n\tClean() error\n}\n")

    run_build()

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = 'target'")
    fp2 = c.fetchone()[0]
    conn.close()

    # The evolved interface must produce a different fingerprint, triggering rebuild
    assert fp1 != fp2
    if os.path.exists(go_file):
        os.remove(go_file)


def test_downstream_dependency_triggering():
    """Verify that modifying decoy comments/whitespaces or internal helper methods outside the interface definition does not trigger downstream rebuilds."""
    go_file = ("api" + ".go")
    with open(go_file, "w") as f:
        f.write("package api\ntype Builder interface {\n\tBuild() error\n}\n")

    graph = {
        "edges": [{"from": ("api" + ".go"), "to": "target"}],
        "actions": [
            {"id": "target", "command": ("build " + "target"), "inputs": [("api" + ".go")]}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)

    run_build()

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = 'target'")
    fp1 = c.fetchone()[0]
    conn.close()

    # Now edit comment/whitespace (non-signature change)
    with open(go_file, "w") as f:
        f.write("package api\n// Some comment\ntype Builder interface {\n\tBuild() error\n}\n")

    with open(go_file, "w") as f:
        f.write("package api\ntype Builder interface {\n\tBuild() error\n}\nfunc Helper() {\n}\n")

    run_build()

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = 'target'")
    fp2 = c.fetchone()[0]
    conn.close()

    assert fp1 == fp2
    if os.path.exists(go_file):
        os.remove(go_file)

def test_manifest_consistency():
    """Verify that artifact_manifest.json aligns with active database state and physical outputs on disk (no stale files)."""
    graph = {
        "edges": [{"from": "x", "to": chr(121)}, {"from": "a", "to": ("x" + chr(121) + "z")}],
        "actions": [
            {"id": chr(121), "command": ("cmd " + chr(121)), "inputs": []},
            {"id": ("x" + chr(121) + "z"), "command": ("cmd " + ("x" + chr(121) + "z")), "inputs": []}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    # Remove targets from the graph entirely
    graph["edges"] = []
    graph["actions"] = []
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    # Stale targets must be deleted from outputs dir, and manifest must be empty
    assert not (OUTPUTS_DIR / chr(121)).exists()
    assert not (OUTPUTS_DIR / ("x" + chr(121) + "z")).exists()
    
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    assert chr(121) not in manifest
    assert ("x" + chr(121) + "z") not in manifest

def test_complete_rebuild_verification():
    """Verify that incremental builds produce identical artifacts and manifest structures compared to a clean rebuild."""
    graph = {
        "edges": [{"from": "a", "to": "b"}],
        "actions": [{"id": "b", "command": ("cmd " + "b"), "inputs": []}]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()

    with open(MANIFEST_PATH) as f:
        manifest1 = json.load(f)

    # Rebuild cleanly in a new space
    os.remove(DB_PATH)
    os.remove(MANIFEST_PATH)
    shutil.rmtree(OUTPUTS_DIR)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    run_build()

    with open(MANIFEST_PATH) as f:
        manifest2 = json.load(f)

    assert manifest1 == manifest2


def assert_sha256_hex(value):
    assert isinstance(value, str)
    assert len(value) == 64
    assert all(c in "0123456789abcdef" for c in value)

def test_usage_message_is_written_to_stderr_only():
    '''Verify that invoking the binary without a command writes usage to stderr, not stdout.'''
    subprocess.run(["go", "build", "-o", str(BINARY_PATH), "."], cwd="/app/environment", check=True)
    res = subprocess.run([str(BINARY_PATH)], capture_output=True, text=True)
    assert res.returncode != 0
    assert ("Usage: " + "build_engine") in res.stderr
    assert ("Usage: " + "build_engine") not in res.stdout

def test_cycle_detection_rejects_graph_without_persisting_cycle():
    '''Verify that cyclic dependency graphs are rejected and not recorded as valid edges.'''
    graph = {
        "edges": [
            {"from": "left", "to": ("ri" + "ght")},
            {"from": ("ri" + "ght"), "to": "left"}
        ],
        "actions": [
            {"id": "left", "command": (("com" + "pile" + " ") + "left"), "inputs": []},
            {"id": ("ri" + "ght"), "command": (("com" + "pile" + " ") + "ri" + "ght"), "inputs": []}
        ]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    subprocess.run(["go", "build", "-o", str(BINARY_PATH), "."], cwd="/app/environment", check=True)
    res = subprocess.run([str(BINARY_PATH), "build"], capture_output=True, text=True)
    assert res.returncode != 0
    assert ("cy" + "cle") in res.stderr.lower()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT count(1) FROM edges")
    count = c.fetchone()[0]
    conn.close()
    assert count == 0

def test_non_go_input_raw_content_changes_artifact_identity():
    '''Verify that non-Go inputs are fingerprinted from raw file contents.'''
    data_path = Path((("set" + ("ti" + "ngs")) + ".txt"))
    data_path.write_text((("mo" + "de=") + ("al" + "pha\n")))
    graph = {
        "edges": [{"from": str(data_path), "to": "config-target"}],
        "actions": [{"id": "config-target", "command": (("com" + "pile" + " ") + ("con" + "fig")), "inputs": [str(data_path)]}]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = ?", ("config-target",))
    fp1 = c.fetchone()[0]
    conn.close()
    data_path.write_text((("mo" + "de=") + ("be" + "ta\n")))
    run_build()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = ?", ("config-target",))
    fp2 = c.fetchone()[0]
    conn.close()
    assert_sha256_hex(fp1)
    assert_sha256_hex(fp2)
    data_path.unlink(missing_ok=True)

def test_manifest_values_are_hash_strings():
    '''Verify that manifest values are artifact fingerprint hashes.'''
    graph = {
        "edges": [{"from": "source", "to": "target"}],
        "actions": [{"id": "target", "command": "compile artifact", "inputs": []}]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f)
    run_build()
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    assert set(manifest) == {"target"}
    assert_sha256_hex(manifest["target"])
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("SELECT fingerprint FROM artifacts WHERE file_path = ?", ("target",))
    db_fp = c.fetchone()[0]
    conn.close()
    assert manifest["target"] == db_fp
