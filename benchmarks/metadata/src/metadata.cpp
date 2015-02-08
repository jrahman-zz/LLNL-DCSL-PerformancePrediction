

#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sstream>
#include <iostream>

#define FILE_COUNT 1000
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
        
        // Only open the file if it doesn't exist
        fd[i] = open(buf[i], O_RDWR | O_CREAT | O_EXCL);
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
            remove(buf[i]);
        }
    }

    return ret;
}

int run_benchmark(char *basedir, int repetitions) {

    int ret, len;
    double *results = NULL;
    
    if (repetitions <= 0 || !basedir) {
        std::cout << "Bad arguments" << std::endl;
        ret = -1;
        goto cleanup;
    }

    len = strlen(basedir);
    if (len <= 0) {
        std::cout << "Base directory path too short" << std::endl;
        ret = -1;
        goto cleanup;
    }

    if (len >= MAX_NAME_LEN - 20) {
        std::cout << "Base directory path too long" << std::endl;
        ret = -1;
        goto cleanup;
    }

    results = new double[repetitions];
    if (results == NULL) {
        std::cout << "Failed to allocate results storage" << std::endl;
        ret = -1;
        goto cleanup;
    }

    // Generate filenames
    for (int i = 0; i < FILE_COUNT; i++) {
        len = snprintf(buf[i], MAX_NAME_LEN, "%s/%d", basedir, i);
        if (len <= 0 || len >= MAX_NAME_LEN) {
            std::cout << "Failed to generate name" << std::endl;
            ret = -1;
            goto cleanup;
        }        
    }

    struct timespec start, stop;
    for (int i = 0; i < repetitions; i++) {
        
        clock_gettime(CLOCK_MONOTONIC, &start);
        ret = run_instance();
        clock_gettime(CLOCK_MONOTONIC, &stop);

        if (ret != 0) {
            std::cout << "Run " << i << " failed" << std::endl;
            ret = -1;
            goto cleanup;
        }

        results[i] = printTimespec(start, stop, "metadata");
    }


    // Perform analysis
    double total, mean, median, p99;
    
    // Sort the data to make analysis easier
    qsort(results, repetitions, sizeof(results[0]), compare_double);

    median = results[repetitions/2];
    p99 = results[(int)((double)repetitions*0.99)];

    // Capture the mean
    total = 0;
    for (int i = 0; i < repetitions; i++) {
        total = total + results[i];
    }
    mean = total / (double)repetitions;

    std::cout << "Final times, total: " << total
                         << ", median: " << median
                         << ", mean: " << mean
                         << ", p99: " << p99 << std::endl;

    ret = 0;
cleanup:
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
    return (ret == 0) ? 0 : 1;
}
