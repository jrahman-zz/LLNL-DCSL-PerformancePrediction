#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <sched.h>
#include <unistd.h>
#include <syscall.h>
#include <errno.h>
//#include <papi.h>
#include <signal.h>

long long int identity(long long int n_) {

	return n_;

}

