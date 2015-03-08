#include "perf_counters.h"
#include "papi_util.h"

int init_perf_counters(perf_counters_t **counters) {
    int events[] = {
#ifdef CACHE
        PAPI_L2_TCA,
        PAPI_L2_TCM,
        PAPI_L3_TCA,
        PAPI_L3_TCM,
#else
        PAPI_TOT_INS,
        PAPI_TOT_CYC
#endif
    };
    char *names[] = {
#ifdef CACHE
        "L2 Accesses",
        "L2 Misses",
        "L3 Accesses",
        "L3 Misses",
#else
        "Total instructions",
        "Total Cycles"
#endif
    };
#ifdef CACHE
    int len = 4;
#else
    int len = 2;
#endif
    return create_counters(counters, names, events, len);
}

int start_perf_counters(perf_counters_t *counters) {
    return start_counters(counters);     
}

int stop_perf_counters(perf_counters_t *counters) {
    return accum_counters(counters);
}

int reset_perf_counters(perf_counters_t *counters) {
    return stop_counters(counters);
}

int free_perf_counters(perf_counters_t *counters) {
    return destroy_counters(counters);
}

int print_perf_counters(perf_counters_t *counters) {
    if (counters == NULL || counters->state != STOPPED) {
        return -1;
    }
#ifdef IPC
    double ipc;
    ipc = counters->accum[0] / counters->accum[1];
#elif defined CACHE
    double l2m;
    l2m = counters->accum[1] / counters->accum[0];
    double l3m;
    l3m = counters->accum[1] / counters->accum[0];
#endif
    printf(
#ifdef CACHE
            "L2 Miss Rate: %f\nL3 Miss Rate: %f\n", l2m, l3m);
#else
            "IPC: %f\n", ipc);
#endif
    return 0;
}
