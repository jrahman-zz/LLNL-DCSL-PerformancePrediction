CC = gcc
CFLAGS = -O2

#FF = g77
FF = gfortran
FFLAGS = -O2

#all: stream_f.exe stream_c.exe
all: stream stream_interfere

stream_f.exe: stream.f mysecond.o
	$(CC) $(CFLAGS) -c mysecond.c
	$(FF) $(FFLAGS) -c stream.f
	$(FF) $(FFLAGS) stream.o mysecond.o -o stream_f.exe

stream: stream.c
	$(CC) $(CFLAGS) stream.c -o stream

stream_interfere: stream.c
	$(CC) $(CFLAGS) stream.c -DNTIMES=1000 -o stream_interfere

clean:
	rm -f stream_f.exe stream stream_interfere *.o

clobber: 
	rm *~
