CC = g++ 

all: example exampleV2 

INCLUDE =

LIBS = -lrt

	
identity.o: identity.cpp
	$(CC) -c -o identity.o identity.cpp 

example.o: example.cpp
	$(CC) -c -o example.o example.cpp $(INCLUDE)

exampleV2.o: example.cpp
	$(CC) -DBANDWIDTH_SCALE=100000 -DREGULAR_STRIDE=1024 -c -o exampleV2.o example.cpp $(INCLUDE)

example: example.o identity.o
	 $(CC) example.o identity.o -o example $(LIBS)

exampleV2: exampleV2.o identity.o
	$(CC) exampleV2.o identity.o -o exampleV2 $(LIBS)

clean:
	rm -f example exampleV2 *.o
