import json
import cirkit

### Misc
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ENDC = '\033[0m'

### Benchmarks
benchmarks = {
  "adder":      { 'verify': True },
  "arbiter":    { 'verify': True },
  "bar":        { 'verify': True },
  "cavlc":      { 'verify': True },
  "ctrl":       { 'verify': True },
  "dec":        { 'verify': True },
  "div":        { 'verify': True },
  "i2c":        { 'verify': True },
  "int2float":  { 'verify': True },
  "log2":       { 'verify': True },
  "max":        { 'verify': True },
  "mem_ctrl":   { 'verify': True },
  "multiplier": { 'verify': True },
  "priority":   { 'verify': True },
  "router":     { 'verify': True },
  "sin":        { 'verify': True },
  "sqrt":       { 'verify': True },
  "square":     { 'verify': True },
  "voter":      { 'verify': True },
  "hyp":        { 'verify': False },
}

### Configurations
configurations = {
    "aig" : {},
    "mig" : {},
    "xag" : {},
    "xmg" : {}
}

def aigerfile(name):
    return f"benchmarks/{name}.aig"

def resultfile(name, suffix, ext):
    return f"results/{name}_{suffix}.{ext}"

def read(name,filename):
    return cirkit.read_aiger(filename=filename, **{name : True})

def clear_store():
    cirkit.store(clear=True, aig=True, mig=True, xag=True, xmg=True, lut=True)
    
def ps(name):
  return cirkit.ps(silent=True, **{name : True})

def lut_mapping(name):
  return cirkit.lut_mapping(**{name : True})

def collapse_mapping(name):
  return cirkit.collapse_mapping(**{name : True})

def compute_stats(name,filename):
    ntk_stats = ps(name).dict()
    lut_mapping(name)
    collapse_mapping(name)
    lut_stats = ps('lut').dict()

    statistics = {
        'depth': ntk_stats['depth'],
        'gates' : ntk_stats['gates'],
        'luts' : lut_stats['gates']
    }

    return statistics

def rfz(name):
   if ( name == 'mig' ):
      return cirkit.refactor(strategy=1, progress=True, zero_gain=True)
   else:
      return {'time_total': 0.0}

def rf(name):
   if ( name == 'mig' ):
      return cirkit.refactor(strategy=1, progress=True)
   else:
      return {'time_total': 0.0}

def rwz(name):
  if ( name == 'mig' ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, zero_gain=True, mig=True)
  elif ( name == 'aig' ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, zero_gain=True, aig=True)
  elif ( name == "xmg" ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, zero_gain=True, xmg=True)
  elif ( name == "xag" ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, zero_gain=True, xag=True)
  else:
    print("[i] rwz: graph type not supported")

def rw(name):
  if ( name == 'mig' ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, mig=True)
  elif ( name == 'aig' ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, aig=True)
  elif ( name == "xmg" ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, xmg=True)
  elif ( name == "xag" ):
    return cirkit.cut_rewrite(strategy=0, progress=True, lutsize=4, xag=True)
  else:
    print("[i] rw: graph type not supported")
    
def rsz(name, cut_size, depth=1):
   return cirkit.resub(progress=True, max_pis=cut_size, depth=depth, zero_gain=True)

def rs(name, cut_size, depth=1):
   if name == "mig" and cut_size > 8 and depth > 1:
      depth = 1
   return cirkit.resub(progress=True, max_pis=cut_size, depth=depth)

def bz(name):
   if ( name == 'mig' ):
      return cirkit.mighty(area_aware=True)
   else:
      return {'time_total': 0.0}

compress2rs = [
    [bz, {}],
    [rs, {'cut_size': 6}],
    [rw, {}],
    [rs, {'cut_size': 6, 'depth':2}],
    [rf, {},],
    [rs, {'cut_size': 8},8],
    [bz, {},],
    [rs, {'cut_size': 8, 'depth':2}],
    [rw, {},],
    [rs, {'cut_size': 10}],
    [rwz, {},],
    [rs, {'cut_size': 10, 'depth':2}],
    [bz, {}],
    [rs, {'cut_size': 12}],
    [rfz, {}],
    [rs, {'cut_size': 12, 'depth':2}],
    [rwz, {}],
    [bz, {}],
]

for benchmark, benchmark_params in benchmarks.items():
    for name, configuration in configurations.items():
        print(f"[i] run {benchmark} with {name}")

        # read benchmark
        in_filename = aigerfile(benchmark)      
        read(name, in_filename)

        # compute statistics for initial benchmark
        stats_before = compute_stats(name, in_filename)

        # clear storage and re-read benchmark
        clear_store()
        read(name, in_filename)

        # run flow script
        time_total = 0.0
        for transformation in compress2rs:
            functor = transformation[0]
            args = transformation[1]
            
            stats = functor(name, **args)
            time = stats['time_total']

            # print(functor.__name__, args, '%8.2fs' % time)
            time_total = time_total + time
            
        # compute statistics for optimized benchmark
        stats_after = compute_stats(name, in_filename)

        print(stats_before)
        print(stats_after)
        print('%8.2fs' % time_total)

            
