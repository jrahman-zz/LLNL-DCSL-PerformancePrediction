#include "papi_util.h"

#define ARR_SIZE 1024

int main(int argc, char **argv) {

    int events[] = {PAPI_L1_TCA, PAPI_L1_TCM, PAPI_L2_TCA, PAPI_L2_TCM, PAPI_L3_TCA, PAPI_L3_TCM};
    char *names[] = {"L1 Accesses", "L1 Misses", "L2 Accesses", "L2 Misses", "L3 Accesses", "L3 Misses"};

    struct papi_counters *counters;

    if (create_counters(&counters, names, events, sizeof(events)/sizeof(events[0])) != 0) {
        fprintf(stderr, "Failed to initialize the papi events\n");
        return 1;
    }

    if (start_counters(counters) != 0) {
        fprintf(stderr, "Failed to start counters\n");
        destroy_counters(counters);
        return 1;
    }

    int *arr = (int*)malloc(sizeof(int) * ARR_SIZE);
    free(arr);

    if (stop_counters(counters) != 0) {
        fprintf(stderr, "Failed to stop counters\n");
        destroy_counters(counters);
        return 1;
    }

    print_counters(counters);
    destroy_counters(counters);

    return 0;
}
