#ifndef PAPI_COUNTERS_H
#define PAPI_COUNTERS_H

#include "papi_util.h"

#ifdef _cplusplus 
extern "C" {
#endif
papi_counters_t* create_miss_counters(void); 
#ifdef _cplusplus
}
#endif

#endif
