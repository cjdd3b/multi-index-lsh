import random

def jaccard(s1, s2):
    x = set(s1)
    y = set(s2)
    return float(len(x & y)) / len(x | y)

def similarity(s1, s2):
    matches = 0
    for i, h in enumerate(s1):
        if h == s2[i]:
            matches += 1
    return matches / float(len(s1))

def hamming(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2)) / float(len(s1))

def split_chunks(bit_vector, k):
    return [bit_vector[k * i : k * (i + 1)] for i in xrange(len(bit_vector) // k)]

def flip(c): return str(1-int(c))

def flip_s(s, i):
   t =  s[:i]+flip(s[i])+s[i+1:]
   return t

def generate_close_chunks(s, k=1):
 if k>1:
      c = s[-1]
      s1 = [y+c for y in hamming(s[:-1], k)] if len(s) > k else []
      s2 = [y+flip(c) for y in hamming(s[:-1], k-1)]
      r = []
      r.extend(s1)
      r.extend(s2)
      return r
 else:
   return [flip_s(s,i) for i in range(len(s))]

class MinHasher(object):
    def __init__(self, n, universe_size, seed=None):
        if seed != None: random.seed(seed) 
        self.hash_functions = [self._create_random_hash_function(universe_size) for i in range(n)]

    def _create_random_hash_function(self, universe_size):
        a = random.randint(0, universe_size)
        b = random.randint(0, universe_size)
        return lambda x: (a * x + b) % universe_size

    def generate_signature(self, s):
        # Ideally retuns a bit vector
        return ''.join([self.sample_bits(self.calculate_minhash(func, s)) for func in self.hash_functions])

    def calculate_minhash(self, hash_function, s):
        # Trim this down to list comp with min()
        minhash = float("inf") 
        for item in s:
            value = hash_function(item)
            if value < minhash:
                minhash = value
        return int(minhash)

    def sample_bits(self, hash):
        bits = 0
        return str((bits << 1) | (hash & 1))

class LshTable(object):
    def __init__(self, n, k, r):
        self.n = n
        self.k = k
        self.r = r
        self.hash_tables = [{} for i in range(k)]

    def add(self, bit_vector):
        chunks = split_chunks(bit_vector, self.k)
        for i in range(self.k):
            hash_table = self.hash_tables[i]
            chunk = chunks[i]

            if chunk not in hash_table.keys():
                hash_table[chunk] = []

            hash_table[chunk].append(bit_vector)
        return

    def lookup(self, bit_vector):
        chunks = split_chunks(bit_vector, self.k)
        for i in range(self.k):
            hash_table = self.hash_tables[i]
            chunk = chunks[i]

            possible_matches = []
            close_chunks = generate_close_chunks(chunk)

            for close_chunk in close_chunks:
                if close_chunk in hash_table.keys():
                    possible_matches.append(hash_table[close_chunk])
        
        return possible_matches

if __name__ == '__main__':
    minhasher = MinHasher(32, 12549826247007890, 1234567)
    #print split_chunks('10101111000101110111001010110101', 8)

    t1 = minhasher.generate_signature([1,2,3])
    t2 = minhasher.generate_signature([1,2,2])

    l = LshTable(32, 4, 4)
    l.add(t1)
    print l.lookup(t2)


    # u1 = range(1,10000)
    # u2 = range(5001,20000)

    # s1 = minhasher.generate_signature(u1)
    # s2 = minhasher.generate_signature(u2)

    # print 'J(u1, u2) = %s' % jaccard(u1, u2)
    # print 'sim(u1, u2) = %s' % hamming(s1, s2)

    # print s1
    # print s2