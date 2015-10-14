/**
 * Author: Yunqi Zhang
 * Email: yunqi@umich.edu
 *
 * Original Bubble by: Jason Mars (mars.ninja@gmail.com)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MASK 0xd0000001u
#define RAND (lfsr = (lfsr >> 1) ^ (unsigned int)(0 - (lfsr & 1u) & MASK))
#define CACHE_LINE_SIZE 64
#ifndef FOOTPRINT
#define FOOTPRINT (24*1024*1024)
#endif

char* data_chunk;

int main (int argc, char* argv[]) {
  register unsigned lfsr;
  lfsr = time(NULL);
  int i;

  data_chunk = (char*)malloc(FOOTPRINT * sizeof(char));
  
  time_t time_limit;
  if (argc >= 2) {
    time_limit = atoi(argv[1]);
  } else {
    time_limit = 0;
  }
 
  // Print PID for background killing purposes
  printf("%d\n", getpid());
  fflush(stdout);
 
  time_t start_time = time(NULL);

  // Print initial time from system clock so the processing scripts
  // can add it to the relative times given by perf
  //struct timespec tv;
  //clock_gettime(CLOCK_MONOTONIC, &tv);
  //fprintf(stderr, "%f\n", tv.tv_sec + (double)tv.tv_nsec / 1000000000.0);

  while (time_limit == 0 || time(NULL) - start_time <= time_limit) {
    char* first_chunk  = data_chunk;
    char* second_chunk = data_chunk + (FOOTPRINT >> 2);
    char* third_chunk = data_chunk + (FOOTPRINT >> 1);
    char* fourth_chunk = data_chunk + 3 * (FOOTPRINT >> 2);

    for (i = 0; i < (FOOTPRINT >> 2); i += CACHE_LINE_SIZE) {
      //data_chunk[RAND % FOOTPRINT]++;
      first_chunk[i] = second_chunk[i] + 1;
      data_chunk[RAND % FOOTPRINT]++;
      third_chunk[i] = fourth_chunk[i] + 1;
    }
    for (i = 0; i < (FOOTPRINT >> 2); i += CACHE_LINE_SIZE) {
      //data_chunk[RAND % FOOTPRINT]++;
      second_chunk[i] = first_chunk[i] + 1;
      data_chunk[RAND % FOOTPRINT]++;
      fourth_chunk[i] = third_chunk[i] + 1;
    }
  }
  return 0;
}
