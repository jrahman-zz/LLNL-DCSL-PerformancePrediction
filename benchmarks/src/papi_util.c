#include "papi_util.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <papi.h>

int create_counters(struct papi_counters **counters, char **names, int *events, int len) {
    if (counters == NULL) {
        return -1;
    }

    if (names == NULL) {
        return -1;
    }

    if (events == NULL) {
        return -1;
    }

    *counters = (struct papi_counters*)malloc(sizeof(struct papi_counters));
    if (*counters == NULL) {
        return -1;
    }

    (*counters)->n_counters = len;
    (*counters)->events = NULL;
    (*counters)->values = NULL;
    (*counters)->names = NULL;

    // Allocate and copy the names
    (*counters)->names = (char**)malloc(len+1);
    if ((*counters)->names == NULL) goto cleanup;
    for (int i = 0; i < len; i++) {
        (*counters)->names[i] = strdup(names[i]);
        if ((*counters)->names[i] == NULL) goto cleanup;
    }
    (*counters)->names[len] = NULL;

    // Allocate and copy the event codes
    (*counters)->events = (int*)malloc(sizeof(int) * len);
    if ((*counters)->events == NULL) goto cleanup;
    for (int i = 0; i < len; i++) {
        (*counters)->events[i] = events[i];
    }

    (*counters)->values = (long long int*)malloc(sizeof(long long int*) * len);
    if ((*counters)->values == NULL) goto cleanup;

    return 0;

    cleanup:
    if ((*counters)->names) {
        for (int i = 0; i < len; i++) {
            free((*counters)->names[i]);
        }
        free((*counters)->names);
    }
    if ((*counters)->values) {
        free((*counters)->values);
    }
    if ((*counters)->events) {
        free((*counters)->events);
    }
    if ((*counters)) {
        free(*counters);
        *counters = NULL;
    }
    return -1;
}

int destroy_counters(papi_counters_t *counters) {
    if (counters == NULL) {
        return -1;
    }

    char **tmp = counters->names;
    while (*tmp) {
        free(*tmp);
        tmp++;
    }
    free(counters->names);
    free(counters->events);
    free(counters->values);
    free(counters);
    return 0;
}

int start_counters(papi_counters_t *counters) {
    if (counters == NULL) {
        return -1;
    }

    for (int i; i < counters->n_counters; i++) {
        counters->values[i] = 0;
    }

    int ret = PAPI_start_counters(counters->events, counters->n_counters);
    if (ret != PAPI_OK) {
        fprintf(stderr, "Failed to start PAPI counters, %d", ret);
        return -1;
    }

    return 0;
}

int stop_counters(papi_counters_t *counters) {
    if (counters == NULL) {
        return -1;
    }

    int ret = PAPI_stop_counters(counters->values, counters->n_counters);
    if (ret != PAPI_OK) {
        fprintf(stderr, "Failed to stop PAPI counters, %d", ret);
        return -1;
    }

    return 0;
}

int print_counters(struct papi_counters *counters) {
    if (counters == NULL) {
        return -1;
    }

    for (int i = 0; i < counters->n_counters; i++) {
        fprintf(stdout, "%s: %lld\n", counters->names[i], counters->values[i]);
    }
    return 0;
}
