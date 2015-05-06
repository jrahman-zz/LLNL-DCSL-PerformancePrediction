

#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sstream>
#include <iostream>

#ifdef INTERFERE
#undef COUNTERS
#endif

/**
 *  * Custom PAPI performance counters are only reported
 *   * if requested upon compilation
 *    */
#ifdef COUNTERS
#include "perf_counters.h"
#define INIT_COUNTERS(counters) do {                \
    if (init_perf_counters(&(counters)) != 0) {     \
        printf("Failed to init counters\n");        \
        return 1;                                   \
    }                                               \
} while (0)
#define START_COUNTERS(counters) do {               \
    if (start_perf_counters(counters) != 0) {       \
        printf("Failed to start counters\n");       \
        return 1;                                   \
    }                                               \
} while (0)
#define END_COUNTERS(counters) do {                 \
    int ret = stop_perf_counters(counters);         \
    if (ret != 0) {                                 \
        printf("Failed to stop counters, %d\n", ret);   \
        return 1;                                   \
    }                                               \
} while (0)
#define PRINT_COUNTERS(counters) do {               \
    if(print_perf_counters(counters) != 0) {        \
        printf("Failed to collect counter data");    \
        return 1;                                   \
    }                                               \
} while(0)
#define FREE_COUNTERS(counters) free_perf_counters(counters)
#define RESET_COUNTERS(counters) reset_perf_counters(counters)
perf_counters_t *counters;
#else
#define INIT_COUNTERS(counters)
#define START_COUNTERS(counters)
#define END_COUNTERS(counters)
#define PRINT_COUNTERS(counters)
#define FREE_COUNTERS(counters)
#define RESET_COUNTERS(counters)
int counters;
#endif



#define FILE_COUNT 192
#define MAX_NAME_LEN 1000

// Store file names in BSS to save stack space, but still avoid dynamic allocation
char buf[FILE_COUNT][MAX_NAME_LEN];

struct duo {
  long higher;
  long lower;
};

struct duo result;

struct duo* duoDiff(long firstHigher, long firstLower, long secondHigher, long secondLower, long base)
{
    long h = firstHigher - secondHigher;
    long l = firstLower - secondLower;
    if (h < 0)
        return NULL;
    if (l < 0) {
        l += base;
        --h;
    }
    result.higher = h;
    result.lower = l;
    return &result;
}

std::stringstream decimalString;

std::string decimalFormat(long number, long base)
{
    decimalString.str("");
    decimalString << ".";

    while (number > 0) {
        number *= 10;
        decimalString << number / base;
        number %= base;
    }

    return decimalString.str();
}

double printTimespec(struct timespec& ts_start, struct timespec& ts_stop, char* app)
{
    struct duo* timeDuo = duoDiff((long) ts_stop.tv_sec, ts_stop.tv_nsec,
                                (long) ts_start.tv_sec, ts_start.tv_nsec,
                                1000000000);
    time_t elapsed_sec = (time_t) timeDuo->higher;
    long elapsed_nsec = timeDuo->lower;

    std::cout << "Time " << app << ": "
              << elapsed_sec << decimalFormat(elapsed_nsec, 1000000000) << std::endl;
    return (double)elapsed_sec + (double)elapsed_nsec/1000000000.0;
}

// Comparision function for sorting arrays of doubles
int compare_double(const void* a, const void* b) {
    if (*(double*)a < *(double*)b) return -1;
    if (*(double*)a > *(double*)b) return 1;
    return 0;
}

