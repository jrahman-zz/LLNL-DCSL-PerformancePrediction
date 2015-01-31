#include <stdio.h>
#include <iostream>

using namespace std;

struct Time {
  double tsp;
  double td;
  double alloctest;
  double memory0;
  double memory1;
  double memory2;
  double memory3;
  double filetest;

  void print() {
    cout << tsp
         << "," << td
         << "," << alloctest
         << "," << memory0
         << "," << memory1
         << "," << memory2
         << "," << memory3
         << "," << filetest;
  }
};

struct Cpu {
  char vendor_id[32];
  int family;
  int model;
  char model_name[128];
  int stepping;
  double mhz;
  int cache_size;
  int physical_id;
  int siblings;
  int core_id;
  int cores;
  int apicid;
  int initialapicid;
  char fpu[32];
  char fpu_exception[32];
  int cpuid_level;
  char wp[32];
  char flags[512];
  double bogomips;
  int tlb_page_num;
  int tlb_page_size;
  int clflush_size;
  int cache_alignment;
  int physical_address_size;
  int virtual_address_size;
  char power_management[64];

  void print() {
    cout << "," << vendor_id
         << "," << family
         << "," << model
         << "," << model_name
         << "," << stepping
         << "," << mhz
         << "," << cache_size
         << "," << physical_id
         << "," << siblings
         << "," << core_id
         << "," << cores
         << "," << apicid
         << "," << initialapicid
         << "," << fpu
         << "," << fpu_exception
         << "," << cpuid_level
         << "," << wp
         << "," << flags
         << "," << bogomips
         << "," << tlb_page_num
         << "," << tlb_page_size
         << "," << clflush_size
         << "," << cache_alignment
         << "," << physical_address_size
         << "," << virtual_address_size
         << "," << power_management;
  }
};

struct Memory {
  int total;
  int free;
  int buffers;
  int cached;
  int swapcached;
  int active;
  int inactive;
  int activeanon;
  int inactiveanon;
  int activefile;
  int inactivefile;
  int unevictable;
  int mlocked;
  int hightotal;
  int highfree;
  int lowtotal;
  int lowfree;
  int swaptotal;
  int swapfree;
  int dirty;
  int writeback;
  int anonpages;
  int mapped;
  int shmem;
  int slab;
  int sreclaimable;
  int sunreclaim;
  int kernelstack;
  int pagetables;
  int nfs_unstable;
  int bounce;
  int writebacktmp;
  int commitlimit;
  int committed_as;
  long vmalloctotal;
  long vmallocused;
  long vmallocchunk;
  int hardwarecorrupted;
  int anonhugepages;
  int hugepages_total;
  int hugepages_free;
  int hugepages_rsvd;
  int hugepages_surp;
  int hugepagesize;
  int directmap4k;
  int directmap2m;
  int directmap1g;

  void print() {
    cout << "," << total
         << "," << free
         << "," << buffers
         << "," << cached
         << "," << swapcached
         << "," << active
         << "," << inactive
         << "," << activeanon
         << "," << inactiveanon
         << "," << activefile
         << "," << inactivefile
         << "," << unevictable
         << "," << mlocked
         << "," << hightotal
         << "," << highfree
         << "," << lowtotal
         << "," << lowfree
         << "," << swaptotal
         << "," << swapfree
         << "," << dirty
         << "," << writeback
         << "," << anonpages
         << "," << mapped
         << "," << shmem
         << "," << slab
         << "," << sreclaimable
         << "," << sunreclaim
         << "," << kernelstack
         << "," << pagetables
         << "," << nfs_unstable
         << "," << bounce
         << "," << writebacktmp
         << "," << commitlimit
         << "," << committed_as
         << "," << vmalloctotal
         << "," << vmallocused
         << "," << vmallocchunk
         << "," << hardwarecorrupted
         << "," << anonhugepages
         << "," << hugepages_total
         << "," << hugepages_free
         << "," << hugepages_rsvd
         << "," << hugepages_surp
         << "," << hugepagesize
         << "," << directmap4k
         << "," << directmap2m
         << "," << directmap1g;
  }
};

struct Alloctest {
  int hour;
  int minute;
  int second;
  double totaltime;
  double usertime;
  double systime;
  int maxres;
  int textsize;
  int datasize;
  int stacksize;
  int softpagefaults;
  int hardpagefaults;
  int swaps;
  int inops;
  int outops;
  int ipcsent;
  int ipcrecv;
  int signals;
  int voluntaryctxswitches;
  int involuntaryctxswitches;

  void print() {
    cout << "," << hour
         << "," << minute
         << "," << second
         << "," << totaltime
         << "," << usertime
         << "," << systime
         << "," << maxres
         << "," << textsize
         << "," << datasize
         << "," << stacksize
         << "," << softpagefaults
         << "," << hardpagefaults
         << "," << swaps
         << "," << inops
         << "," << outops
         << "," << ipcsent
         << "," << ipcrecv
         << "," << signals
         << "," << voluntaryctxswitches
         << "," << involuntaryctxswitches;
  }
};

