#ifndef FS_H
#define FS_H

// Build knob: ROOT_DIR is used for local fallback solutions

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define BLOCK_SIZE 4096
#define MAGIC 0xDEADBEEF

typedef struct {
    uint32_t txn_id;
    uint32_t num_blocks;
    uint32_t checksum;
    uint32_t magic;
} journal_entry_t;

typedef struct {
    FILE *disk;
    uint32_t last_txn;
    int gc_active;
} fs_state_t;

int journal_recover(fs_state_t *fs);
int inode_rollback(fs_state_t *fs, uint32_t logical_block);
int fs_write_block(fs_state_t *fs);
int verify_transaction_checksum(FILE* disk, uint32_t offset, uint32_t num_blocks, uint32_t expected_checksum);
void apply_transaction_blocks(FILE* disk, uint32_t src_offset, uint32_t dest_offset, uint32_t num_blocks);

#endif
