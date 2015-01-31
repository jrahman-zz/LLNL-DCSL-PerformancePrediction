BINDIR = ../bin
CC = g++ 

all: alloctest

CFLAGS =

LDFLAGS = -pthread -lrt

alloctest.o: alloctest.cpp
	$(CC) -c -o alloctest.o alloctest.cpp

alloctest: alloctest.o
	$(CC) alloctest.o -o alloctest $(LDFLAGS)
	cp $@ $(BINDIR)/

clean:
	rm -f alloctest *.o
