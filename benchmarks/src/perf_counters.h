#ifndef PERF_COUNTERS_H
#define PERF_COUNTERS_H

#include "papi_util.h"

#define CACHE

typedef papi_counters_t perf_counters_t;

int init_perf_counters(perf_counters_t **counters);

/**
 * Start counting perf counters
 */
int start_perf_counters(perf_counters_t *counters);

/**
 * Stop perf counters, accumulating
 */
int stop_perf_counters(perf_counters_t *counters);

/**
 * Reset all performance information back to 0
 * And stop counters if there are running
 */
int reset_perf_counters(perf_counters_t *counters);

/**
 * Release perf counter resources
 */
int free_perf_counters(perf_counters_t *counters);

/**
 * Print collected performance information
 */
int print_perf_counters(perf_counters_t *counters);

#endif