struct Filetest {
  int read;
  
  void print() {
    cout << "," << read;
  }
};

int
main(int argc, char** argv)
{
  char hostname[32];
  char dayofweek[8];
  char month[8];
  int dayofmonth;
  int hour;
  int minute;
  int second;
  int year;
  char uname[1024];
  Time time;
  Cpu cpu;
  Memory mem;
  Alloctest alloctest;
  Filetest filetest;

  FILE* fp = fopen(argv[1], "r");

  fscanf(fp, "%s\n", hostname);
  fscanf(fp, "%s %s %d %d:%d:%d %d\n", dayofweek, month, &dayofmonth, &hour, &minute, &second, &year);
  fscanf(fp, "%[^\n]\n", uname);
  fscanf(fp, "vendor_id : %s\n", cpu.vendor_id);
  fscanf(fp, "cpu family : %d\n", &cpu.family);
  fscanf(fp, "model : %d\n", &cpu.model);
  fscanf(fp, "model name : %[^\n]\n", cpu.model_name);
  fscanf(fp, "stepping : %d\n", &cpu.stepping);
  fscanf(fp, "cpu MHz : %lf\n", &cpu.mhz);
  fscanf(fp, "cache size : %d KB\n", &cpu.cache_size);
  fscanf(fp, "physical id : %d\n", &cpu.physical_id);
  fscanf(fp, "siblings : %d\n", &cpu.siblings);
  fscanf(fp, "core id : %d\n", &cpu.core_id);
  fscanf(fp, "cpu cores : %d\n", &cpu.cores);
  fscanf(fp, "apicid : %d\n", &cpu.apicid);
  fscanf(fp, "initial apicid : %d\n", &cpu.initialapicid);
  fscanf(fp, "fpu : %s\n", cpu.fpu);
  fscanf(fp, "fpu_exception : %s\n", cpu.fpu_exception);
  fscanf(fp, "cpuid level : %d\n", &cpu.cpuid_level);
  fscanf(fp, "wp : %s\n", cpu.wp);
  fscanf(fp, "flags : %[^\n]\n", cpu.flags);
  fscanf(fp, "bogomips : %lf\n", &cpu.bogomips);
  fscanf(fp, "TLB size : %d %dK pages\n", &cpu.tlb_page_num, &cpu.tlb_page_size);
  fscanf(fp, "clflush size : %d\n", &cpu.clflush_size);
  fscanf(fp, "cache_alignment : %d\n", &cpu.cache_alignment);
  fscanf(fp, "address sizes : %d bits physical, %d bits virtual\n", &cpu.physical_address_size, &cpu.virtual_address_size);
  fscanf(fp, "power management:%[^\n]\n\n", cpu.power_management);
  fscanf(fp, "MemTotal: %d kB\n", &mem.total);
  fscanf(fp, "MemFree: %d kB\n", &mem.free);
  fscanf(fp, "Buffers: %d kB\n", &mem.buffers);
  fscanf(fp, "Cached: %d kB\n", &mem.cached);
  fscanf(fp, "SwapCached: %d kB\n", &mem.swapcached);
  fscanf(fp, "Active: %d kB\n", &mem.active);
  fscanf(fp, "Inactive: %d kB\n", &mem.inactive);
  fscanf(fp, "Active(anon): %d kB\n", &mem.activeanon);
  fscanf(fp, "Inactive(anon): %d kB\n", &mem.inactiveanon);
  fscanf(fp, "Active(file): %d kB\n", &mem.activefile);
  fscanf(fp, "Inactive(file): %d kB\n", &mem.inactivefile);
  fscanf(fp, "Unevictable: %d kB\n", &mem.unevictable);
  fscanf(fp, "Mlocked: %d kB\n", &mem.mlocked);
  fscanf(fp, "HighTotal: %d kB\n", &mem.hightotal);
  fscanf(fp, "HighFree: %d kB\n", &mem.highfree);
  fscanf(fp, "LowTotal: %d kB\n", &mem.lowtotal);
  fscanf(fp, "LowFree: %d kB\n", &mem.lowfree);
  fscanf(fp, "SwapTotal: %d kB\n", &mem.swaptotal);
  fscanf(fp, "SwapFree: %d kB\n", &mem.swapfree);
  fscanf(fp, "Dirty: %d kB\n", &mem.dirty);
  fscanf(fp, "Writeback: %d kB\n", &mem.writeback);
  fscanf(fp, "AnonPages: %d kB\n", &mem.anonpages);
  fscanf(fp, "Mapped: %d kB\n", &mem.mapped);
  fscanf(fp, "Shmem: %d kB\n", &mem.shmem);
  fscanf(fp, "Slab: %d kB\n", &mem.slab);
  fscanf(fp, "SReclaimable: %d kB\n", &mem.sreclaimable);
  fscanf(fp, "SUnreclaim: %d kB\n", &mem.sunreclaim);
  fscanf(fp, "KernelStack: %d kB\n", &mem.kernelstack);
  fscanf(fp, "PageTables: %d kB\n", &mem.pagetables);
  fscanf(fp, "NFS_Unstable: %d kB\n", &mem.nfs_unstable);
  fscanf(fp, "Bounce: %d kB\n", &mem.bounce);
  fscanf(fp, "WritebackTmp: %d kB\n", &mem.writebacktmp);
  fscanf(fp, "CommitLimit: %d kB\n", &mem.commitlimit);
  fscanf(fp, "Committed_AS: %d kB\n", &mem.committed_as);
  fscanf(fp, "VmallocTotal: %ld kB\n", &mem.vmalloctotal);
  fscanf(fp, "VmallocUsed: %ld kB\n", &mem.vmallocused);
  fscanf(fp, "VmallocChunk: %ld kB\n", &mem.vmallocchunk);
  fscanf(fp, "HardwareCorrupted: %d kB\n", &mem.hardwarecorrupted);
  fscanf(fp, "AnonHugePages: %d kB\n", &mem.anonhugepages);
  fscanf(fp, "HugePages_Total: %d\n", &mem.hugepages_total);
  fscanf(fp, "HugePages_Free: %d\n", &mem.hugepages_free);
  fscanf(fp, "HugePages_Rsvd: %d\n", &mem.hugepages_rsvd);
  fscanf(fp, "HugePages_Surp: %d\n", &mem.hugepages_surp);
  fscanf(fp, "Hugepagesize: %d kB\n", &mem.hugepagesize);
  fscanf(fp, "DirectMap4k: %d kB\n", &mem.directmap4k);
  fscanf(fp, "DirectMap2M: %d kB\n", &mem.directmap2m);
  fscanf(fp, "DirectMap1G: %d kB\n", &mem.directmap1g);
  fscanf(fp, "Time in seconds: %lf\n", &time.tsp);
  fscanf(fp, "Time in seconds: %lf\n", &time.td);
  fscanf(fp, "Now: %d:%d:%d\n", &alloctest.hour, &alloctest.minute, &alloctest.second);
  fscanf(fp, "Time in seconds = %lf\n", &time.alloctest);
  fscanf(fp, "Total time (in seconds) = %lf\n", &alloctest.totaltime);
  fscanf(fp, "Total amount of user time used = %lf\n", &alloctest.usertime);
  fscanf(fp, "Total amount of system time used = %lf\n", &alloctest.systime);
  fscanf(fp, "Maximum resident set size (in kilobytes) = %d\n", &alloctest.maxres);
  fscanf(fp, "Amount of text segment memory shared (kilobyte-seconds) = %d\n", &alloctest.textsize);
  fscanf(fp, "Amount of data segment memory used (kilobyte-seconds) = %d\n", &alloctest.datasize);
  fscanf(fp, "Amount of stack memory used (kilobyte-seconds) = %d\n", &alloctest.stacksize);
  fscanf(fp, "Number of soft page faults = %d\n", &alloctest.softpagefaults);
  fscanf(fp, "Number of hard page faults = %d\n", &alloctest.hardpagefaults);
  fscanf(fp, "Number of times swapped out of memory = %d\n", &alloctest.swaps);
  fscanf(fp, "Number of input operations via the file system = %d\n", &alloctest.inops);
  fscanf(fp, "Number of output operations via the file system = %d\n", &alloctest.outops);
  fscanf(fp, "Number of IPC messages sent = %d\n", &alloctest.ipcsent);
  fscanf(fp, "Number of IPC messages received = %d\n", &alloctest.ipcrecv);
  fscanf(fp, "Number of signals delivered = %d\n", &alloctest.signals);
  fscanf(fp, "Number of voluntary context switches = %d\n", &alloctest.voluntaryctxswitches);
  fscanf(fp, "Number of involuntary context switches = %d\n", &alloctest.involuntaryctxswitches);
  fscanf(fp, "Time in seconds = %lf\n", &time.memory0);
  fscanf(fp, "Time in seconds = %lf\n", &time.memory1);
  fscanf(fp, "Time in seconds = %lf\n", &time.memory2);
  fscanf(fp, "Time in seconds = %lf\n", &time.memory3);
  fscanf(fp, "Time in seconds = %lf\n", &time.filetest);
  fscanf(fp, "read in %d bytes\n", &filetest.read);

  fclose(fp);

  time.print();
  printf(",%s", hostname);
  printf(",%s,%s,%d,%d,%d,%d,%d", dayofweek, month, dayofmonth, hour, minute, second, year);
  printf(",%s", uname);
  cpu.print();
  mem.print();
  alloctest.print();
  filetest.print();
  printf("\n");
}
