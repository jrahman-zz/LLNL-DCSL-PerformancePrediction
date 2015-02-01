BINDIR = ../bin
CC = g++ 

all: example 

INCLUDE =

LIBS = -lrt

	
identity.o: identity.cpp
	$(CC) -c -o identity.o identity.cpp 

example.o: example.cpp
	$(CC) -c -o example.o example.cpp $(INCLUDE)

example: example.o identity.o
	 $(CC) example.o identity.o -o example $(LIBS)
	 cp $@ $(BINDIR)/

clean:
	rm -f example *.o
