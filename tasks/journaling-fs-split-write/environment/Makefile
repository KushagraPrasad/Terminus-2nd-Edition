CC = gcc
CFLAGS = -Wall -Wextra -g

all: fs_daemon

fs_daemon: fs_daemon.c journal.c inode.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f fs_daemon
