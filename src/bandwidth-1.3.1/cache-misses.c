#include <stdlib.h>
#include <string.h>

extern int CacheMisses (void *ptr);

int main(int argc, char **argv) {
	//int cache_line = atoi(argv[1]);
	//int total_cache_lines = atoi(argv[2]);
	//int size = cache_line * total_cache_lines;
	//char *chunk = malloc (size);
	char *chunk = malloc (200000000);
	CacheMisses(chunk);
	return 0;
}
