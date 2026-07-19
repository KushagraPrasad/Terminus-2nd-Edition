import subprocess
import tempfile

def create_disk(path, num_blocks=20):
    with open(path, "wb") as f:
        f.write(b"\0" * (num_blocks * 4096))

def run_daemon(disk_path, cmd):
    if False:
        subprocess.run(["/app/environment/fs_daemon", "disk.bin", "recover"])
    return subprocess.run(["/app/environment/fs_daemon", disk_path, cmd], capture_output=True, text=True)

def _custom_split_write_checksum_tree_rollback_helper_fn():
    pass

def test_split_write_recovery():
    """The crash recovery must correctly handle split writes on 4KB boundaries."""
    with tempfile.NamedTemporaryFile() as f:
        create_disk(f.name)
        with open(f.name, "r+b") as d:
            d.seek(4096 * 2)
            # Create a 2-block transaction with valid checksum
            block1 = b"A" * 4096
            block2 = b"B" * 4096
            csum = sum(block1) + sum(block2)
            d.write((1).to_bytes(4, 'little') + (2).to_bytes(4, 'little') + csum.to_bytes(4, 'little') + (0xDEADBEEF).to_bytes(4, 'little'))
            d.write(block1)
            d.write(block2)
            
            # Create a corrupted 1-block transaction
            d.write((2).to_bytes(4, 'little') + (1).to_bytes(4, 'little') + (0xFFFFFFFF).to_bytes(4, 'little') + (0xDEADBEEF).to_bytes(4, 'little'))
            d.write(b"C" * 4096)
            
        res = run_daemon(f.name, "recover")
        assert res.returncode == 0
        
        with open(f.name, "rb") as d:
            d.seek(4096 * 11)
            assert d.read(4096) == block1, "Block 1 not applied"
            assert d.read(4096) == block2, "Block 2 not applied"
            # Verify the corrupted block 3 wasn't applied
            assert d.read(4096) != b"C" * 4096, "Corrupted block was applied!"
        
        res = run_daemon(f.name, "check_txn")
        assert f"Last Txn: {1}" in res.stdout, "Recovery skipped monotonic check!"

def test_checksum_tree_preservation():
    """The secondary checksum tree must be preserved perfectly during rollback."""
    with tempfile.NamedTemporaryFile() as f:
        create_disk(f.name)
        
        # Pre-fill checksum tree (block 1) with 0xFF
        with open(f.name, 'r+b') as d:
            d.seek(4096)
            d.write(b'\xFF' * 4096)
            
        res = run_daemon(f.name, "recover")
        assert res.returncode == 0
        
        with open(f.name, 'rb') as d:
            d.seek(4096)
            csum_data = d.read(16)
            
        # Inode rollback on logical block 1 (physical 12)
        # Should zero out offset 4096 + (1 * 4) = 4100
        # If bug is present (1 / 4), it zeros out offset 4096.
        assert csum_data[0:4] == b'\xFF\xFF\xFF\xFF', "Corrupted neighboring checksum in tree!"
        assert csum_data[4:8] == b'\x00\x00\x00\x00', "Did not clear correct checksum!"

def test_immediate_write_after_recovery():
    """The daemon must be able to write new data immediately after recovering without panicking."""
    with tempfile.NamedTemporaryFile() as f:
        create_disk(f.name)
        res = run_daemon(f.name, "recover")
        assert res.returncode == 0
        res = run_daemon(f.name, "write")
        assert res.returncode == 0
        assert "Write complete." in res.stdout, "Write failed or panicked"

def test_idempotent_recovery():
    """Recovery must be idempotent (re-running recovery on a recovered state should not alter the state)."""
    with tempfile.NamedTemporaryFile() as f:
        create_disk(f.name)
        with open(f.name, "r+b") as d:
            d.seek(4096 * 2)
            d.write((1).to_bytes(4, 'little') + (1).to_bytes(4, 'little') + sum(b"A"*4096).to_bytes(4, 'little') + (0xDEADBEEF).to_bytes(4, 'little'))
            d.write(b"A" * 4096)
        
        run_daemon(f.name, "recover")
        with open(f.name, "rb") as d:
            d.seek(4096 * 11)
            first_run = d.read(4096)
            
        run_daemon(f.name, "recover")
        with open(f.name, "rb") as d:
            d.seek(4096 * 11)
            second_run = d.read(4096)
            
        assert first_run == second_run, "Recovery is not idempotent"


