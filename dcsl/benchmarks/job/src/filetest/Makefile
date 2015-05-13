BINDIR = ../bin
CC = g++
CFLAGS =
LDFLAGS = -lrt
OBJS = filetest.o


all: filetest

filetest: $(OBJS)
	$(CC) $^ -o $@ $(LDFLAGS) 
	cp $@ $(BINDIR)/

clean:
	rm -f $(OBJS) filetest
