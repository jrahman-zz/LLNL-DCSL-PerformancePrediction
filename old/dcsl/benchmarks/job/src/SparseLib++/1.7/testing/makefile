# 
# Makefile for sparselb testing
#

BINDIR = ../../../bin
SPARSELIB_DIR = ..
include $(SPARSELIB_DIR)/makefile.def


SRCS		= tsl.cc tpre.cc tspsm.cc tsp.cc td.cc
EXECS		= tsl    tpre    tspsm    tsp		 td
OBJS		= tsl.o  tpre.o  tspsm.o  tsp.o  td.o
all: progs

progs: $(EXECS)

clean:
	/bin/rm -f $(OBJS) $(EXECS) out *.out

wipe: 
	/bin/rm -f $(OBJS) $(EXECS) out *.out

tsl.o : tsl.cc  
tpre.o : tpre.cc  
tspsm.o : tspsm.cc  
tsp.o : tsp.cc
td.o : td.cc

tsl : tsl.o
	$(CCC) $(CCCFLAGS) -o tsl tsl.o  $(LDFLAGS)

tpre : tpre.o
	$(CCC) $(CCCFLAGS) -o tpre tpre.o  $(LDFLAGS)

tspsm : tspsm.o
	$(CCC) $(CCCFLAGS) -o tspsm tspsm.o  $(LDFLAGS)

tsp : tsp.o
	$(CCC) $(CCCFLAGS) -o tsp tsp.o  $(LDFLAGS) -lrt
	cp $@ $(BINDIR)/

td : td.o
	$(CCC) $(CCCFLAGS) -o td td.o  $(LDFLAGS) -lrt
	cp $@ $(BINDIR)/
