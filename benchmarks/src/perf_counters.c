#include "perf_counters.h"
#include "papi_util.h"

int init_perf_counters(perf_counters_t **counters) {
    int events[] = {
        PAPI_L2_TCA,
        PAPI_L2_TCM,
        PAPI_L3_TCA,
        PAPI_L3_TCM,
        PAPI_TOT_INS,
    };
    char *names[] = {
        "L2 Accesses",
        "L2 Misses",
        "L3 Accesses",
        "L3 Misses",
        "Total instructions",
    };
    return create_counters(counters, names, events, 5);
}

int start_perf_counters(perf_counters_t *counters) {
    return start_counters(counters);     
}

int stop_perf_counters(perf_counters_t *counters) {
    return accum_counters(counters);
}

int reset_perf_counters(perf_counters_t *counters) {
    int ret = stop_counters(counters);
    counters->temp_time = 0;
    counters->elapsed_time = 0;
    for (int i = 0; i < counters->n_counters; i++) {
        counters->accum[i] = 0;
    }
    return ret;
}

int free_perf_counters(perf_counters_t *counters) {
    return destroy_counters(counters);
}

int print_perf_counters(perf_counters_t *counters) {
    if (counters == NULL || counters->state != STOPPED) {
        return -1;
    }
    double ips;
    ips = counters->accum[4] / counters->elapsed_time * 1000000;
    double l2m;
    l2m = counters->accum[1] / counters->accum[0];
    double l3m;
    l3m = counters->accum[3] / counters->accum[2];
    printf("PAPI - L2 Miss Rate: %f\nPAPI - L3 Miss Rate: %f\nPAPI - IPS: %f\n", l2m, l3m, ips);
    return 0;
}
