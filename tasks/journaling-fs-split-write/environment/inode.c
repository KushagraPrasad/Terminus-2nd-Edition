#include "fs.h"

int inode_rollback(fs_state_t *fs, uint32_t block) {
    if (block < 11) return -1;
    
    uint32_t logical_block = block - 11;
    
    uint32_t csum_offset = 4096 + (logical_block / 4);
    
    uint32_t zero = 0;
    fseek(fs->disk, csum_offset, SEEK_SET);
    fwrite(&zero, 4, 1, fs->disk);
    
    return 0;
}
