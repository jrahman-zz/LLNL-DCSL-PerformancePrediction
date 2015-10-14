#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <iostream>
#include <sstream>

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


int
main(int argc, char** argv)
{
  struct timespec ts_start, ts_stop;
  char buf[256];
  int size;
  FILE* file;

  int repeat = atoi(argv[2]);

  // XXX warmup
  file = fopen(argv[1], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    size += strlen(buf);
  }
  fclose(file);
  // XXX warmup

  file = fopen(argv[1], "r");
  if (file == NULL)
    std::cout << "failed with errno " << errno << std::endl;

  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int i=0; i<repeat; ++i) {
    size = 0;
    while (fgets(buf, sizeof(buf), file) != NULL) {
      size += strlen(buf);
    }
    rewind(file);
  }

  clock_gettime(CLOCK_MONOTONIC, &ts_stop);

  fclose(file);

  printTimespec(ts_start, ts_stop, argv[0]);
}
