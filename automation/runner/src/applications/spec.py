
from application import Application

import re

class Spec(Application):

    def __init__(self, environ, app_cores, client_cores):
        Application.__init__(self, environ, 'Spec', client_cores, app_cores)
        self._run_params = [self._bmark_name, 'train']
        self._intefere_params = [self._bmark_name, 'ref']

    def _parse_output(self, output):
        return {'hi': 'test'}

class SpecFloat(Spec):
    def __init__(self, environ, app_cores, client_cores):
        Spec.__init__(self, environ, app_cores, client_cores)

    def _parse_output(self, output):
        return {'hi': 'test'}

class SpecInt(Spec):
    def __init__(self, environ, app_cores, client_cores):
        Spec.__init__(self, environ, app_cores, client_cores)

    def _parse_output(self, output):
        regex=r".*Estimated.*Estimated\s*\n\s*Base\s*Base \s*Base \s*Peak\s*Peak\s*Peak\s*\nBenchmarks\s*Ref\.\s*Run\sTime\s*Ratio\s*Ref\.\s*Run\sTime\s*Ratio\s*\n[-\s]*\n(?:.*\n)*?%s[^-]*--[^-]*?(\d*\.\d*)[^-]*--\s*S.*\n(?:.*?\n)*\s*Est\.\s*SPECint2006\s*Not\sRun\s*\n\n\s*set:\sfp\s*\n\n\s*The\slog\sfor\sthis\srun\sis\sin .*\.log" % (self._bmark_name)
        match = re.search(regex, output)
        if match is None:
            raise Exception('No match')
        return { 'time': float(match.group(1)) }

class SpecPerlbench(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '400.perlbench'
        SpecInit.__init__(self, environ, app_cores, client_cores)

class SpecBzip(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '401.bzip2'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecGcc(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '403.gcc'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecGobmk(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '445.gobmk'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecHMMER(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '456.hmmer'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecSjeng(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '458.sjeng'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecLibquantum(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '462.libquantum'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecHRef(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '464.h264ref'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecOmnetpp(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '471.omnetpp'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecAstar(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '473.astar'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecXalancbmk(SpecInt):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '483.xalancbmk'
        SpecInt.__init__(self, environ, app_cores, client_cores)

class SpecBwaves(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '410.bwaves'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecGamess(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '416.gamess'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecMilc(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '433.milc'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecZeusmp(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '434.zeusmp'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecGromacs(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '435.gromacs'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecCactusADM(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '436.cactusADM'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecLeslie(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '437.leslie3d'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecNamd(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '444.namd'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecDealII(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '447.dealII'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecSoplex(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '450.soplex'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecPovray(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '453.povray'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecCalculix(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '454.calculix'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecGemsFDTD(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '459.GemsFDTD'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecTonto(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '465.tonto'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecLbm(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '470.lbm'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecWrf(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '481.wrf'
        SpecFloat.__init__(self, environ, app_cores, client_cores)

class SpecSphinx(SpecFloat):
    def __init__(self, environ, app_cores, client_cores):
        self._bmark_name = '482.sphinx3'
        SpecFloat.__init__(self, environ, app_cores, client_cores)


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
