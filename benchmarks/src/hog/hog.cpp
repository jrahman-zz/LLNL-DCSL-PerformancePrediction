#include <signal.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>

#define NUM_USEC 1000

int usec;

void
handler(int signal)
{
  usleep(usec);
}

main(int argc, char** argv)
{
  /*
  if (argc > 1)
    usec = atoi(argv[1]);
  else
    usec = NUM_USEC;

  struct itimerval timer;
  timer.it_interval.tv_sec = 0;
  timer.it_interval.tv_usec = NUM_USEC;
  timer.it_value.tv_sec = 0;
  timer.it_value.tv_usec = NUM_USEC;
  setitimer(ITIMER_PROF, &timer, 0);

  struct sigaction sig;
  sig.sa_handler = handler;
  sigemptyset(&sig.sa_mask);
  sig.sa_flags = 0;
  sigaction(SIGPROF, &sig, 0);
  */

  while(1);
}
