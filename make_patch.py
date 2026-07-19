import os
import subprocess
import shutil

base_dir = r"c:\Users\kusha\OneDrive\Desktop\Projects\Dawgs\Terminal-main\tasks\journaling-fs-split-write"
tmp_base = r"c:\Users\kusha\OneDrive\Desktop\Projects\Dawgs\Terminal-main\tmp\patch_base"
tmp_fixed = r"c:\Users\kusha\OneDrive\Desktop\Projects\Dawgs\Terminal-main\tmp\patch_fixed"

# Recreate directories
for d in [tmp_base, tmp_fixed]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

# Copy base environment files
env_dir = os.path.join(base_dir, "environment")
for f in ["journal.c", "inode.c", "fs_daemon.c", "fs.h"]:
    shutil.copy(os.path.join(env_dir, f), os.path.join(tmp_base, f))
    shutil.copy(os.path.join(env_dir, f), os.path.join(tmp_fixed, f))

# Write fixed version of journal.c
fixed_journal = """#include "fs.h"

int verify_transaction_checksum(FILE* disk, uint32_t offset, uint32_t num_blocks, uint32_t expected_checksum) {
    uint32_t sum = 0;
    long original_pos = ftell(disk);
    fseek(disk, offset, SEEK_SET);
    for (uint32_t i = 0; i < num_blocks; i++) {
        char buf[BLOCK_SIZE];
        if (fread(buf, 1, BLOCK_SIZE, disk) != BLOCK_SIZE) return 0;
        for (int j = 0; j < BLOCK_SIZE; j++) {
            sum += (uint8_t)buf[j];
        }
    }
    fseek(disk, original_pos, SEEK_SET);
    return sum == expected_checksum;
}

void apply_transaction_blocks(FILE* disk, uint32_t src_offset, uint32_t dest_offset, uint32_t num_blocks) {
    char buf[BLOCK_SIZE];
    for (uint32_t i = 0; i < num_blocks; i++) {
        fseek(disk, src_offset + (i * BLOCK_SIZE), SEEK_SET);
        if (fread(buf, 1, BLOCK_SIZE, disk) != BLOCK_SIZE) break;
        fseek(disk, dest_offset + (i * BLOCK_SIZE), SEEK_SET);
        fwrite(buf, 1, BLOCK_SIZE, disk);
    }
}

int journal_recover(fs_state_t *fs) {
    uint32_t offset = BLOCK_SIZE * 2;
    uint32_t expected_txn = 0;
    
    while (offset < BLOCK_SIZE * 10) {
        journal_entry_t header;
        fseek(fs->disk, offset, SEEK_SET);
        if (fread(&header, sizeof(header), 1, fs->disk) != 1) break;
        
        if (header.magic != MAGIC) {
            break;
        }
        if (expected_txn != 0 && header.txn_id != expected_txn) {
            break;
        }
        
        if (!verify_transaction_checksum(fs->disk, offset + sizeof(header), header.num_blocks, header.checksum)) {
            break;
        }
        
        apply_transaction_blocks(fs->disk, offset + sizeof(header), BLOCK_SIZE * 11, header.num_blocks);
        
        offset += sizeof(header) + (header.num_blocks * BLOCK_SIZE);
        expected_txn = header.txn_id + 1;
        fs->last_txn = header.txn_id;
    }
    
    return 0;
}
"""

# Write fixed version of inode.c
fixed_inode = """#include "fs.h"

int inode_rollback(fs_state_t *fs, uint32_t block) {
    if (block < 11) return -1;
    
    uint32_t logical_block = block - 11;
    
    uint32_t csum_offset = 4096 + (logical_block * 4);
    
    uint32_t zero = 0;
    fseek(fs->disk, csum_offset, SEEK_SET);
    fwrite(&zero, 4, 1, fs->disk);
    
    return 0;
}
"""

# Write fixed version of fs_daemon.c
fixed_fs_daemon = """#include "fs.h"
#include <string.h>

void fs_gc_run(fs_state_t *fs) {
    fs->gc_active = 1;
    fseek(fs->disk, BLOCK_SIZE * 10, SEEK_SET);
    // fs->gc_active = 0; 
}

int fs_write_block(fs_state_t *fs) {
    if (fs->gc_active == 0) {
        fprintf(stderr, "PANIC: Stale GC state, cannot write.\\n");
        exit(1);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <disk_image> <command>\\n", argv[0]);
        return 1;
    }
    
    fs_state_t fs;
    fs.disk = fopen(argv[1], "r+");
    if (!fs.disk) {
        perror("fopen");
        return 1;
    }
    
    fs.gc_active = 0;
    fs.last_txn = 0;
    
    if (strcmp(argv[2], "recover") == 0) {
        journal_recover(&fs);
        inode_rollback(&fs, 12); 
        fs_gc_run(&fs);
        printf("Recovery complete.\\n");
    } else if (strcmp(argv[2], "write") == 0) {
        journal_recover(&fs);
        fs_gc_run(&fs);
        fs_write_block(&fs);
        printf("Write complete.\\n");
    } else if (strcmp(argv[2], "check_txn") == 0) {
        journal_recover(&fs);
        printf("Last Txn: %u\\n", fs.last_txn);
    }
    
    fclose(fs.disk);
    return 0;
}
"""

with open(os.path.join(tmp_fixed, "journal.c"), "w", newline="\n") as f:
    f.write(fixed_journal)

with open(os.path.join(tmp_fixed, "inode.c"), "w", newline="\n") as f:
    f.write(fixed_inode)

with open(os.path.join(tmp_fixed, "fs_daemon.c"), "w", newline="\n") as f:
    f.write(fixed_fs_daemon)

# Generate patch using diff in WSL
patch_file = os.path.join(base_dir, "solution", "solution.patch")
# Clean up previous patch file
if os.path.exists(patch_file):
    os.remove(patch_file)

# Run diff in WSL for each file
with open(patch_file, "w", newline="\n") as out:
    for filename in ["journal.c", "inode.c", "fs_daemon.c"]:
        # Run diff -u between base and fixed
        res = subprocess.run([
            "wsl", "diff", "-u",
            f"/mnt/c/Users/kusha/OneDrive/Desktop/Projects/Dawgs/Terminal-main/tmp/patch_base/{filename}",
            f"/mnt/c/Users/kusha/OneDrive/Desktop/Projects/Dawgs/Terminal-main/tmp/patch_fixed/{filename}"
        ], capture_output=True, text=True)
        # Normalize the diff output paths to environment/filename
        diff_lines = res.stdout.splitlines()
        for line in diff_lines:
            if line.startswith("--- "):
                out.write(f"--- environment/{filename}\n")
            elif line.startswith("+++ "):
                out.write(f"+++ environment/{filename}\n")
            else:
                out.write(line + "\n")

print("Generated clean solution.patch at:", patch_file)
