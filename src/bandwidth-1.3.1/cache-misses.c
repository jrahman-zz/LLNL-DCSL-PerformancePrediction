#include <stdlib.h>
#include <string.h>

#define SIZE 100000000

extern int CacheMisses (void *ptr);

int main(int argc, char **argv) {
	//int cache_line = atoi(argv[1]);
	//int total_cache_lines = atoi(argv[2]);
	//int size = cache_line * total_cache_lines;
	//char *chunk = malloc (size);
	char *chunk = malloc(SIZE);
	memset(chunk, 0, SIZE);
	CacheMisses(chunk);
	return 0;
}
