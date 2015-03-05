#include "papi_util.h"
#include "papi_counters.h"

#define ARR_SIZE 1024

int main(int argc, char **argv) {


    papi_counters_t *counters;

    counters = create_miss_counters();    
    if (counters == NULL) {
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
