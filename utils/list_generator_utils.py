import random

def randomListGenerator(sz):
   sz = int(sz)
   return [random.randint(0,1) for _ in range(sz)]

def zeroListGenerator(sz):
   sz = int(sz)
   return [0 for _ in range(sz)]

  