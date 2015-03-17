#!/usr/bin/env python

from automation.runner.run import run_experiement
import logging

interference=["StreamV2Scale", "StreamV2Add"]
#"MemoryV2Stream1K", "MemoryV2Stream1K", "MemoryV2Stream256M", "MemoryV2Random1M", "IOBenchV2Read1M", "IOBenchV2Read128M", "IOBenchV2Write4M", "Metadata"]

reps = 1

applications = ["SpecGromacs", "SpecSjeng"]
coloc_levels = [0, 1]

def main():
    
    for rep in range(0, reps):
        for thread in interference:
            for coloc_level in coloc_levels:
                if coloc_level == 0:
                    nice_levels = [0, 5, 10]
                else:
                    nice_levels = [0]
                for nice_level in nice_levels:
                    threadspec = ["%s:1:%d:%d" % (thread, coloc_level, nice_level)]
                    runspec = "%d:%s" % (rep, threadspec)
                    run_experiement(threadspec, applications, ".", "output/%s.json" % (runspec))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
