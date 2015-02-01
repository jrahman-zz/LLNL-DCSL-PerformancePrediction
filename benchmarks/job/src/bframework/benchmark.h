
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <sstream>

class Benchmark {

    public:
        Benchmark(char* benchmarkName);
        

        void runBenchmark();

    protected:

        /**
         * Record a moment in time using a clock
         */
        struct timespec clock();

        void initialize() = 0;
        void warmup() = 0;
        void run() = 0;
        void cooldown() = 0;
        void cleanup() = 0;

    private:

        // TODO, support per thread calculations

        // Remove default constructor
        Benchmark() = delete;

        struct duo {
            long higher;
            long lower;
        };

        struct duo duoDiff(long firstHigher, long firstLower, long secondHiger, long secondLower, long base);

        std::string decimalFormat(long number, long base);

       void printTimespec(struct timespec& ts_start, struct timespec_t ts_stop, char* app); 

       char* benchmarkName_;
}
