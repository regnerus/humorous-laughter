import tgt
from interlap import InterLap
from os import listdir
from os.path import isfile, join
import krippendorff
import numpy as np
from itertools import islice
import math
import itertools
import operator

#put textgrids in ./Annotations

mypath = "./Annotations/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

files = []
for n in onlyfiles:
    if n.endswith("R.TextGrid"):
        files.append((n.rstrip("R.TextGrid")))
    
def convert_to_float(i):
    return int(math.floor(i.start_time)),int(math.ceil(i.end_time)),i.text
   

def intify(code):
    if(code == 'H'):
        return 1
    if(code == 'N'):    
        return 0
    else:
        return 2
        
        
def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]
  
  
print(files)
br=[]
rr=[]
bc = 0 #count bouke
rc = 0 #count raoul

for x in files:
    inter = InterLap()
    b = tgt.read_textgrid(mypath+x+"B.TextGrid").tiers[1]
    r = tgt.read_textgrid(mypath+x+"R.TextGrid").tiers[1]
    bc+=len(b)
    rc+=len(r)
    inter.add([convert_to_float(i) for i in r])
    tot_overlaps = set()
    for i in b:
        interval = convert_to_float(i)
        overlaps = list(inter.find(interval))


        #print(interval[2])

        if(len(overlaps)>0):
            overlaps = [tuple(x) for x in overlaps]
            for o in overlaps:
                tot_overlaps.add(o)
            
            rr.append(most_common([o[2] for o in overlaps]))
            br.append(interval[2])
        else:
            rr.append("*")
            br.append(interval[2])
    
    #check for unmatched from Raoul
    for y in [tuple(convert_to_float(x)) for x in r]:
        if(y not in tot_overlaps):
            rr.append(y[2])
            br.append("*")
    #print(tot_overlaps)
#print(br)
#print(len(br))
#print(bc)


#print(rr)
#print(len(tot_overlaps))
#print(rc)
print(br.count("H")+rr.count("H"))
print(br.count("N")+rr.count("N"))
result = np.array([br,rr])
result = [[np.nan if v == '*' else intify(v) for v in coder] for coder in result]
print(result[0])
print(result[1])
print(len(result[0]))
print(len(result[1]))

print(krippendorff.alpha(reliability_data=result,level_of_measurement='ordinal'))










