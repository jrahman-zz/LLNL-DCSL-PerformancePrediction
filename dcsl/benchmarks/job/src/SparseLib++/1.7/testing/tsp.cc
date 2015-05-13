/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/*             ********   ***                                 SparseLib++    */
/*          *******  **  ***       ***      ***               v. 1.5c        */
/*           *****      ***     ******** ********                            */
/*            *****    ***     ******** ********              R. Pozo        */
/*       **  *******  ***   **   ***      ***                 K. Remington   */
/*        ********   ********                                 A. Lumsdaine   */
/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/*                                                                           */
/*                                                                           */
/*                     SparseLib++ : Sparse Matrix Library                   */
/*                                                                           */
/*               National Institute of Standards and Technology              */
/*                        University of Notre Dame                           */
/*              Authors: R. Pozo, K. Remington, A. Lumsdaine                 */
/*                                                                           */
/*                                 NOTICE                                    */
/*                                                                           */
/* Permission to use, copy, modify, and distribute this software and         */
/* its documentation for any purpose and without fee is hereby granted       */
/* provided that the above notice appear in all copies and supporting        */
/* documentation.                                                            */
/*                                                                           */
/* Neither the Institutions (National Institute of Standards and Technology, */
/* University of Notre Dame) nor the Authors make any representations about  */
/* the suitability of this software for any purpose.  This software is       */
/* provided ``as is'' without expressed or implied warranty.                 */
/*                                                                           */
/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#include <iostream>
#include <sstream>
#include <stdlib.h>

#include "compcol_double.h"
#include "comprow_double.h"
#include "ilupre_double.h"
#include "icpre_double.h"
#include "iotext_double.h"

using namespace std;

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

int main(int argc, char * argv[])
{
  struct timespec ts_start, ts_stop;

  if (argc < 6) {
      cerr << "Usage: A  x  y  A*x   A'*y   (filenames)" << endl;
    exit(-1);
  }

  int verbose = 0;
  int errcount = 0;

  if (argc > 6 )  {
    if (argv[6][1] == 'v')
      verbose = 1;
    else {
      cerr << "Usage: A  x  y  A*x   A'*y   (filenames)" << endl;
      return -1;
    }
  }

  char *A_name = argv[1];
  char *x_name = argv[2];
  char *y_name = argv[3];
  char *Ax_name  =argv[4];
  char *Aty_name = argv[5];

  CompCol_Mat_double Acol;
  CompRow_Mat_double Arow;
  Coord_Mat_double Acoord;

  VECTOR_double x, y;
  VECTOR_double Ax, Aty;

  readtxtfile_mat(A_name, &Acoord);
  Acol = Acoord;
  Arow = Acol;

  readtxtfile_vec(x_name, &x);
  readtxtfile_vec(y_name, &y);
  readtxtfile_vec(Ax_name, &Ax);
  readtxtfile_vec(Aty_name, &Aty);

  if (verbose)
  {
    cout << "Dimensons: " << endl;
    cout << " A ("<< Acoord.dim(0) << "," << Acoord.dim(1) << ") ";
    cout << " x: (" << x.size() << ")  y: (" << y.size() << ")"  << endl;
    cout << " A*x: " << Ax.size()  <<  endl;
    cout << " A'*y:"  << Aty.size()  << endl; 
  } 

  // XXX warmup
  if (norm(Ax - Acol*x) > 1e-8 )
  {
    errcount++;
    if (verbose) cout << "A*x failed. (col)\n";
  }

  if (norm(Aty - Acol.trans_mult(y)) > 1e-8)
  {
    errcount++;
    if (verbose) cout << "A'*y failed. (col) \n";
  }

  if (norm(Ax - Acoord*x) > 1e-8)
  {
    errcount++;
    if (verbose) cout << "A*x failed. (coord)\n";
  }
  
  if (norm(Aty - Acoord.trans_mult(y)) > 1e-8)
  {
    errcount++;
    if (verbose) cout << "A'*y failed. (coord)\n";
  }
  
  if (norm(Ax - Arow*x) > 1e-8)
  {
    errcount++;
    if (verbose) cout << "A*x failed (row).\n";
  }
    
  if (norm(Aty - Arow.trans_mult(y)) > 1e-8)
  {
    errcount++;
    if (verbose) cout << "A'*y failed (row).\n";
  }

  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int repeat=0; repeat<100000; ++repeat) {

    if (norm(Ax - Acol*x) > 1e-8 )
    {
      errcount++;
      if (verbose) cout << "A*x failed. (col)\n";
    }

    if (norm(Aty - Acol.trans_mult(y)) > 1e-8)
    {
      errcount++;
      if (verbose) cout << "A'*y failed. (col) \n";
    }

    if (norm(Ax - Acoord*x) > 1e-8)
    {
      errcount++;
      if (verbose) cout << "A*x failed. (coord)\n";
    }
    
    if (norm(Aty - Acoord.trans_mult(y)) > 1e-8)
    {
      errcount++;
      if (verbose) cout << "A'*y failed. (coord)\n";
    }
    
    if (norm(Ax - Arow*x) > 1e-8)
    {
      errcount++;
      if (verbose) cout << "A*x failed (row).\n";
    }
      
    if (norm(Aty - Arow.trans_mult(y)) > 1e-8)
    {
      errcount++;
      if (verbose) cout << "A'*y failed (row).\n";
    }

  }

  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, argv[0]);


  return errcount;
}
