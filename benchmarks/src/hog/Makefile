BINDIR = ../bin
CC = g++
CFLAGS =
LDFLAGS = -lrt
OBJS = hog.o


all: hog

hog: $(OBJS)
	$(CC) $^ -o $@ $(LDFLAGS) 
	cp $@ $(BINDIR)/

clean:
	rm -f $(OBJS) hog
