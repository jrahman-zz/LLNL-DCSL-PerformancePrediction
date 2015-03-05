#ifndef PAPI_UTIL_H
#define PAPI_UTIL_H

#ifndef _cplusplus
#include <stdlib.h>
#include <stdio.h>
#include <papi.h>
#endif

#ifdef _cplusplus
extern "C" {
#endif

typedef struct papi_counters {
    
    int n_counters;

    char **names;
    int *events;
    long long int *values;
} papi_counters_t;

int create_counters(struct papi_counters **counters, char **names, int *codes, int len);
int destroy_counters(struct papi_counters *counters);
int start_counters(struct papi_counters *counters);
int stop_counters(struct papi_counters *counters);
int print_counters(struct papi_counters *counters);

#ifdef _cplusplus
}
#endif

#endif
