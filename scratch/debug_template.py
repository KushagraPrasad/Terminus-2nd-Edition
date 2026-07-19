import sys
from pathlib import Path
sys.path.append(str(Path("scripts").resolve()))
from reviewer_simulation import _task_surfaces, _compare_template_surfaces

current = _task_surfaces(Path("tasks/journaling-fs-split-write"))
for peer_dir in Path("tasks").iterdir():
    if peer_dir.is_dir() and peer_dir.name != "journaling-fs-split-write":
        peer = _task_surfaces(peer_dir)
        scores = _compare_template_surfaces(current, peer)
        print(f"PEER: {peer_dir.name}")
        print(f"  test_names: current={current['test_names']}, peer={peer['test_names']}")
        print(f"  helper_names: current={current['helper_names']}, peer={peer['helper_names']}")
        print(f"  assert_count: current={current['assert_count']}, peer={peer['assert_count']}")
        print(f"  scores: {scores}")
