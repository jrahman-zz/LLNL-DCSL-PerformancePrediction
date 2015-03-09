#include "perf_counters.h"
#include "papi_util.h"

int init_perf_counters(perf_counters_t **counters) {
    int events[] = {
        PAPI_L2_TCA,
        PAPI_L2_TCM,
        PAPI_L3_TCA,
        PAPI_L3_TCM,
        PAPI_TOT_INS,
        PAPI_TOT_CYC,
        PAPI_LD_INS,
        /*PAPI_SR_INS,
        PAPI_BR_INS,*/
        PAPI_FP_INS
    };
    char *names[] = {
        "L2 Accesses",          // 0
        "L2 Misses",            // 1
        "L3 Accesses",          // 2
        "L3 Misses",            // 3
        "Total instructions",   // 4
        //"Total Cycles",         // 5
        "Load instructions",    // 6
        /*"Store instructions", // 6
        "Branch instructions",  // 7*/
        "FP instructions"       // 7
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

    //print_counters(counters);

    double ips;
    ips = counters->accum[4] / counters->elapsed_time * 1000000;
    double l2m;
    l2m = counters->accum[1] / counters->accum[0];
    double l3m;
    l3m = counters->accum[3] / counters->accum[2];
    double ipc;
    //ipc = counters->accum[4] / counters->accum[5];
    printf("PAPI - L2 Miss Rate: %f\n", l2m);
    printf("PAPI - L3 Miss Rate: %f\n", l3m);
    printf("PAPI - IPS: %f\n", ips);
    //printf("PAPI - IPC: %f\n", ipc);

    //printf("PAPI - Mispredict: %f\n", counters->accum[6]/counters->accum[5]);
    //printf("PAPI - Load: %f\n", counters->accum[5]/counters->accum[4]);
    //printf("PAPI - Store: %f\n", counters->accum[6]/counters->accum[4]);
    //printf("PAPI - Branch: %f\n", counters->accum[7]/counters->accum[4]);
    //printf("PAPI - FP: %f\n", counters->accum[8]/counters->accum[4]);
    return 0;
}