int run_instance() {

    int fd[FILE_COUNT];
    int ret, len;

    for (int i = 0; i < FILE_COUNT; i++) {
        fd[i] = -1;
    }

    // Open files
    for (int i = 0; i < FILE_COUNT; i++) {
        
        // Create the file
        fd[i] = open(buf[i], O_RDWR | O_CREAT);
        if (fd[i] < 0) {
            std::cout << "Failed to create file: " << std::string(buf[i])
                      << ", errno: " << errno << std::endl;
            ret = -1;
            goto cleanup;
        }

        // Write some dummy data into the file to actually exercise the metadata keeping
        len = strlen(buf[i]);
        ret = write(fd[i], buf, len);
        if (ret != len) {
            std::cout << "Failed to write to file: " << std::string(buf[i])
                      << ", errno: " << errno << std::endl;
            ret = -1;
            goto cleanup;
        }
    }

    sync();

    // Stat some files
    struct stat file_stat;
    for (int i = 0; i < FILE_COUNT; i++) {
        ret = stat(buf[i], &file_stat);
        if (ret != 0) {
            std::cout << "Failed to stat file: " << std::string(buf[i])
                      << ", errno: " << errno << std::endl;
            ret = -1;
            goto cleanup;
        }
    }

    ret = 0;
cleanup:

    for (int i = 0; i < FILE_COUNT; i++) {
        if (fd[i] > 0) {
            close(fd[i]);
        }
    }

	for (int i = 0; i < FILE_COUNT; i++) {
		if (fd[i] > 0 && remove(buf[i]) != 0) {
			std::cout << "Failed to remove file: " << std::string(buf[i])
					  << ", errno: " << errno << std::endl;
			remove(buf[i]); // Try again
		}
	}

    return ret;
}

int run_benchmark(char *basedir, int repetitions) {

    int ret, len;
    double *results = NULL;
    
    if (repetitions <= 0 || !basedir) {
        std::cout << "Bad arguments" << std::endl;
        ret = 1;
        goto cleanup;
    }

    len = strlen(basedir);
    if (len <= 0) {
        std::cout << "Base directory path too short" << std::endl;
        ret = 2;
        goto cleanup;
    }

    if (len >= MAX_NAME_LEN - 20) {
        std::cout << "Base directory path too long" << std::endl;
        ret = 3;
        goto cleanup;
    }

    results = new double[repetitions];
    if (results == NULL) {
        std::cout << "Failed to allocate results storage" << std::endl;
        ret = 4;
        goto cleanup;
    }

    // Generate filenames
    for (int i = 0; i < FILE_COUNT; i++) {
        len = snprintf(buf[i], MAX_NAME_LEN, "%s/%d", basedir, i);
        if (len <= 0 || len >= MAX_NAME_LEN) {
            std::cout << "Failed to generate name" << std::endl;
            ret = 5;
            goto cleanup;
        }        
    }

    INIT_COUNTERS(counters);

    struct timespec start, stop;
    for (int i = 0; i < repetitions; i++) {
        
        START_COUNTERS(counters);
        clock_gettime(CLOCK_MONOTONIC, &start);
        ret = run_instance();
        clock_gettime(CLOCK_MONOTONIC, &stop);
        END_COUNTERS(counters);

        if (ret != 0) {
            std::cout << "Run " << i << " failed" << std::endl;
            ret = 6;
            goto cleanup;
        }

        results[i] = printTimespec(start, stop, "metadata");
    }


    // Perform analysis
    double total, mean, median, p90;
    
    // Sort the data to make analysis easier
    qsort(results, repetitions, sizeof(results[0]), compare_double);

    median = results[repetitions/2];
    p90 = results[(int)((double)repetitions*0.90)];

    // Capture the mean
    total = 0;
    for (int i = 0; i < repetitions; i++) {
        total = total + results[i];
    }
    mean = total / (double)repetitions;

    std::cout << "Final times, total: " << total
                         << ", median: " << median
                         << ", mean: " << mean
                         << ", p90: " << p90 << std::endl;

    PRINT_COUNTERS(counters);

    ret = 0;
cleanup:
    FREE_COUNTERS(counters);
    if (results != NULL) {
        delete results;
    }
    return ret;
}

int main(int argc, char **argv) {

    int ret; 
    int reps;
    char *basedir;
        
    if (argc != 3) {
        std::cout << "Not enough arguments" << std::endl
                  << "Usage: metadata <basedirectory> <repetitions>" << std::endl;
        return 1;
    }

    reps = atoi(argv[2]);
    if (reps <= 0) {
        std::cout << "Invalid repetiions" << std::endl;
        return 1;
    }

    basedir = argv[1];

    ret = run_benchmark(basedir, reps);
    return ret;
}
