#ifndef PAPI_UTIL_H
#define PAPI_UTIL_H

#ifndef __cplusplus
#include <stdlib.h>
#include <stdio.h>
#include <papi.h>
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef struct papi_counters {
    
    int n_counters;

    char **names;
    int *events;
    long long int *values;
} papi_counters_t;

int create_counters(papi_counters_t **counters, char **names, int *codes, int len);
int destroy_counters(papi_counters_t *counters);
int start_counters(papi_counters_t *counters);
int stop_counters(papi_counters_t *counters);
int print_counters(papi_counters_t *counters);

#ifdef __cplusplus
}
#endif

#endif
