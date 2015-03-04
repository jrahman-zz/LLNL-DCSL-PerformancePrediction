/* Short test program to test sched_setaffinity
* (which sets the affinity of processes to processors).
* Compile: gcc sched_setaffinity_test.c -o sched_setaffinity_test -lm
* Usage: ./sched_setaffinity_test
*
* Open a "top"-window at the same time and see all the work
* being done on CPU 0 first and after a short wait on CPU 1.
* Repeat with different numbers to make sure, it is not a
* coincidence.
       
#include <stdio.h>
#include <math.h>
#include <sched.h>
*/

#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <sched.h>
#include <unistd.h>
#include <syscall.h>
#include <errno.h>
#include <pthread.h>
//#include <papi.h>
#include <signal.h>
#include <math.h>
#include <string.h>
#include <sstream>
#include <iostream>

// Add tuning parameters

#ifndef BANDWIDTH_SCALE
#define BANDWIDTH_SCALE 3736503
#endif

#ifndef REGULAR_STRIDE
#define REGULAR_STRIDE 1
#endif

#ifndef RANDOM_STRIDE
#define RANDOM_STRIDE 64
#endif

long long int identity(long long int n_);

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

char* app;

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


void measurement_bandwidth(long long int n_, int CPU_, int repeat) {

  // int n_counters = 3;
  // int Events[3] = { PAPI_L3_TCR, PAPI_L3_TCA,  PAPI_L3_TCM};
  // //int Events[3] = { PAPI_L1_DCM, PAPI_L2_DCM, PAPI_L3_TCM};
  // long long int time_old=0, time_new=0, time_old2=0, time_new2=0, time_old3=0;
  // long long int * Values = new long long int [n_counters];
  // long long int * Average_values = new long long int [n_counters];
  // long long int average_time=0, average_time2=0;

  // if(CPU_==0) {
    // for(int i=0; i<n_counters; i++) { 
      // Average_values[i] =  0;
    // }

    // if (PAPI_start_counters(Events, 3) != PAPI_OK) {
      // printf("counters non started!\n");
      // exit(1);
    // }
  // }

  //long long int bubble_size  = n_;
  //n_ = 48001;

  long long int* vec_ = new long long int[n_];
  long long int* vec_2 = new long long int[n_];
  long long int* vec_3 = new long long int[n_];
  long long int* vec_4 = new long long int[n_];
  long long int* vec_5 = new long long int[n_];
  long long int* vec_6 = new long long int[n_];
  long long int* vec_7 = new long long int[n_];
  long long int* vec_8 = new long long int[n_];
  long long int* vec_9 = new long long int[n_];
  long long int* vec_10 = new long long int[n_];
  long long int* vec_11 = new long long int[n_];
  long long int* vec_12 = new long long int[n_];
  long long int* vec_13 = new long long int[n_];
  long long int* vec_14 = new long long int[n_];
  long long int* vec_15 = new long long int[n_];
  long long int* vec_16 = new long long int[n_];
  long long int* vec_17 = new long long int[n_];
  long long int* vec_18 = new long long int[n_];
  long long int* vec_19 = new long long int[n_];
  long long int* vec_20 = new long long int[n_];
  long long int* vec_21 = new long long int[n_];
  long long int* vec_22 = new long long int[n_];
  long long int* vec_23 = new long long int[n_];
  long long int* vec_24 = new long long int[n_];
  long long int* vec_25 = new long long int[n_];
  long long int* vec_26 = new long long int[n_];
  long long int* vec_27 = new long long int[n_];
  long long int* vec_28 = new long long int[n_];
  long long int* vec_29 = new long long int[n_];
  long long int* vec_30 = new long long int[n_];
  long long int* vec_31 = new long long int[n_];
  long long int* vec_32 = new long long int[n_];
  long long int* vec_33 = new long long int[n_];
  long long int* vec_34 = new long long int[n_];
  long long int* vec_35 = new long long int[n_];
  long long int* vec_36 = new long long int[n_];
  long long int* vec_37 = new long long int[n_];
  long long int* vec_38 = new long long int[n_];
  long long int* vec_39 = new long long int[n_];
  long long int* vec_40 = new long long int[n_];
  long long int* vec_41 = new long long int[n_];
  long long int* vec_42 = new long long int[n_];
  long long int* vec_43 = new long long int[n_];
  long long int* vec_44 = new long long int[n_];

 


  long long int sum=666;  


  if(vec_==0)
    printf("Error Allocating Memory\n");

  long long int num_obs = 1000000000/n_;
  long long int freq_bubbles = 10000;
  long long int bubble_size  = 1000; 
  double b=0;
  //WARM-UP
  //for(int k_=0; k_<n_; k_++) {
  //  vec_[k_] = 1;
  //}
  fprintf(stderr, "CPU = %d n = %lld num_obs=%d\n", CPU_, n_, num_obs);



  //srand ( time(NULL) );

  /*long long int *pos = new long long int[num_obs];

  for(int j = 0; j < num_obs; j++)
    pos[j] = (3736503*j)%n_; */


  long long int a = 1000;
  srand ( time(NULL) );
  

  // if(CPU_==0) {
    // PAPI_read_counters(Values, n_counters);
    // time_old = PAPI_get_real_usec();
  // }
  
  struct timespec ts_start, ts_stop;
  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int i=0; i<repeat; ++i) {
  
    for( long long int k_=0; k_<num_obs; k_++) {

      //vec_33[identity(pos[k_])]++;a

      //time_old3 = PAPI_get_real_usec();

      vec_[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_2[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_3[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_4[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_5[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_6[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_7[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_8[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_9[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_10[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_11[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_12[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_13[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_14[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_15[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_16[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_17[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_18[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_19[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_20[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_21[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_22[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_23[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_24[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_25[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_26[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_27[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_28[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_29[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_30[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_31[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_32[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_33[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_34[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_35[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_36[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_37[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_38[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_39[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_40[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_41[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_42[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_43[identity(BANDWIDTH_SCALE*k_)%n_]++;
      vec_44[identity(BANDWIDTH_SCALE*k_)%n_]++;




    }
  }
  //fprintf(stderr, "%lld\n", sum);
  // time_new = PAPI_get_real_usec();
  
  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, app);
  
  // //average_time += (time_new - time_old);
  // if(CPU_ == 0) {
    // PAPI_read_counters(Values, 3);
    // //time_new = PAPI_get_real_usec();

  // }

  // if(CPU_ == 0 ) {
    // fprintf(stdout, "(Size, PAPI_L3_TCM/PAPI_L3_TCR, PAPI_L3_TCM/PAPI_L3_TCA) = ");
    // fprintf(stdout, "%lld ", n_);
    // for(int i=0; i<n_counters-1; i++) {
      // fprintf(stdout, "%lf ",  (double)Values[n_counters-1]/(double)(Values[i]));
    // }
    // //long long int = 8 bytes, cache line size is 64 bytes, #(long long int accesses * cache_line_size) / ms == MB / s
    // fprintf(stdout, "BW (MB/s) [ %lf %lf ]\n ", 64*(double)Values[n_counters-1]/(double)(time_new - time_old),  64*(double)Values[n_counters-1]/(double)(time_new - time_old));

    // //fprintf(stdout, "%lf #vector_accesses=%d, #misses=%lld #L3_accesses=%lld, #vec_acces/#L3_acces = %lf\n", (double)64*Values[n_counters-1]/(time_new - time_old), num_obs*44, Values[2], Values[1], (double)num_obs*44/Values[1] );

  // }
  // /*if(CPU_ == 0 ) {
    // fprintf(stdout, "%lld %lld ", n_, size_);
    // for(int i=0; i<n_counters; i++) {
      // fprintf(stdout, "%lf ", 100*(float)Values[i]/(num_obs*45));
      // //Average_values[i] = 0;
    // }
    // //fprintf(stdout, "BW %lf ", (float)average_time/n_*8*2);
    // fprintf(stdout, "%lf\n", (float)(time_new -time_old)/(num_obs*45));
  // }*/
  // if(CPU_==0)
    // PAPI_shutdown();
  free(vec_);
  free(vec_2);
  free(vec_3);
  free(vec_4);
  free(vec_5);
  free(vec_6);
  free(vec_7);
  free(vec_8);
  free(vec_9);
  free(vec_10);
  free(vec_11);
  free(vec_12);
  free(vec_13);
  free(vec_14);
  free(vec_15);
  free(vec_16);
  free(vec_17);
  free(vec_18);
  free(vec_19);
  free(vec_20);
  free(vec_21);
  free(vec_22);
  free(vec_23);
  free(vec_24);
  free(vec_25);
  free(vec_26);
  free(vec_27);
  free(vec_28);
  free(vec_29);
  free(vec_30);
  free(vec_31);
  free(vec_32);
  free(vec_33);
  free(vec_34);
  free(vec_35);
  free(vec_36);
  free(vec_37);
  free(vec_38);
  free(vec_39);
  free(vec_40);
  free(vec_41);
  free(vec_42);
  free(vec_43);
  free(vec_44);
}

// n_ is the length of the loop 
// size_ is the size of the vectors being accessed in the contaminating routines
void measurement_regular_access(long long int n_, int CPU_, int repeat) {

  // int n_counters = 3;
  // int Events[3] = {PAPI_L1_DCM, PAPI_L2_DCM, PAPI_L3_TCM};
  // //int Events[3] = {PAPI_L3_TCR, PAPI_L3_TCA, PAPI_L3_TCM};
  // /*int n_counters = 3;
  // int Events[3] = { PAPI_L1_DCM, PAPI_L2_DCM, PAPI_TOT_CYC};*/
  // long long int time_old, time_new;
  // long long int * Values = new long long int [n_counters];
  // long long int * Average_values = new long long int [n_counters];
  // long long int average_time;

  // if(CPU_==0) {
    // for(int i=0; i<n_counters; i++) {
      // Average_values[i] =  0;
    // }
    // average_time =  0;

    // if (PAPI_start_counters(Events, 3) != PAPI_OK) {
      // printf("counters non started!\n");
      // exit(1);
    // }
  // }


  int* vec_ = new int[n_];
  if(vec_==0)
    printf("Error Allocating Memory\n");

  int num_obs = 1000000000/n_;
  if(num_obs<1)
    num_obs=1;

  //WARM-UP
  for(int k_=0; k_<n_; k_++) {
    vec_[k_] = 1;
  }
  fprintf(stderr, "CPU = %d n = %lld num_obs=%d\n", CPU_, n_, num_obs);
  
  struct timespec ts_start, ts_stop;
  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int j=0; j<repeat; ++j) {
    for(int i=0; i<num_obs; i++ ) {

      // if(CPU_==0) {
        // PAPI_read_counters(Values, n_counters);
        // time_old = PAPI_get_real_usec();
      // }
      for( long long int k_=0; k_<n_; k_ += REGULAR_STRIDE) {
        //printf("%lld %lld %lld %lld\n", (k_*500)%n_, (k_*1000)%n_, 500*k_, n_);
        //Stride = 1 
        vec_[k_]++;
      }
      // if(CPU_ == 0) {
        // PAPI_read_counters(Values, 3);
        // time_new = PAPI_get_real_usec();

        // //printf("CPU = %d L1 = %lld L2 = %lld Cycles = %lld time=%lld\n", CPU_, Values[0], Values[1], Values[2], time_new - time_old);
        // for(int i=0; i<n_counters; i++) {
          // Average_values[i]  +=  Values[i];
        // }
        // average_time +=  time_new - time_old;
      // }
    }
  }
  // if(CPU_ == 0 ) {
    // fprintf(stdout, "(size, PAPI_L1_DCM, PAPI_L2_DCM, PAPI_L3_TCM) = ");
    // fprintf(stdout, "%lld ", n_);
    // for(int i=0; i<n_counters; i++) {
      // fprintf(stdout, "%lld ", Average_values[i]);
      // //Average_values[i] = 0;
    // }
    // //fprintf(stdout, "BW %lf ", (float)average_time/n_*8*2);
    // fprintf(stdout, "time/obs %lf\n", (float)average_time/(num_obs));
    // average_time = 0;
  // }
  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, app);

  free(vec_);
  // if(CPU_==0)
    // PAPI_shutdown();
}



// n_ is the size of the vector 
// size is the size of the vectors being accessed in the contaminating routines
void measurement_random_access(long long int n_, int CPU_, int repeat) {

  // int n_counters = 3;
  // int Events[3] = {PAPI_L1_DCM, PAPI_L2_DCM, PAPI_L3_TCM};
  // //int Events[3] = {PAPI_L3_TCR, PAPI_L3_TCA, PAPI_L3_TCM};
  // /*int n_counters = 3;
  // int Events[3] = { PAPI_L1_DCM, PAPI_L2_DCM, PAPI_TOT_CYC};*/
  // long long int time_old, time_new;
  // long long int * Values = new long long int [n_counters];
  // long long int * Average_values = new long long int [n_counters];
  // long long int average_time;

  // if(CPU_==0) {
    // for(int i=0; i<n_counters; i++) { 
    // Average_values[i] =  0;
    // }
    // average_time =  0;

    // if (PAPI_start_counters(Events, 3) != PAPI_OK) {
      // printf("counters non started!\n");
      // exit(1);
    // }
  // }
  int* vec_ = new int[n_];
  if(vec_==0) 
    printf("Error Allocating Memory\n");

  int num_obs = 1000000000/n_;
  if(num_obs<1)
    num_obs=1;
  //WARM-UP
  for(int k_=0; k_<n_; k_++) {
    vec_[k_] = 1;
  }
  srand ( time(NULL) );
  fprintf(stderr, "CPU = %d n = %lld num_obs=%d\n", CPU_, n_, num_obs);

  int index;
  struct timespec ts_start, ts_stop;
  clock_gettime(CLOCK_MONOTONIC, &ts_start);

  for (int j=0; j<repeat; ++j) {
    for(int i=0; i<num_obs; i++ ) {

      // if(CPU_==0) {
        // PAPI_read_counters(Values, n_counters);
        // time_old = PAPI_get_real_usec();
      // }
      for( long long int k_=0; k_<n_; k_++) {
        //printf("%lld %lld %lld %lld\n", (k_*500)%n_, (k_*1000)%n_, 500*k_, n_);
        //Stride = 1 
        //vec_[k_]++;

        //Stride = 3000000 
        //vec_[(3736503*k_)%n_]++;
        index = rand();
        vec_[index%n_] += index;
        #ifdef V2
        vec_[(index+RANDOM_STRIDE)%n_] += vec_[((unsigned int)vec_[index%n_])%n_];
        vec_[(index+2*RANDOM_STRIDE)%n_] += vec_[((unsigned int)vec_[2*index%n_])%n_];
        vec_[(index+3*RANDOM_STRIDE)%n_] += vec_[((unsigned int)vec_[3*index%n_])%n_];
        vec_[(index+4*RANDOM_STRIDE)%n_] += vec_[((unsigned int)vec_[4*index%n_])%n_];
        #endif
      
      }
      // if(CPU_ == 0) {
        // PAPI_read_counters(Values, 3);
        // time_new = PAPI_get_real_usec();

        // //printf("CPU = %d L1 = %lld L2 = %lld Cycles = %lld time=%lld\n", CPU_, Values[0], Values[1], Values[2], time_new - time_old);
        // for(int i=0; i<n_counters; i++) {
          // Average_values[i]  +=  Values[i];
        // }
        // average_time +=  time_new - time_old;
      // }
    }
  }

  // if(CPU_ == 0 ) {
    // fprintf(stdout, "(size, PAPI_L1_DCM, PAPI_L2_DCM, PAPI_L3_TCM) = ");
    // fprintf(stdout, "%lld ", n_);
    // for(int i=0; i<n_counters; i++) { 
      // fprintf(stdout, "%lld ", Average_values[i]);
      // //Average_values[i] = 0;
    // }
    // //fprintf(stdout, "BW %lf ", (float)average_time/n_*8*2);
    // fprintf(stdout, "time/obs %lf\n", (float)average_time/(num_obs));
    // average_time = 0;

  // }
  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, app);

  free(vec_);
}


// n_ is the length of the loop 
// size_ is the size of the vectors being accessed in the contaminating routines
void compress_branch(long long int n_, int CPU_, int repeat) {

  cpu_set_t mask;
  CPU_ZERO(&mask);
  CPU_SET(CPU_, &mask);

  if (sched_setaffinity(0, sizeof(mask), &mask) <0) {
    printf("ERROR sched_setaffinityi\n");
    exit(1);
  }
  // int n_counters = 3;
  // int Events[3] = {PAPI_L1_DCM, PAPI_L2_DCM, PAPI_BR_MSP};
  // //int Events[3] = {PAPI_L3_TCR, PAPI_L3_TCA, PAPI_L3_TCM};
  // /*int n_counters = 3;
  // int Events[3] = { PAPI_L1_DCM, PAPI_L2_DCM, PAPI_TOT_CYC};*/
  // long long int time_old, time_new, time_old_old, time_old_old_old, time_outside_bubble=0;
  // long long int * Values = new long long int [n_counters];
  // long long int * Average_values = new long long int [n_counters];
  // long long int average_time, random_number;


  // if(CPU_==0) {
    // for(int i=0; i<n_counters; i++) {
      // Average_values[i] =  0;
    // }
    // average_time =  0;

    // if (PAPI_start_counters(Events, 3) != PAPI_OK) {
      // printf("counters non started!\n");
      // exit(1);
    // }
  // }



  int size = 200;

  int* vec_ = new int[size];
  long long int* positions = new long long int[ size ];
  if(vec_==0 ) {
    printf("Error Allocating Memory\n");
    exit(-666);
  }

  //srand ( time(NULL)*CPU_ );

  struct random_data* rand_states = (struct random_data*)calloc(1, sizeof(struct random_data));
  char* rand_statebufs = (char*)calloc(1, 8);
  initstate_r(random(), rand_statebufs, 8, rand_states);
  int r1;


  for(int k_ = 0; k_<size; k_++) {
    random_r(rand_states, &r1);
    positions[k_]=r1%size;
  }

  int num_obs;

  if( n_ > 0)
    num_obs = 100000/n_;
  else
    num_obs = 100000;

  if(num_obs<100)
    num_obs=100;

  //WARM-UP
  for(int k_=0; k_<size; k_++) {
    vec_[k_] = 1;
  }

  fprintf(stderr, "CPU = %d n = %lld num_obs=%d\n", CPU_, n_, num_obs);
  
  struct timespec ts_start, ts_stop;
  clock_gettime(CLOCK_MONOTONIC, &ts_start);
  
  for (int j=0; j<repeat; ++j) {
    for(int i=0; i<num_obs; i++ ) {
      //random_number = rand();
      // if(CPU_==0) {
        // PAPI_read_counters(Values, n_counters);
        // time_old = PAPI_get_real_usec();
      // }
      for( long long int kk_=0; kk_<size; kk_++) {

        usleep(50);
        // the whole branch miss is 50 ms 
        // 1 iter == 2 ms
        for( long long int k_=0; k_<n_; k_++) {
          vec_[ positions[k_ % size] % size]=vec_[ positions[k_ % size] % size]*vec_[ positions[k_ % size] % size]/10;
          //vec_[ positions[k_ % size] % size]=identity(vec_[ positions[k_ % size] % size])/3736503;
          //vec_[ positions[k_ % size] % size]=identity(vec_[ positions[k_ % size] % size])*vec_[ positions[k_ % size] % size ];
        }
      }
      // if(CPU_ == 0) {
        // PAPI_read_counters(Values, 3);
        // time_new = PAPI_get_real_usec();

        // //printf("CPU = %d L1 = %lld L2 = %lld Cycles = %lld time=%lld\n", CPU_, Values[0], Values[1], Values[2], time_new - time_old);
        // for(int i=0; i<n_counters; i++) {
          // Average_values[i]  +=  Values[i];
        // }
        // average_time +=  time_new - time_old;
      // }

      //printf("i = %d num_obs = %d\n", i, num_obs);
    }
  }
  // if(CPU_ == 0 ) {
    // fprintf(stdout, "(size, PAPI_L1_DCM, PAPI_L2_DCM, PAPI_BR_MSP)= ");
    // fprintf(stdout, "%lld ", n_);
    // for(int i=0; i<n_counters; i++) {
      // fprintf(stdout, "%lld ", Average_values[i]);
      // //Average_values[i] = 0;
    // }
    // //fprintf(stdout, "BW %lf ", (float)average_time/n_*8*2);
    // fprintf(stdout, "time/obs %lf\n", (float)average_time/(num_obs));
    // average_time = 0;
  // }
  clock_gettime(CLOCK_MONOTONIC, &ts_stop);
  printTimespec(ts_start, ts_stop, app);

  free(vec_);
  free(positions);
  // if(CPU_==0)
    // PAPI_shutdown();
}

int main(int argc, char **argv)
{

  app = (char*) malloc(strlen(argv[0]) + strlen(argv[1]) + 1);
  strcpy(app, argv[0]);
  strcat(app, argv[1]);

  if(argc!=4) {
    printf("%s <benchmark: 0 bandwidth, 1 regular access, 2 random access, 3 branches> <size>\n", argv[0]);
    exit(-1);
  }

  int option;
  long long int size;
  int repeat;


  option = atoi(argv[1]);
  size   = atoll(argv[2]); 
  repeat = atoi(argv[3]);

  
  if(option == 0)
    measurement_bandwidth(size, 0, repeat);
  else if (option == 1)
    measurement_regular_access(size, 0, repeat);
  else if (option == 2)
    measurement_random_access(size, 0, repeat);
  else if (option == 3)
    compress_branch(size, 0, repeat);
}
