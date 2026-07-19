#include "fs.h"
#include <string.h>

void fs_gc_run(fs_state_t *fs) {
    fs->gc_active = 1;
    fseek(fs->disk, BLOCK_SIZE * 10, SEEK_SET);
    // fs->gc_active = 0; 
}

int fs_write_block(fs_state_t *fs) {
    if (fs->gc_active == 0) {
        fprintf(stderr, "PANIC: Stale GC state, cannot write.\n");
        exit(1);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <disk_image> <command>\n", argv[0]);
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
        printf("Recovery complete.\n");
    } else if (strcmp(argv[2], "write") == 0) {
        journal_recover(&fs);
        fs_gc_run(&fs);
        fs_write_block(&fs);
        printf("Write complete.\n");
    } else if (strcmp(argv[2], "check_txn") == 0) {
        journal_recover(&fs);
        printf("Last Txn: %u\n", fs.last_txn);
    }
    
    fclose(fs.disk);
    return 0;
}
