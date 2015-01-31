
Benchmark::Benchmark(char* benchmarkName)
    : benchmarkName_(benchmarkName) { }


void Benchmark::runBenchmark() {

    initialize();

    warmup();

    struct timespec ts_start, ts_stop;
    ts_start = clock();
    run();
    ts_stop = clock();
    printTimespec(ts_start, ts_stop);    

    cooldown();

    cleanup();
}

/**
 * Captures the time using some available clock
 */
struct timespec Benchmark::clock() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts;
}

struct duo Benchmark::duoDiff(long firstHigh, long firstLow, long secondHigh, long secondLow, long base) {

    long h = firstHigh - secondHigh;
    long l = firstLow - secondLow;
    if (h < 0) {
        throw std::runtime_exception("Bad time");
    }
    if (l < 0) {
        l += base;
        --h;
    }
    struct duo result;
    result.higher = h;
    result.lower = l;
    return result;
}

std::string Benchmark::decimalFormat(long number, long base) {
    std::stringstream decimalString;

    decimalString << ".";

    while (number > 0) {
        number *= 10;
        decimalString << number/base;
        number %= base;
    }

    return decimalString.str();
}

void Benchmark::printTimespec(struct timespec& ts_start, struct timespec& ts_stop) {

    struct duo = duoDiff((long)ts_stop.tv_sec, ts_stop.tv_nsec,
                        (long)ts_start.tv_sec, ts_start.tv_nsec,
                        1000000000);

    time_t elapsed_sec = (time_t)timeDuo.higher;
    long elapsed_nsec = timeDuo.lower;

    std::cout << "Time " << benchmarkName_ << ": "
                << elapsed_sec << decimalFormat(elapsed_nsec, 1000000000) << std::endl;

}
