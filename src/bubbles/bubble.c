/**
 * Author: Yunqi Zhang
 * Email: yunqi@umich.edu
 *
 * Original Bubble by: Jason Mars (mars.ninja@gmail.com)
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>

#define MASK 0xd0000001u
#define RAND (lfsr = (lfsr >> 1) ^ (unsigned int)(0 - (lfsr & 1u) & MASK))
#define MAX_FOOTPRINT (67108864)
#define MIN_FOOTPRINT 128*1024
#define CACHE_LINE_SIZE 64

char* data_chunk;

struct params {
  float factor;
  unsigned int delay_ms;
  int bubbles;
};

volatile unsigned int footprint = MIN_FOOTPRINT;
volatile unsigned int keep_running = 1;

void *thread_main(void *param) {
  struct params* params = (struct params*)param;

  while(1) {
    usleep(1000 * params->delay_ms);
    if (footprint * params->factor > MAX_FOOTPRINT) {
      if (--(params->bubbles) == 0) {
        keep_running = 0;
      }
      footprint = MIN_FOOTPRINT;
    } else {
      footprint *= params->factor;
    }
  }
}

int main (int argc, char* argv[]) {
  if (argc < 3) {
    fprintf(stderr, "Invalid parameters\n");
    return 1;
  }
 
  register unsigned lfsr = time(0);
 
  struct params params;
  params.factor = atof(argv[1]);
  params.delay_ms = atoi(argv[2]);

  if (argc >= 4) {
    params.bubbles = atoi(argv[3]);
  } else {
    params.bubbles = 0;
  }

  if (params.factor <= 0 || params.delay_ms <= 0) {
    fprintf(stderr, "Invalid parameters\n");
    return 1;
  }

  data_chunk = (char*) malloc (MAX_FOOTPRINT * sizeof(char));
  int i;

  // Start background thread to change size
  pthread_t tid;
  if (pthread_create(&tid, NULL, thread_main, (void*)&params)) {
    fprintf(stderr, "Failed to create background thread: %d\n");
    return 1;
  }

  register unsigned int fp = 0;
  while (keep_running) {
    
    if (fp != footprint) {
       struct timespec tv;
       clock_gettime(CLOCK_MONOTONIC, &tv);
       fprintf(stderr, "bubble %d %f\n", footprint, tv.tv_sec + (double)tv.tv_nsec / 1000000000.0);
    }
    fp = footprint;
    char* first_chunk  = data_chunk;
    char* second_chunk = data_chunk + fp/8;
    char* third_chunk = data_chunk + fp/4;
    char* fourth_chunk = data_chunk + 3*fp/8;
    char* fifth_chunk = data_chunk + fp/2;
    char* sixth_chunk = data_chunk + 5*fp/8;
    char* seventh_chunk = data_chunk + 3*fp/8;
    char* eighth_chunk = data_chunk + 7*fp/8;
    for (i = 0; i < ((fp >> 3) - CACHE_LINE_SIZE); i += CACHE_LINE_SIZE) {
      first_chunk[i]++;
      second_chunk[i]++;
      third_chunk[i]++;
      fourth_chunk[i]++;
      fifth_chunk[i]++;
      sixth_chunk[i]++;
      seventh_chunk[i]++;
      eighth_chunk[i]++;
      data_chunk[RAND % fp]++;
      first_chunk[i + CACHE_LINE_SIZE]++;
      second_chunk[i + CACHE_LINE_SIZE]++;
      third_chunk[i + CACHE_LINE_SIZE]++;
      fourth_chunk[i + CACHE_LINE_SIZE]++;
      fifth_chunk[i + CACHE_LINE_SIZE]++;
      sixth_chunk[i + CACHE_LINE_SIZE]++;
      seventh_chunk[i + CACHE_LINE_SIZE]++;
      eighth_chunk[i + CACHE_LINE_SIZE]++;
    }
  }
  return 0;
}