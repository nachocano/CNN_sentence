import numpy as np
import cPickle
from collections import defaultdict
import sys, re
import pandas as pd
import argparse

def load_data(filename):
    docs = []
    vocab = defaultdict(float)
    for line in open(filename).read().splitlines():
        line = line.strip()
        splitted = line.split()
        name = splitted[0]
        _, _, fold, label = name.split("_")
        sentences = ' '.join(str(s) for s in splitted[1:])
        num_words = len(splitted[1:])
        words = set(splitted[1:])
        for word in words:
            vocab[word] += 1
        datum  = {"y":int(label),
                  "text": sentences,
                  "num_words": num_words,
                  "split": int(fold)}
        docs.append(datum)
    return docs, vocab

def read_lines(f):
    for ii,line in enumerate(f):
        yield line

    
def get_W(filename, vocab, k=100):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(vocab)
    W = np.zeros(shape=(vocab_size+1, k))
    W[0] = np.zeros(k)
    word2idx = {}
    j = 1
    i = 0
    counter = 0
    for line in read_lines(open(filename, 'r')):
        if i == 0:
            i = 1
            continue
        #print 'processing %s' % counter
        counter += 1
        line = line.split()
        sentence = line[0]
        if sentence in vocab:
            W[j] = np.array(line[1:]).astype(np.float32)
            word2idx[sentence] = j
            j += 1
    return W, word2idx

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', required=True) # doc as sentences (probably the syntax based one)
    parser.add_argument('-e', '--embeddings', required=True) # sentence embeddings (or syntax one)
    parser.add_argument('-o', '--output', required=True) # pickle output
    args = parser.parse_args()

    print "loading data..."        
    docs, vocab = load_data(args.input)
    max_l = np.max(pd.DataFrame(docs)["num_words"])
    print "data loaded"
    print "number of sentences: " + str(len(docs))
    print "vocab size: " + str(len(vocab))
    print "max sentence length: " + str(max_l)

    W, word2idx = get_W(args.embeddings, vocab)
    cPickle.dump([docs, W, word2idx, vocab, max_l], open(args.output, "wb"))

    print "dataset created"

if __name__=="__main__":
    main()    

    