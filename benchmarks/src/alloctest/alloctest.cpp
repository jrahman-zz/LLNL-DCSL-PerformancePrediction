#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <iostream>
#include <sstream>

int nthreads = 1;
int niterations = 1000;
int nobjects = 1000;
int size = 1000;

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
  
void printTimespec(struct timespec& ts_start, struct timespec& ts_stop, char* app)
{
  struct duo* timeDuo = duoDiff((long) ts_stop.tv_sec, ts_stop.tv_nsec,
                                (long) ts_start.tv_sec, ts_start.tv_nsec,
                                1000000000);
  time_t elapsed_sec = (time_t) timeDuo->higher;
  long elapsed_nsec = timeDuo->lower;

  std::cout << "Time " << app << ": "
            << elapsed_sec << decimalFormat(elapsed_nsec, 1000000000) << std::endl;
}


void printCurrentTime()
{
  time_t rawtime;
  struct tm* timeinfo;
  char buffer[80];

  time(&rawtime);
  timeinfo = localtime(&rawtime);

  strftime (buffer, 80, "Now: %H:%M:%S", timeinfo);
  std::cout << buffer << std::endl;
}

char* app;

void* foo(void* data)
{
  char** a;
  struct timespec ts_start, ts_stop;

  // XXX warmup
  a = new char*[nobjects];
  a[0] = new char[size];
  delete[] a[0];
  delete[] a;

  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  a = new char*[nobjects];
  for (int i=0; i<niterations; ++i) {
    for (int o=0; o<nobjects; ++o)
      a[o] = new char[size];
    for (int o=0; o<nobjects; ++o)
      delete[] a[o];
  }
  delete[] a;

  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, app);
}

int main(int argc, char** argv)
{
  app = argv[0];

  if (argc >= 2) {
    nthreads = atoi(argv[1]);
  }

  if (argc >= 3) {
    niterations = atoi(argv[2]);
  }

  if (argc >= 4) {
    nobjects = atoi(argv[3]);
  }

  if (argc >= 5) {
    size = atoi(argv[4]);
  }

  pthread_t* threads = new pthread_t[nthreads];
  pthread_attr_t attr;
  int rc;
  void* status;

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

  //printCurrentTime();

  struct timespec ts_start, ts_stop;
  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_start);

  for (int t=0; t<nthreads; ++t) {
    rc = pthread_create(&threads[t], &attr, foo, (void*) t);
    if (rc) {
      std::cerr << __func__ << ": pthread_create() returned " << rc << std::endl;
      exit(-1);
    }
  }

  pthread_attr_destroy(&attr);
  
  for (int t=0; t<nthreads; ++t) {
    rc = pthread_join(threads[t], &status);
    if (rc) {
      std::cerr << __func__ << ": pthread_join() returned " << rc << std::endl;
      exit(-1);
    }
  }

  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_stop);

  struct rusage usage;
  getrusage(RUSAGE_SELF, &usage);

//  time_t elapsed_sec;
//  long elapsed_nsec;
//  elapsed_sec = ts_stop.tv_sec - ts_start.tv_sec;
//  elapsed_nsec = ts_stop.tv_nsec - ts_start.tv_nsec;
//  if (elapsed_nsec < 0) {
//    elapsed_nsec += 1000000000;
//    --elapsed_sec;
//  }

  struct duo* timeDuo = duoDiff((long) ts_stop.tv_sec, ts_stop.tv_nsec,
                                (long) ts_start.tv_sec, ts_start.tv_nsec,
                                1000000000);
  time_t elapsed_sec = (time_t) timeDuo->higher;
  long elapsed_nsec = timeDuo->lower;

//  std::cout << "Time in seconds = " << elapsed_sec << ".";
//
//  while (elapsed_nsec > 0) {
//    elapsed_nsec *= 10;
//    std::cout << elapsed_nsec / 1000000000;
//    elapsed_nsec %= 1000000000;
//  }
//  std::cout << std::endl;

  /*
  std::cerr << "Total time (in seconds) = "
            << elapsed_sec << decimalFormat(elapsed_nsec, 1000000000) << std::endl;
  std::cerr << "Total amount of user time used = "
            << usage.ru_utime.tv_sec << decimalFormat(usage.ru_utime.tv_usec, 1000000) << std::endl;
  std::cerr << "Total amount of system time used = "
            << usage.ru_stime.tv_sec << decimalFormat(usage.ru_stime.tv_usec, 1000000) << std::endl;
  std::cerr << "Maximum resident set size (in kilobytes) = "
            << usage.ru_maxrss << std::endl;
  std::cerr << "Amount of text segment memory shared (kilobyte-seconds) = "
            << usage.ru_ixrss << std::endl;
  std::cerr << "Amount of data segment memory used (kilobyte-seconds) = "
            << usage.ru_idrss << std::endl;
  std::cerr << "Amount of stack memory used (kilobyte-seconds) = "
            << usage.ru_isrss << std::endl;
  std::cerr << "Number of soft page faults = "
            << usage.ru_minflt << std::endl;
  std::cerr << "Number of hard page faults = "
            << usage.ru_majflt << std::endl;
  std::cerr << "Number of times swapped out of memory = "
            << usage.ru_nswap << std::endl;
  std::cerr << "Number of input operations via the file system = "
            << usage.ru_inblock << std::endl;
  std::cerr << "Number of output operations via the file system = "
            << usage.ru_oublock << std::endl;
  std::cerr << "Number of IPC messages sent = "
            << usage.ru_msgsnd << std::endl;
  std::cerr << "Number of IPC messages received = "
            << usage.ru_msgrcv << std::endl;
  std::cerr << "Number of signals delivered = "
            << usage.ru_nsignals << std::endl;
  std::cerr << "Number of voluntary context switches = "
            << usage.ru_nvcsw << std::endl;
  std::cerr << "Number of involuntary context switches = "
            << usage.ru_nivcsw << std::endl;
  */
}
