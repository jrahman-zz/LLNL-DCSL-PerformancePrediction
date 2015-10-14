
from application import Application
import re
import logging

class Spec(Application):

    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        Application.__init__(self, environ, 'Spec', client_cores, app_cores, nice, instance)
        self._size = size
        self._load_params = [self._bmark_name, self._size]
        self._cleanup_params = [self._bmark_name]
        self._run_params = [self._bmark_name, self._size, '0']
        self._interfere_params = [self._bmark_name, self._size, '1']

    def _process_output(self, output):
        #regex = r"%s[^-]*--\s*(\d*(?:\.\d*)?)[^-]*--\s*S.*\n" % self._bmark_name
        regex = r"real\s*(\d+)m(\d+\.\d+)"
        match = re.search(regex, output)
        if match is None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match')
        #return { 'time': float(match.group(1)) }
        return { 'time': 60.0 * int(match.group(1)) + float(match.group(2)) }

    def __str__(self):
        return "spec_%s" % (self._bmark_name)

    # regex=r".*Estimated.*Estimated\s*\n\s*Base\s*Base \s*Base \s*Peak\s*Peak\s*Peak\s*\nBenchmarks\s*Ref\.\s*Run\sTime\s*Ratio\s*Ref\.\s*Run\sTime\s*Ratio\s*\n[-\s]*\n(?:.*\n)*?%s[^-]*--[^-]*?(\d*\.\d*)[^-]*--\s*S.*\n(?:.*?\n)*\s*Est\.\s*SPECint2006\s*Not\sRun\s*\n\n\s*set:\sfp\s*\n\n\s*The\slog\sfor\sthis\srun\sis\sin .*\.log" % (self._bmark_name)
        
class SpecPerlbench(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '400.perlbench'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecBzip(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '401.bzip2'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecGcc(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '403.gcc'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecGobmk(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '445.gobmk'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecHmmer(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '456.hmmer'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecSjeng(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '458.sjeng'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecLibquantum(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '462.libquantum'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecHRef(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '464.h264ref'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecOmnetpp(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '471.omnetpp'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecAstar(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '473.astar'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecXalancbmk(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '483.xalancbmk'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecBwaves(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '410.bwaves'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecGamess(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '416.gamess'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecMilc(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '433.milc'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecZeusmp(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '434.zeusmp'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecGromacs(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '435.gromacs'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecCactusADM(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '436.cactusADM'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecLeslie(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '437.leslie3d'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecNamd(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '444.namd'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecDealII(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '447.dealII'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecSoplex(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '450.soplex'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecPovray(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '453.povray'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecCalculix(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '454.calculix'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecGemsFDTD(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '459.GemsFDTD'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecTonto(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '465.tonto'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecLbm(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '470.lbm'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecWrf(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '481.wrf'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)

class SpecSphinx(Spec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1, size='train'):
        self._bmark_name = '482.sphinx3'
        Spec.__init__(self, environ, app_cores, client_cores, nice, instance, size)


if __name__ == '__main__':
    data = """                                  Estimated                       Estimated
                Base     Base       Base        Peak     Peak       Peak
Benchmarks      Ref.   Run Time     Ratio       Ref.   Run Time     Ratio
-------------- ------  ---------  ---------    ------  ---------  ---------
400.perlbench                               NR                                 
401.bzip2                                   NR                                 
403.gcc                                     NR                                 
429.mcf                                     NR                                 
445.gobmk                                   NR                                 
456.hmmer                                   NR                                 
458.sjeng                                   NR                                 
462.libquantum                              NR                                 
464.h264ref        --       73.4         -- S                                  
471.omnetpp                                 NR                                 
473.astar                                   NR                                 
483.xalancbmk                               NR                                 
 Est. SPECint_base2006                   --
 Est. SPECint2006                                                   Not Run

      set: fp

                The log for this run is in /home/jprahman/SPEC2006/result/CPU2006.052.log"""

    m = SpecHRef({'data_dir': 'test', 'applications': {'Spec': {'application_dir': 'test', 'script_dir': 'test' }}}, [], [])
    print m._parse_output(data)
