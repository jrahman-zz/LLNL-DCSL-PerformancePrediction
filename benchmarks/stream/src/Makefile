CC = gcc
CFLAGS = -O2
CFLAGS2 = -O0

#FF = g77
FF = gfortran
FFLAGS = -O2

#all: stream_f.exe stream_c.exe
all: stream streamV2 stream_interfere streamV2_interfere

stream_f.exe: stream.f mysecond.o
	$(CC) $(CFLAGS) -c mysecond.c
	$(FF) $(FFLAGS) -c stream.f
	$(FF) $(FFLAGS) stream.o mysecond.o -o stream_f.exe

stream: stream.c
	$(CC) $(CFLAGS) stream.c -o stream

stream_interfere: stream.c
	$(CC) $(CFLAGS) stream.c -DNTIMES=100000 -o stream_interfere

streamV2: stream.c
	$(CC) $(CFLAGS2) stream.c -o streamV2

streamV2_interfere: stream.c
	$(CC) $(CFLAGS2) stream.c -DNTIMES=100000 -o streamV2_interfere

clean:
	rm -f stream_f.exe stream streamV2 stream_interfere streamV2_interfere *.o

clobber: 
	rm *~
