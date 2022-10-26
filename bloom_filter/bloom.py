# UW CSE 312, PSet #4 Spring 2022
# Student Name: Sebastian Liu
# Email    : ll57@uw.edu

# =============================================================
# You may define helper functions, but DO NOT MODIFY
# the parameters or names of the provided functions.
# The autograder will expect that these functions exist
# and attempt to call them to grade you.

# Do NOT add any import statements.
# =============================================================

import numpy as np
import mmh3

class BloomFilter:
    def __init__(self, k:int = 10, m:int=100000):
        """
        :param k: The number of hash functions (rows).
        :param m: The number of buckets (cols).

        Initializes the bloom filter to all zeros, as a
        boolean array where True = 1 and False = 0.
        
        """
        self.k = k
        self.m = m
        self.t = np.zeros((k, m), dtype=bool)

    def hash(self, x, i:int) -> int:
        """
        :param x: The element x to be hashed.
        :param i: Which hash function to use, for i=0,...,self.k-1.
        :return: h_i(x) the ith hash function applied to x. We use
        the mmh3 Python package, which you may need to install using
        the command `pip3 install mmh3`. We take the hash value and mod
        it by our table size. This hash "theoretically" should give a 
        uniform random integer from 0 to self.m - 1.
        """
        return mmh3.hash(str(x), i) % self.m

    def add(self, x):
        """
        :param x: The element to add to the bloom filter.
        
        In this function, we add x to our bloom filter.

        Hint(s):
        1. Read the pseudocode provided!
        2. You will want to use self.hash(...).
        3. Remember we initialized our bit array to be of type
        boolean, so 1 should be represented as True, and 0 as 
        False.
        """
        for i in range(0,self.k):
            self.t[i,self.hash(x,i)]=1

    def contains(self, x) -> bool:
        """
        :param x: The element to check whether or not it belongs
        to the bloom filter.
        :return: True or False; whether or not it is in the bloom filter.
        As described in the notes, this is not always accurate and may give
        false positives sometimes. That is, if this function returns False, 
        the element is definitely not in our structure, but if this function 
        returns True, the element may or may not be in our structure.

        Hint(s):
        1. Read the pseudocode provided!
        2. Again, remember we initialized our bit array to be of type
        boolean, so 1 should be represented as True, and 0 as 
        False.
        """
        for i in range(0, self.k):
            if self.t[i,self.hash(x,i)] == 0:
                return 0
        return 1

if __name__ == '__main__':
    # You can test out things here. Feel free to write anything below.

    # Create a new bloom filter structure.
    bf = BloomFilter(k=10, m=8000) # 10 * 8,000 = 80,000 bits = 10 KB

    print("Adding malicious URLS to Bloom Filter")

    # Create our bloom filter of malicious URLs
    mal_urls = np.genfromtxt('/home/data/mal_urls.txt', dtype='str')
    for mal_url in mal_urls:
        bf.add(mal_url)
        assert bf.contains(mal_url) # After adding, should definitely be in

    print("Computing False Positive Rate (FPR) on 10000 Unseen URLs")
    # Check contains on 10000 different URLs to see what percentage
    # incorrectly are marked as being contained.
    fpr = 0
    test_urls = np.genfromtxt('/home/data/test_urls.txt', dtype='str')
    for test_url in test_urls:
        if bf.contains(test_url): # Should ideally return False
            fpr += 1
    fpr /= len(test_urls)
    print("FPR: {}".format(fpr))
