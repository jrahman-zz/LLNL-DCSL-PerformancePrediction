#include <stdio.h>
#include <stdlib.h>
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
  FILE* file;
  int i, j, index;
  double v;
  char s[256];
  char buf[256];
  int xdim = atoi(argv[1]);
  int ydim = atoi(argv[2]);
  double** A;
  double* x;
  double* y;
  double* Ax;
  double* Aty;
  double* result_Ax;
  double* result_Aty;

  A = new double* [xdim];
  x = new double [ydim];
  y = new double [xdim];
  Ax = new double [xdim];
  Aty = new double [ydim];
  result_Ax = new double[xdim];
  result_Aty = new double[ydim];
  for (i=0; i<xdim; ++i)
    A[i] = new double [ydim];

  file = fopen(argv[3], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    sscanf(buf, "%8d%8d%s\n", &i, &j, s);
    v = atof(s);
    A[i-1][j-1] = v;
  }
  fclose(file);

  index = 0;
  file = fopen(argv[4], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    v = atof(buf);
    x[index++] = v;
  }
  fclose(file);

  index = 0;
  file = fopen(argv[5], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    v = atof(buf);
    y[index++] = v;
  }
  fclose(file);

  index = 0;
  file = fopen(argv[6], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    v = atof(buf);
    Ax[index++] = v;
  }
  fclose(file);

  index = 0;
  file = fopen(argv[7], "r");
  while (fgets(buf, sizeof(buf), file) != NULL) {
    v = atof(buf);
    Aty[index++] = v;
  }
  fclose(file);

  // XXX warmup
  for (i=0; i<xdim; ++i) {
    result_Ax[i] = 0;
    for (j=0; j<ydim; ++j)
      result_Ax[i] += A[i][j] * x[j];
  }

  for (i=0; i<ydim; ++i) {
    result_Aty[i] = 0;
    for (j=0; j<xdim; ++j)
      result_Aty[i] += A[j][i] * y[j];
  }

  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int repeat=0; repeat<100000; ++repeat) {

    for (i=0; i<xdim; ++i) {
      result_Ax[i] = 0;
      for (j=0; j<ydim; ++j)
        result_Ax[i] += A[i][j] * x[j];
    }

    for (i=0; i<ydim; ++i) {
      result_Aty[i] = 0;
      for (j=0; j<xdim; ++j)
        result_Aty[i] += A[j][i] * y[j];
    }
  }

  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, argv[0]);

  for (i=0; i<xdim; ++i) {
    if (result_Ax[i] - Ax[i] > 1e-12) {
      //printf("Error in computing Ax[%d]: result_Ax = %.16f, Ax = %.16f\n", i, result_Ax[i], Ax[i]);
      return -1;
    }
  }

  for (i=0; i<ydim; ++i) {
    if (result_Aty[i] - Aty[i] > 1e-12) {
      //printf("Error in computing Aty[%d]: result_Aty = %.16f, Aty = %.16f\n", i, result_Aty[i], Aty[i]);
      return -1;
    }
  }

  for (i=0; i<xdim; ++i)
    delete[] A[i];
  delete[] A;
  delete[] x;
  delete[] y;
  delete[] Ax;
  delete[] Aty;
  delete[] result_Ax;
  delete[] result_Aty;

  return 0;
}
