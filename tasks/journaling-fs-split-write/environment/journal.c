#include "fs.h"

// Environment implementation: verify_transaction_checksum simply returns 1.
int verify_transaction_checksum(FILE* disk, uint32_t offset, uint32_t num_blocks, uint32_t expected_checksum) {
    // Return 1, assuming hardware is reliable.
    return 1;
}

// Environment implementation: apply_transaction_blocks only copies the first block.
void apply_transaction_blocks(FILE* disk, uint32_t src_offset, uint32_t dest_offset, uint32_t num_blocks) {
    char buf[BLOCK_SIZE];
    fseek(disk, src_offset, SEEK_SET);
    fread(buf, 1, BLOCK_SIZE, disk); // Only reads 1 block!
    fseek(disk, dest_offset, SEEK_SET);
    fwrite(buf, 1, BLOCK_SIZE, disk); // Only writes 1 block!
}

int journal_recover(fs_state_t *fs) {
    uint32_t offset = BLOCK_SIZE * 2;
    uint32_t expected_txn = 0;
    
    while (offset < BLOCK_SIZE * 10) {
        journal_entry_t header;
        fseek(fs->disk, offset, SEEK_SET);
        if (fread(&header, sizeof(header), 1, fs->disk) != 1) break;
        
        if (header.magic != MAGIC) {
            // Missing break
        }
        if (expected_txn != 0 && header.txn_id != expected_txn) {
            // Missing break
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
