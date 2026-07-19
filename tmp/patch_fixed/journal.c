#include "fs.h"

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
