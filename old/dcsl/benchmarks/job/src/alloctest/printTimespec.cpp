#include <iostream>
#include <time.h>

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
  
void printTimespec(struct timespec& ts_start, struct timespec& ts_stop)
{
  struct duo* timeDuo = duoDiff((long) ts_stop.tv_sec, ts_stop.tv_nsec,
                                (long) ts_start.tv_sec, ts_start.tv_nsec,
                                1000000000);
  time_t elapsed_sec = (time_t) timeDuo->higher;
  long elapsed_nsec = timeDuo->lower;

  std::cout << "Time in seconds = "
            << elapsed_sec << decimalFormat(elapsed_nsec, 1000000000) << std::endl;
}
